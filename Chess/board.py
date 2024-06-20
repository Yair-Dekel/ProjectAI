# first player : king 
# secound player : king + rook + rook

from rx.subject import Subject

class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.state_changed = Subject()  # Observable subject for state changes

    def get_king(self, color):
        for piece in self.pieces:
            if  piece.type == "King": 
                if piece.color == color:
                    return piece.position

             

    def add_piece(self, piece, position):
        x, y = position
        if self.check_empty(position):
            self.board[x][y] = piece
            self.pieces.append(piece)
            piece.position = position
            self.state_changed.on_next(self)
        else:
            return False


    def move_piece(self, piece, new_position):
        x, y = piece.position
        self.board[x][y] = ' '
        nx, ny = new_position
        self.board[nx][ny] = piece
        piece.position = new_position
        self.state_changed.on_next(self)


    def get_piece_at(self, position):
        x, y = position
        return self.board[x][y]


    def remeve_piece(self, position):
        x, y = position
        self.board[x][y] = ' '


    def print_board(self):
        for row in self.board:
            print(' '.join([str(piece) if piece != ' ' else '.' for piece in row]))
        print()

    def check_empty(self, position):
        x, y = position
        if self.board[x][y] == ' ':
            return True
        else:
            return False


