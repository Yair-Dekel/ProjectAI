from board import Board
from king import King
from rook import Rook
import random

while True:
# Create a new board
    chess_board = Board()

    pieces = []
    # Create a white king and a white rook
    pieces.append(King('black', "King", chess_board))
    pieces.append(King('white', "King", chess_board))
    pieces.append(Rook('white', "Rook", chess_board))
    pieces.append(Rook('white', "Rook", chess_board))


    # Place the king and rook on the board
    for piece in pieces:
        position = (random.randint(0, 7), random.randint(0, 7))
        while not chess_board.check_empty(position):
            position = (random.randint(0, 7), random.randint(0, 7)) 
        chess_board.add_piece(piece, position)
    
    if not chess_board.is_in_check('black'):
        break

# Print the initial board setup
chess_board.print_board()

print(' ')

#hess_board.remeve_piece(pieces[0].get_position())

#pieces[1].print_my_board()

# get the best move for the white (by the objective functions)

white_turn = True

for i in range(16):
    if white_turn:
        rook1_move, rook1_value = pieces[2].objective_function()
        rook2_move, rook2_value = pieces[3].objective_function()
        white_king_move, white_king_value = pieces[1].objective_function()

        print(pieces[0].possible_moves(chess_board))
        # move the pieces with the highest value
        if rook1_value >= rook2_value and rook1_value >= white_king_value:
            chess_board.move_piece(pieces[2], rook1_move)
        elif rook2_value >= rook1_value and rook2_value >= white_king_value:
            chess_board.move_piece(pieces[3], rook2_move)
        else:
            chess_board.move_piece(pieces[1], white_king_move)

    else:

        black_king_move, black_king_value = pieces[0].objective_function()
        chess_board.move_piece(pieces[0], black_king_move)

    chess_board.print_board()
    print(' ')

    print(pieces[0].possible_moves(chess_board))
    print(pieces[1].possible_moves(chess_board))

    if len(pieces[0].possible_moves(chess_board)) == 0:
        print('White wins')
        break

    white_turn = not white_turn

games = 50
number_of_moves = 30
winning = 0
draw = 0

positions = []

boards = []

for j in range(games):
    while True:
    # Create a new board
        chess_board = Board()

        pieces = []
        # Create a white king and a white rook
        pieces.append(King('black', "King", chess_board))
        pieces.append(King('white', "King", chess_board))
        pieces.append(Rook('white', "Rook", chess_board))
        pieces.append(Rook('white', "Rook", chess_board))


        # Place the king and rook on the board
        for piece in pieces:
            position = (random.randint(0, 7), random.randint(0, 7))
            while not chess_board.check_empty(position):
                position = (random.randint(0, 7), random.randint(0, 7)) 
            chess_board.add_piece(piece, position)
        
        if not chess_board.is_in_check('black'):
            pieces_positions = []
            for piece in pieces:
                pieces_positions.append(piece.get_position())
            positions.append(pieces_positions)
            break

    white_turn = True

    #chess_board.print_board()
    #print(' ')
    boards.append(chess_board)

    for i in range(number_of_moves):
        if white_turn:
            rook1_move, rook1_value = pieces[2].objective_function()
            rook2_move, rook2_value = pieces[3].objective_function()
            white_king_move, white_king_value = pieces[1].objective_function()

            # move the pieces with the highest value
            if rook1_value >= rook2_value and rook1_value >= white_king_value:
                chess_board.move_piece(pieces[2], rook1_move)
            elif rook2_value >= rook1_value and rook2_value >= white_king_value:
                chess_board.move_piece(pieces[3], rook2_move)
            else:
                chess_board.move_piece(pieces[1], white_king_move)

        else:

            black_king_move, black_king_value = pieces[0].objective_function()
            chess_board.move_piece(pieces[0], black_king_move)
            if len(chess_board.pieces) < 4:
                break


        if len(pieces[0].possible_moves(chess_board)) == 0:
            #print('White wins')
            if chess_board.is_in_checkmate('black'):
                winning += 1
            else:
                draw += 1
            boards.pop()
            break

        white_turn = not white_turn

for board in boards:
    board.print_board()
    print(' ')

print(f'len of boards: {len(boards)}')

print(f'White wins {winning} out of {games} games, with {number_of_moves} moves each')
# Print the final board setup
print(f'{winning/games*100}%')

print(f'draw = {draw} \n{draw/games*100}%')
print(f'total = {winning + draw} \n{(winning + draw)/games*100}%')


