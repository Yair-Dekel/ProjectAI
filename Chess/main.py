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
for piece in pieces:
    position = (random.randint(0, 7), random.randint(0, 7))
    while not chess_board.check_empty(position):
        position = (random.randint(0, 7), random.randint(0, 7)) 
    chess_board.add_piece(piece, position)


# Print the initial board setup
chess_board.print_board()

for piece in pieces:
    print(piece.position)

print(' ')

#hess_board.remeve_piece(pieces[0].get_position())

#pieces[1].print_my_board()

# get the best move for the white (by the objective functions)

rook1_move, rook1_value = pieces[2].objective_function()
rook2_move, rook2_value = pieces[3].objective_function()
white_king_move, white_king_value = pieces[1].objective_function()

for piece in pieces:
    print(piece.position)

# move the pieces with the highest value
if rook1_value >= rook2_value and rook1_value >= white_king_value:
    chess_board.move_piece(pieces[2], rook1_move)
elif rook2_value >= rook1_value and rook2_value >= white_king_value:
    chess_board.move_piece(pieces[3], rook2_move)
else:
    chess_board.move_piece(pieces[1], white_king_move)

chess_board.print_board()


# Show possible moves for the king and the rook
for piece in pieces:
    print(piece.position)



