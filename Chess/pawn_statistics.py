from board import Board
from king import King
from pawn import Pawn
import random
import sys

if __name__ == '__main__':

    iterations = 100
    moves = 30
    if len(sys.argv) > 1:
        iterations = int(sys.argv[1])
        if len(sys.argv) > 2:
            moves = int(sys.argv[2])
        
    wins = 0
    loses = 0
    board_list = []
    board_start = []
    for i in range(iterations):
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

        # Print the initial board setup
        #chess_board.print_board()
        board_list.append(chess_board)

        board_start.append(chess_board.board)
        white_turn = True

        for i in range(moves):
            if white_turn:
                pawn_move, pawn_value = pieces[2].objective_function()
                white_king_move, white_king_value = pieces[1].objective_function_white()

                # move the pieces with the highest value
                if pawn_value < white_king_value:
                    chess_board.move_piece(pieces[2], pawn_move)
                else:
                    chess_board.move_piece(pieces[1], white_king_move)

            else:
                black_king_move, black_king_value = pieces[0].objective_function_black()
                chess_board.move_piece(pieces[0], black_king_move)

            #chess_board.print_board()
            #print(' ')

            if len(chess_board.pieces) < 3:
                #print('black wins')
                loses += 1
                #board_list.append(chess_board)
                break
            pawn_pos_x, pawn_pos_y = pieces[2].position

            if pawn_pos_x == 0:
                #print('white wins')
                wins += 1
                board_list.pop()
                board_start.pop()
                break


            white_turn = not white_turn
            if i == moves - 1:
                loses += 1
                #board_list.append(chess_board)
    
    print(f'White wins: {wins} times {wins/iterations*100}%')
    print(f'Black wins: {loses} times {loses/iterations*100}%')

    with open("output.txt", "w") as file: 
        for chess_board in board_list:
            chess_board.print_to_file(file)
            file.write('\n')
    
    with open("output_start.txt", "w") as file: 
        for board in board_start:
            for row in board:
                file.write(' '.join([str(piece) if piece != ' ' else '.' for piece in row]) + '\n')
            file.write('\n')