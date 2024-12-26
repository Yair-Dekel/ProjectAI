from piece import Piece

class King(Piece):
    
    def print_piece(self):
        print(f'{self.color} King at {self.position}')
    
    def possible_moves(self, board):
        x, y = self.position
        moves = []
        impossible_moves = []

        pieces_positions = []
        for piece in board.pieces:
            if piece.color != self.color:
                pieces_positions.append(piece.get_position())

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
                            if 0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in pieces_positions:
                                enemy_king_moves.append((nx, ny))
                    impossible_moves.extend(enemy_king_moves)
                elif piece.type == "Rook":
                    # For other enemy pieces, collect their possible moves
                    for move in piece.threat_places(board):
                        impossible_moves.append(move)
                elif piece.type == "Pawn":
                    if piece.color == "white":
                        impossible_moves.extend([(piece.position[0] - 1, piece.position[1] - 1), (piece.position[0] - 1, piece.position[1] + 1)])
                    else:
                        impossible_moves.extend([(piece.position[0] + 1, piece.position[1] - 1), (piece.position[0] + 1, piece.position[1] + 1)])
                    
        
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
    
    def possible_moves2(self):
        x, y = self.position
        moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:                
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy                
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
        return moves
    
    def objective_function_black(self):
        for piece in self.board.pieces:
            if piece.type == "Pawn":
                pawn = piece
            if piece.type == "King" and piece.color == "white":
                king = piece
        pawn_moves = pawn.possible_moves(self.board)
        king_moves = king.possible_moves2() 
        moves = self.possible_moves2()
        x_pawn, y_pawn = pawn.position
        if (x_pawn - 1, y_pawn - 1) in moves:
            moves.remove((x_pawn - 1, y_pawn - 1))
        if (x_pawn - 1, y_pawn + 1) in moves:
            moves.remove((x_pawn - 1, y_pawn + 1))
        
        # remove the moves that are not possible for the king
        moves = [move for move in moves if move not in king_moves]
        score = {}
        if pawn.position in moves:
            return pawn.position, 0
        for move in moves:
            x, y = move
            score[move] = (x - x_pawn - 1) ** 2 + (y - y_pawn) ** 2

        return min(score, key=score.get), 0
    
    def objective_function_white(self):
        for piece in self.board.pieces:
            if piece.type == "Pawn":
                pawn = piece
            if piece.type == "King" and piece.color == "black":
                king = piece
        pawn_moves = pawn.possible_moves(self.board)
        king_moves = king.possible_moves2() 
        moves = self.possible_moves2()
        
        # remove the moves that are not possible for the king
        moves = [move for move in moves if move not in king_moves]
        if pawn.position in moves:
            moves.remove(pawn.position)

        x_pawn, y_pawn = pawn.position
        score = {}
        for move in moves:
            x, y = move
            score[move] = min(abs(x - x_pawn) + abs(y - y_pawn - 1), abs(x - x_pawn) + abs(y - y_pawn + 1))

        return min(score, key=score.get), min(score.values())

    def objective_function(self):
        layers = self.board.make_layers().copy()
        moves = self.possible_moves(self.board)

        layers = [[position for position in layer if position in moves] for layer in layers]
        
        #return random move in the minimal layer
        for layer in layers:
            if layer:
                #random choose
                return layer[0], 0

    
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'
