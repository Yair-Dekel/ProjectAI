from piece import Piece
STAY_IN_PLACE = 16
BESIDE_PAWN = 0
PAWM_PROTECTED = 0
OPOSITION = 3
OPOSITION_SCORE = 2
PROTECT_PATH = 5

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
        x_w_king, y_w_king = king.position

        # remove the moves that are not possible for the king because of the pawn
        if (x_pawn - 1, y_pawn - 1) in moves:
            moves.remove((x_pawn - 1, y_pawn - 1))
        if (x_pawn - 1, y_pawn + 1) in moves:
            moves.remove((x_pawn - 1, y_pawn + 1))
        
        # remove the moves that are not possible for the king because of the white king
        moves = [move for move in moves if move not in king_moves]
        score = {}

        # eat the pawn if possible
        if pawn.position in moves:
            return pawn.position, 0
        
        for move in moves:
            x, y = move
            # distance from above the pawn
            score[move] = (x - (x_pawn - 1)) ** 2 + (y - y_pawn) ** 2

            # king should take the oposition
            if y == y_w_king and x == x_w_king -2:
                score[move] -= OPOSITION
        
        # if moves is empty, throw an exception
        if not score:
            raise Exception("No possible moves")

        return min(score, key=score.get), 0
    
    def objective_function_white(self):
        pawn_protected = PAWM_PROTECTED
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
            pawn_protected = 3

        x_b_king, y_b_king = king.position
        x_pawn, y_pawn = pawn.position
        x_king, y_king = self.position

        distance_from_pawn_side = min(abs(x_king - x_pawn)+abs(y_king - (y_pawn-1)), abs(x_king - x_pawn)+abs(y_king - (y_pawn+1)))

        score = {}
        for move in moves:
            x, y = move
            
            score[move] = min(abs(x - x_pawn) + abs(y - y_pawn - 1), abs(x - x_pawn) + abs(y - y_pawn + 1))
            score[move] += pawn_protected

            # king should stay in place
            if distance_from_pawn_side == 0:
                score[move] += STAY_IN_PLACE
            # if king comes beside the pawn
            if abs(x-x_pawn) <= 1 and abs(y-y_pawn) <= 1:
                score[move] -= BESIDE_PAWN
            
            # king should take the oposition
            if y == y_b_king and x == x_b_king + 2:
                score[move] -= OPOSITION_SCORE
                
            # if the king is beside the pawn and above the pawn, and the king protect 3 slots
            if abs(y-y_pawn) == 1 and x < x_pawn - 1 and x > 0 and not (abs(y_king-y_pawn) == 1 and x_king < x_pawn - 1 and x_king > 0):
                # the black king is not beside the pawn
                if not (abs(x_b_king - x_pawn) <= 1 and abs(y_b_king - y_pawn) <= 1):
                    # count the slots the king keeps from the black king
                    score[move] -= PROTECT_PATH

                

        return min(score, key=score.get), min(score.values())
    
    def objective_function_white2(self):
        pawn_protected = PAWM_PROTECTED
        for piece in self.board.pieces:
            if piece.type == "Pawn":
                pawn = piece
            if piece.type == "King" and piece.color == "black":
                king = piece
        
        pawn_statement, pawn_best_move = pawn.objective_function3()
        
        # If the pawn must move, return its move
        if "must move on" in pawn_statement:
            return "Pawn", pawn_best_move
        
        pawn_moves = pawn.possible_moves(self.board)
        king_moves = king.possible_moves2() 
        moves = self.possible_moves2()
        
        # Remove the moves that are not possible for the king
        moves = [move for move in moves if move not in king_moves]
        if pawn.position in moves:
            moves.remove(pawn.position)

        x_b_king, y_b_king = king.position
        x_pawn, y_pawn = pawn.position
        x_king, y_king = self.position

        # promote the pawn unless the black king capture the oposition
        if pawn_statement == "not defended, can move":
            if not (x_king - 2, y_king) in king_moves:
                return "Pawn", pawn_best_move
            
        # If the pawn is defended, and the black king far away, promote the pawn unless the pawn above the king
        if pawn_statement == "defended, can move":
            if abs(y_b_king - y_pawn) > 2 and abs(y_b_king - y_king) > 2 and x_pawn >= x_king:
                return "Pawn", pawn_best_move
            # If the pawn is defended, and the black king at the one row before end, promote the pawn.

            # If the pawn still defended after the move, and the black king in row below, promote the pawn.
            if (abs(pawn_best_move[0] - x_king) <= 1 and abs(pawn_best_move[1] - y_king) <= 1) and (x_b_king >= x_pawn or (x_b_king <= 1 and x_pawn <= 2)):
                return "Pawn", pawn_best_move

        distance_from_pawn_side = min(abs(x_king - (x_pawn-1)) + abs(y_king - (y_pawn-1)), abs(x_king - (x_pawn-1)) + abs(y_king - (y_pawn+1)))

        score = {}
        for move in moves:
            x, y = move
            
            score[move] = min(abs(x - (x_pawn-1)) + abs(y - y_pawn - 1), abs(x - (x_pawn-1)) + abs(y - y_pawn + 1))
            score[move] += pawn_protected

            # King should stay in place
            if distance_from_pawn_side == 0:
                score[move] += STAY_IN_PLACE
            # If king comes beside the pawn
            if abs(x-x_pawn) <= 1 and abs(y-y_pawn) <= 1:
                score[move] -= BESIDE_PAWN
            
            # King should take the opposition
            if y == y_b_king and x == x_b_king + 2:
                score[move] -= OPOSITION_SCORE
                
            # If the king is beside the pawn and above it, and protects 3 slots
            if abs(y-y_pawn) == 1 and x < x_pawn - 1 and x > 0 and not (abs(y_king-y_pawn) == 1 and x_king < x_pawn - 1 and x_king > 0):
                # The black king is not beside the pawn
                if not (abs(x_b_king - x_pawn) <= 1 and abs(y_b_king - y_pawn) <= 1):
                    # Count the slots the king keeps from the black king
                    score[move] -= PROTECT_PATH
        if score:
            best_king_move = min(score, key=score.get)
            best_king_score = min(score.values())
        else:
            best_king_move = None
            best_king_score = None

        return "King", best_king_move
        '''else:
        # If the king can move to defend the pawn, prioritize that
        if abs(best_king_move[0] - x_pawn) <= 1 and abs(best_king_move[1] - y_pawn) <= 1:
            return "King", best_king_move
        # Otherwise, consider moving the pawn if possible
        return "Pawn", pawn_best_move'''


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
