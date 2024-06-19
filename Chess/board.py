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


    
    def display_board_graphically(self):
        fig, ax = plt.subplots()
        ax.set_xticks(np.arange(8) + 0.5, minor=False)
        ax.set_yticks(np.arange(8) + 0.5, minor=False)
        ax.invert_yaxis()
        ax.xaxis.tick_top()

        board_colors = np.array([[1, 0] * 4, [0, 1] * 4] * 4)
        ax.imshow(board_colors, cmap='gray', interpolation='none')

        piece_to_unicode = {
            'r': '\u265C', 'n': '\u265E', 'b': '\u265D', 'q': '\u265B', 'k': '\u265A', 'p': '\u265F',
            'R': '\u2656', 'N': '\u2658', 'B': '\u2657', 'Q': '\u2655', 'K': '\u2654', 'P': '\u2659'
        }

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != '.':
                    ax.text(j, i, piece_to_unicode[piece], fontsize=24, ha='center', va='center', color='black' if piece.islower() else 'white')

        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.show()

# Example usage
chess_board = Board()
chess_board.display_board()
chess_board.display_board_graphically()


#   pip install matplotlib