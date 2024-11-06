# first player : king 
# secound player : king + rook + rook

import copy

from rx.subject import Subject

class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.state_changed = Subject()  # Observable subject for state changes
        self.layers = self.make_layers()

    def make_layers(self):
        layers = []
        first_layer = [(3, 3), (3, 4), (4, 3), (4, 4)]
        layers.append(first_layer)
        second_layer = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
        layers.append(second_layer)
        third_layer = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 1), (2, 6), (3, 1), (3, 6), (4, 1), (4, 6), (5, 1), (5, 6), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]
        layers.append(third_layer)
        fourth_layer = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 7), (2, 0), (2, 7), (3, 0), (3, 7), (4, 0), (4, 7), (5, 0), (5, 7), (6, 0), (6, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]
        layers.append(fourth_layer)
        return layers

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
        if self.board[nx][ny] != ' ':
            self.remeve_piece(new_position)
        self.board[nx][ny] = piece
        piece.position = new_position
        self.state_changed.on_next(self)


    def get_piece_at(self, position):
        x, y = position
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None


    def remeve_piece(self, position):
        x, y = position
        self.board[x][y] = ' '
        for piece in self.pieces:
            if piece.position == position:
                self.pieces.remove(piece)
                break


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
    
    def pseudo_copy(self):
        # Create a new board instance
        new_board = Board()
        
        # Shallow copy the board (2D array of positions)
        new_board.board = [row[:] for row in self.board]
        
        # Shallow copy the pieces (assuming pieces can be shallow copied)
        #new_board.pieces = self.pieces[:]  # No deep copy of pieces, just copying references
        for piece in self.pieces:
            new_board.pieces.append(piece.pseudo_copy(new_board))
        
        # Shallow copy the layers
        new_board.layers = self.layers[:]
        
        # Do not copy the `state_changed` subject
        new_board.state_changed = Subject()  # Reinitialize a fresh Subject

        return new_board
    
    def is_in_check(self, color):
        king_position = self.get_king(color)
        for piece in self.pieces:
            if piece.color != color:
                if king_position in piece.possible_moves(self):
                    return True
        return False
    
    def is_in_checkmate(self, color):
        king_position = self.get_king(color)
        king = self.get_piece_at(king_position)
        if not self.is_in_check(color):
            return False
        possible_moves = king.possible_moves(self)
        possible_moves.append(king_position)

        threaten_places = []

        for piece in self.pieces:
            if piece.color != color:
                if hasattr(piece, 'threat_places'):
                    threaten_places.extend(piece.threat_places(self))
                elif hasattr(piece, 'possible_moves'):
                    threaten_places.extend(piece.possible_moves(self))
        return all(move in threaten_places for move in possible_moves)     # Check if every move in possible_moves is in threaten_moves



