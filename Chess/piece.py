class Piece:
    def __init__(self, color, type):
        self.color = color
        self.position = None
        self.type = type
    

    def get_position(self):
        return self.position
    
    def possible_moves(self, board):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError
