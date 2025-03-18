from board import Board
from king import King
from pawn import Pawn
import random
import sys
#chess.syzygy
# Official Website: http://syzygy-tables.info/

'''
chess.syzygy
python‑chess
import chess
import chess.syzygy

# Set up a board position (example: King and Pawn vs King)
board = chess.Board("8/8/8/8/8/8/k7/K7 w - - 0 1")

# Specify the directory where your Syzygy tablebase files are stored
tablebase_path = "/path/to/syzygy"

with chess.syzygy.open_tablebase(tablebase_path) as tablebase:
    wdl = tablebase.probe_wdl(board)  # Returns winning/drawing/losing info
    dtm = tablebase.probe_dtm(board)  # Returns moves to mate or distance to draw info

print("WDL:", wdl)
'''

def convert_board_to_fen(board):
    fen = ""
    for i in range(8):
        empty = 0
        for j in range(8):
            if board[i][j] == ' ':
                empty += 1
                #if j == 7 and empty > 0:
                #    fen += str(empty)
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += str(board[i][j])
        if empty > 0:
            fen += str(empty)
        if i < 7:
            fen += "/"
    return fen + " w - - 0 1"


def check_result_by_syzygy(board):
    import chess
    import chess.syzygy
    fen = convert_board_to_fen(board)
    #print(fen)
    # Set up a board position (example: King and Pawn vs King)
    board = chess.Board(fen)
    # Specify the directory where your Syzygy tablebase files are stored
    tablebase_path = "C:\\Users\\Yair\\pythonProjects\\ProgectAI\\tables"
    with chess.syzygy.open_tablebase(tablebase_path) as tablebase:
        wdl = tablebase.probe_wdl(board)  # Returns winning/drawing/losing info
    return wdl

