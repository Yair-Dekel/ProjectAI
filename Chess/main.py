from board import Board
from king import King
from rook import Rook
import random

# Create a new board
chess_board = Board()

pieces = []
# Create a white king and a white rook
pieces.append(King('black', "King"))
pieces.append(King('white', "King"))
pieces.append(Rook('white', "Rook"))
pieces.append(Rook('white', "Rook"))


# Place the king and rook on the board
for piece in pieces:
    position = (random.randint(0, 7), random.randint(0, 7))
    while not chess_board.check_empty(position):
        position = (random.randint(0, 7), random.randint(0, 7)) 
    chess_board.add_piece(piece, position)


# Print the initial board setup
chess_board.print_board()

# Show possible moves for the king and the rook
for piece in pieces:
    print(piece.possible_moves(chess_board))


for piece in pieces:
    print(piece.get_position()) 
