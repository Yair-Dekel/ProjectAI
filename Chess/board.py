# first player : king 
# secound player : king + tour 


import matplotlib.pyplot as plt
import numpy as np

class Board:
    def __init__(self):
        self.board = self.init_board()

    def init_board(self):
        # Initialize the board with the initial positions of the pieces
        board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  # Black pieces
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Black pawns
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty squares
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # White pawns
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   # White pieces
        ]
        return board

    def display_board(self):
        # Display the board in a readable format
        for row in self.board:
            print(' '.join(row))



# Example usage
chess_board = Board()
chess_board.display_board()
