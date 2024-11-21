from board import Board
from king import King
from rook import Rook
import random


# Create a new board
chess_board = Board()

pieces = []
# Create a white king and a white rook
pieces.append(King('black', "King", chess_board))
pieces.append(King('white', "King", chess_board))
pieces.append(Rook('white', "Rook", chess_board))
pieces.append(Rook('white', "Rook", chess_board))


# Place the king and rook on the board
chess_board.add_piece(pieces[0], (4, 6))
chess_board.add_piece(pieces[1], (4, 2))
chess_board.add_piece(pieces[2], (5, 1))
chess_board.add_piece(pieces[3], (1, 5))

# Print the initial board setup
chess_board.print_board()


white_turn = True

for i in range(30):
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

    chess_board.print_board()
    print(' ')

    print(pieces[0].possible_moves(chess_board))
    print(pieces[1].possible_moves(chess_board))

    if len(pieces[0].possible_moves(chess_board)) == 0:
        print('White wins')
        break

    white_turn = not white_turn
