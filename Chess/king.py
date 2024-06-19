from piece import Piece

class King(Piece):
    def possible_moves(self, board):
        x, y = self.position
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board.get_piece_at((nx, ny))
                    if target == ' ' or target.color != self.color:
                        moves.append((nx, ny))
        return moves

    
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'
