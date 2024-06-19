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

#print()

#hess_board.remeve_piece(pieces[0].get_position())

#pieces[1].print_my_board()


# Show possible moves for the king and the rook
for piece in pieces:
    print(piece.possible_moves(chess_board))


for piece in pieces:
    print(piece.get_position()) 
