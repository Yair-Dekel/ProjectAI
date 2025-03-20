import tkinter as tk
from tkinter import Canvas

class ChessGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.cell_size = 60
        self.canvas = Canvas(root, width=8*self.cell_size, height=8*self.cell_size)
        self.canvas.pack()
        self.draw_board()
        self.update_pieces()
        
        # Subscribe to board changes
        self.board.state_changed.subscribe(lambda _: self.update_pieces())
    
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = "#DDB88C" if (row + col) % 2 == 0 else "#A66D4F"
                self.canvas.create_rectangle(
                    col * self.cell_size, row * self.cell_size,
                    (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                    fill=color, outline="black"
                )
    
    def update_pieces(self):
        self.canvas.delete("pieces")
        for piece in self.board.pieces:
            x, y = piece.position
            symbol = "♔" if piece.type == "King" and piece.color == "white" else \
                     "♚" if piece.type == "King" and piece.color == "black" else "♙"
            self.canvas.create_text(
                y * self.cell_size + self.cell_size // 2,
                x * self.cell_size + self.cell_size // 2,
                text=symbol, font=("Arial", 32), tags="pieces"
            )
