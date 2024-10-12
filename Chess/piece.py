from board import Board
from rx import operators as ops

class Piece:
    def __init__(self, color, type, board):
        self.color = color
        self.position = None
        self.type = type
        self.board = board
        self.subscribe_to_board()

    def subscribe_to_board(self):
        self.board.state_changed.pipe(
            ops.map(lambda board: self.update(board))
        ).subscribe()

    def update(self, board):
        self.board = board       
        

    def print_my_board(self):
        for row in self.board.board:
            print(' '.join([str(piece) if piece != ' ' else '.' for piece in row]))
        print()
        
        
    def get_position(self):
        return self.position
    
    def possible_moves(self, board):
        raise NotImplementedError

    # Copy constructor method
    def copy(self):
        new_piece = Piece(self.color, self.type, self.board)
        new_piece.position = self.position  # Assuming position is a simple tuple, otherwise use copy.deepcopy
        return new_piece
    
    def __str__(self):
        raise NotImplementedError
