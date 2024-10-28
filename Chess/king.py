from piece import Piece

class King(Piece):
    
    def print_piece(self):
        print(f'{self.color} King at {self.position}')
    
    def possible_moves(self, board):
        x, y = self.position
        moves = []
        impossible_moves = []

        # Collect all impossible moves (attacked squares) from enemy pieces
        for piece in board.pieces:
            if piece.color != self.color:
                if piece.type == "King":
                    # For the enemy king, consider its possible moves but exclude adjacent squares
                    enemy_king_moves = []
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            ex, ey = piece.position
                            nx, ny = ex + dx, ey + dy
                            if 0 <= nx < 8 and 0 <= ny < 8:
                                enemy_king_moves.append((nx, ny))
                    impossible_moves.extend(enemy_king_moves)
                else:
                    # For other enemy pieces, collect their possible moves
                    for move in piece.possible_moves(board):
                        impossible_moves.append(move)
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < 8 and 0 <= ny < 8:

                    target = board.get_piece_at((nx, ny))
                    if target == None or target.color != self.color:

                        moves.append((nx, ny))
        
        moves = [move for move in moves if move not in impossible_moves]
        

        return moves
    
    def objective_function(self):
        layers = self.board.make_layers().copy()
        moves = self.possible_moves(self.board)

        layers = [[position for position in layer if position in moves] for layer in layers]

        print(f'after: {layers}')
        
        #return random move in the minimal layer
        for layer in layers:
            if layer:
                #random choose
                return layer[0], 0

    
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'