if __name__ == '__main__':

    iterations = 10000
    moves = 50
    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])
        if len(sys.argv) > 2:
            moves = int(sys.argv[2])
        
    wins = 0
    loses = 0
    draw = 0
    exceptions = 0
    board_list = []
    board_start = []
    output = ""
    wins_syzygy = 0
    draw_syzygy = 0
    contradict_fen = set()
    lose_lose = []
    lose_win = []
    win_lose = []
    win_win = []

    j=0
    #for i in range(iterations):
    while j < iterations:
        # Create a new board
        chess_board = Board()

        pieces = []
        # Create a white king and a white rook
        pieces.append(King('black', "King", chess_board))
        pieces.append(King('white', "King", chess_board))
        pieces.append(Pawn('white', "Pawn", chess_board))

        position_black_king = (random.randint(0, 7), random.randint(0, 7))
        chess_board.add_piece(pieces[0], position_black_king)
        x_b_k, y_b_k = position_black_king

        position_white_king = position_black_king
        while not chess_board.check_empty(position_white_king):
            position_white_king = (random.randint(0, 7), random.randint(0, 7))
            x_w_k, y_w_k = position_white_king
            if abs(x_b_k - x_w_k) <= 1 and abs(y_b_k - y_w_k) <= 1:
                position_white_king = position_black_king
        chess_board.add_piece(pieces[1], position_white_king)

        position_pawn = position_black_king
        while not chess_board.check_empty(position_pawn):
            position_pawn = (random.randint(0, 6), random.randint(0, 7))
            x_p, y_p = position_pawn
            if x_b_k + 1 == x_p and abs(y_b_k - y_p) == 1:
                position_pawn = position_black_king
        chess_board.add_piece(pieces[2], position_pawn)

        # the pawn out of the range of the black king - the white always wins
        if x_p < x_b_k:
            continue
        #if y_b_k < y_p - x_p - 1 or y_b_k > y_p + x_p + 1:
        if y_b_k < y_p - x_p or y_b_k > y_p + x_p:
            continue
            
        # the black king closer to the pawn so the black always enforce a draw
        if max(abs(x_b_k - x_p), abs(y_b_k - y_p)) < max(abs(x_w_k - x_p), abs(y_w_k - y_p))-1:
            # this is exception case which the black king need one more step to reach the pawn
            if not (abs(x_b_k-x_p) == abs(y_b_k-y_p) and max(abs(x_w_k - x_p), abs(y_w_k - y_p)) - 2 == abs(x_b_k - x_p)):
                continue

        if j < 100:
            with open("all_boards.txt", "a") as file: 
                chess_board.print_to_file(file)
                file.write('\n')
            
        # Print the initial board setup
        #chess_board.print_board()
        board_list.append(chess_board)

        board_start.append(chess_board.board)
        white_turn = True
        fen = convert_board_to_fen(chess_board.board)
        wdl = check_result_by_syzygy(chess_board.board)
        if wdl == 0:
            draw_syzygy += 1
        elif wdl == 2:
            wins_syzygy += 1
            

        try:
            for i in range(moves):
                if white_turn:
                    pawn_move, pawn_value = pieces[2].objective_function()
                    white_king_move, white_king_value = pieces[1].objective_function_white()

                    # move the pieces with the lowest value
                    if pawn_value <= white_king_value:
                        chess_board.move_piece(pieces[2], pawn_move)
                    else:
                        chess_board.move_piece(pieces[1], white_king_move)

                else:
                    try:
                        black_king_move, black_king_value = pieces[0].objective_function_black()
                        chess_board.move_piece(pieces[0], black_king_move)
                    except Exception as e:
                        if e.args[0] == "No possible moves":
                            draw += 1
                            #j += 1
                            if wdl == 2:
                                contradict_fen.add(fen)
                                win_lose.append(fen)
                            with open("all_boards.txt", "a") as file:
                                file.write('Draw\n************\n') 
                            if wdl == 0:
                                lose_lose.append(fen)

                            #continue
                            break

                #chess_board.print_board()
                #print(' ')

                if len(chess_board.pieces) < 3:
                    #print('black wins')
                    draw += 1
                    #board_list.append(chess_board)
                    break
                pawn_pos_x, pawn_pos_y = pieces[2].position

                if pawn_pos_x == 0:
                    #print('white wins')
                    with open("all_boards.txt", "a") as file:
                        file.write('White wins\n************\n')
                    wins += 1
                    if wdl == 0:
                        contradict_fen.add(fen)
                        lose_win.append(fen)
                    if wdl == 2:
                        win_win.append(fen)
                    board_list.pop()
                    board_start.pop()
                    break


                white_turn = not white_turn
                if i == moves - 1:
                    with open("all_boards.txt", "a") as file:
                        file.write('Draw\n************\n')
                    draw += 1
                    if wdl == 2:
                        contradict_fen.add(fen)
                        win_lose.append(fen)
                    if wdl == 0:
                        lose_lose.append(fen)
                    #board_list.append(chess_board)
        except Exception as e:
            print(f"An error occurred: probaly draw... \n{e}")
            exceptions += 1
        
        j += 1
    
    print(f'White wins: {wins} times {wins/iterations*100}%')
    print(f'Black wins: {loses} times {loses/iterations*100}%')
    print(f'Draw: {draw} times {draw/iterations*100}%')
    print(f'Exceptions: {exceptions} times {exceptions/iterations*100}%')
    print()
    print(f'White wins by syzygy: {wins_syzygy} times {wins_syzygy/iterations*100}%')
    print(f'Draw by syzygy: {draw_syzygy} times {draw_syzygy/iterations*100}%')

    print()
    print(f'contradict_fen: {len(contradict_fen)}')
    print(f'expect lose but win: {len(lose_win)}')
    print(f'expect win but lose: {len(win_lose)}')
    print(f'expect win and win: {len(win_win)}')
    print(f'expect lose and lose: {len(lose_lose)}')

    with open("output.txt", "w") as file: 
        for chess_board in board_list:
            chess_board.print_to_file(file)
            file.write('\n')
    
    with open("output_start.txt", "w") as file: 
        for board in board_start:
            for row in board:
                file.write(' '.join([str(piece) if piece != ' ' else '.' for piece in row]) + '\n')
            file.write('\n')