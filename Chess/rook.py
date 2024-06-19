
from piece import Piece

class Rook(Piece):

    def objective_function(self):
        moves = self.possible_moves(self.board)
           
    

    def possible_moves(self, board):
        x, y = self.position
        moves = []
        # Vertical and horizontal moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target == ' ':
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy

        return moves

    def __str__(self):
        return 'R' if self.color == 'white' else 'r'
