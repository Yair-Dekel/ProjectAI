from piece import Piece
import json
STAY_IN_PLACE = 16
BESIDE_PAWN = 0
PAWM_PROTECTED = 3
OPOSITION = 9
OPOSITION_SCORE = 2
PROTECT_PATH = 6

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
        x_king, y_king = self.position

        # remove the moves that are not possible for the king because of the pawn
        if (x_pawn - 1, y_pawn - 1) in moves:
            moves.remove((x_pawn - 1, y_pawn - 1))
        if (x_pawn - 1, y_pawn + 1) in moves:
            moves.remove((x_pawn - 1, y_pawn + 1))
        
        # remove the moves that are not possible for the king because of the white king
        moves = [move for move in moves if move not in king_moves]
        score = {}

        # if pawn position is in king_movse, remove it
        if pawn.position in king_moves:
            king_moves.remove(pawn.position)

        # eat the pawn if possible
        if pawn.position in moves:
            return pawn.position, 0
        
        # if the pawn and the w_king is in the edge, and b_king between them, take the oposition to the w_king
        if x_w_king + 1 == self.position[0] and self.position[0] + 1 == x_pawn and abs(self.position[1] - y_pawn) == 2 and abs(self.position[1] - y_w_king) == 2 and (self.position[0] -1, self.position[1]) in moves:
            return (self.position[0] - 1, self.position[1]), 0
        
        '''if x_king == 0 and x_king + 3 == x_w_king and abs(y_pawn - y_w_king) == 2 and (x_king + 1, ((y_pawn + y_w_king)/2)) in moves:
            return (x_king + 1, int((y_pawn + y_w_king)/2)), 0'''
        
        if y_w_king + 1 == y_king and y_king + 1 == y_pawn and x_king + 2 == x_w_king and x_w_king + 2 == x_pawn and (x_king + 1, y_king + 1) in moves:
            return (x_king + 1, y_king + 1), 0
        
        if x_pawn != 6 and (x_pawn, y_pawn - 1) in moves and not (x_w_king == x_pawn + 1 and y_w_king == y_pawn +1):
            return (x_pawn, y_pawn - 1), 0
        
        if (x_pawn - 2, y_pawn) in moves:
            return (x_pawn - 2, y_pawn), 0
        
        if x_pawn == x_w_king and abs(y_pawn - y_w_king) == 2 and (x_pawn - 4, int((y_pawn + y_w_king)/2)) in moves:
            return (x_pawn - 4, (y_pawn + y_w_king)/2), 0
        
        for move in moves:
            x, y = move
            # distance from above the pawn
            score[move] = (x - (x_pawn - 1)) ** 2 + (y - y_pawn) ** 2 

            # if the pawn is in his first row he can move 2 steps
            if x_pawn == 6:
                score[move] = (x - (x_pawn - 2)) ** 2 + (y - y_pawn) ** 2

            '''# if the w_king is far away from the pawn, the b_king get closer to the pawn
            if max(abs(x_pawn - x_w_king), abs(y_pawn - y_w_king)) > max(abs(x_pawn - x), abs(y_pawn - y)):
                score[move] = (x - (x_pawn)) ** 2 + (y - y_pawn) ** 2'''
            # if the next move of the white king it took the opposition, then not go to there, (if the pawn is not there...)
            if x + 3 == x_w_king and abs(y - y_w_king) <= 1 and abs(x - x_pawn) >=2 and (x_pawn, y_pawn) != (x + 2, y):
                score[move] += 5
            
            if self.position[0] + 4 == x_w_king and x_pawn == x_w_king and (y==y_pawn or y==y_w_king):
                score[move] -= OPOSITION
        

            # king should take the oposition
            if y == y_w_king and x == x_w_king - 2:
                score[move] -= OPOSITION
            
            # king should take the oposition
            if y == y_w_king and x == x_w_king - 4 and self.position[0] != 0:
                score[move] -= OPOSITION

            # king should take the oposition
            if abs(y - y_w_king) == 4 and x == x_w_king - 4:
                score[move] -= OPOSITION_SCORE

            # not giving the oposition to the white king
            if y == y_w_king and x == x_w_king - 3 and x_pawn >= x_w_king:
                score[move] += OPOSITION_SCORE
            if (x + 2, y) in king_moves and x_pawn >= x_w_king:
                score[move] += OPOSITION_SCORE

            # diagonal opposition, but no when the pawn beside the king      
            if abs(y - y_w_king) == 2 and x == x_w_king - 2 and not (abs(y_pawn - y_w_king) == 1 and x_pawn == x_w_king):
                score[move] -= OPOSITION_SCORE
            
            # if the pawn is in the edge, the black king should go to the corner
            if y_pawn == 0 or y_pawn == 7:
                score[move] = (x - 0) ** 2 + (y - y_pawn) ** 2            
            
            # if the black king can capture the pawn
            if max(abs(x_pawn - x_w_king), abs(y_pawn - y_w_king)) > max(abs(x_pawn - x_king), abs(y_pawn - y_king)) and x_pawn != 6:
                score[move] = (x - x_pawn) ** 2 + (y - y_pawn) ** 2

            


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

            # king should take the oposition
            if y == y_b_king and x == x_b_king + 4:
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
        #x_p_move, y_p_move = pawn_best_move

        '''positions = {"x_p_move": x_p_move, "y_p_move": y_p_move, "x_w_king": x_king, "y_w_king": y_king, "x_b_king": x_b_king, "y_b_king": y_b_king,"x_pawn": x_pawn, "y_pawn": y_pawn}

        # Load condition-action plan from JSON file
        with open("plan.json", "r") as file:
            plan = json.load(file)'''
        if ((1, 4) == king.position or king.position == (0,4)) and (1, 6) in moves and y_pawn == 7:
            return "King", (1, 6)

        if ((1, 3) == king.position or king.position == (0,3)) and (1, 1) in moves and y_pawn == 0:
            return "King", (1, 1)

        # promote the pawn unless the black king capture the oposition
        # the pawn not in the edge and y_pawn != 0 and y_pawn != 7
        if pawn_statement == "not defended, can move":
            if not (x_king - 2, y_king) in king_moves:
                # and king not in the corner
                if not (x_b_king == 0 and (y_b_king == 0 or y_b_king == 7)):
                    return "Pawn", pawn_best_move
                # the king in the corner
                elif abs(x_b_king - x_king) == 1 and (x_pawn - 1, y_pawn) in moves:
                    return "King", (x_pawn - 1, y_pawn)
            
        # If the pawn is defended, and the black king far away, promote the pawn unless the pawn above the king
        if pawn_statement == "defended, can move":
            if abs(y_b_king - y_pawn) > 2 and abs(y_b_king - y_king) > 2 and x_pawn >= x_king :
                return "Pawn", pawn_best_move
            # If the pawn is defended, and the black king at the one row before end, promote the pawn.

            # If the pawn still defended after the move, and the black king in row below, promote the pawn.
            if (abs(pawn_best_move[0] - x_king) <= 1 and abs(pawn_best_move[1] - y_king) <= 1) and (x_b_king >= x_pawn or (x_b_king <= 1 and x_pawn <= 2)):
                return "Pawn", pawn_best_move
        
        if pawn_statement == "black king in the corner, king should move back":
            moves = [move for move in moves if move[0] > x_king]
            
        # If the pawn and the king beside each other, the king should go above the pawn, unless the black king capture the oposition or the pawn is in the edge
        if x_pawn == x_king and abs(y_pawn - y_king) <= 1 and (x_pawn - 1, y_pawn) in moves and not (x_pawn - 3, y_pawn) in king_moves and y_pawn != 0 and y_pawn != 7:
            return "King", (x_pawn - 1, y_pawn)
        
        # king should go beneath the pawn
        if abs(y_pawn - y_b_king) == 2 and x_pawn == x_b_king and y_king == (y_pawn + y_b_king)/2 and (x_pawn + 1, y_pawn) in moves:
            return "King", (x_pawn + 1, y_pawn)
        
        # king should go up
        if (y_pawn == 0 or y_pawn == 7) and abs(y_pawn - y_king) <= 1 and 0 < x_b_king < x_king and (x_king - 1, y_king) in moves:
            return "King", (x_king - 1, y_king)

        distance_from_pawn_side = min(abs(x_king - (x_pawn-1)) + abs(y_king - (y_pawn-1)), abs(x_king - (x_pawn-1)) + abs(y_king - (y_pawn+1)))

        if ((self.position == (1, 1) and y_pawn == 0) or (self.position == (1, 6) and y_pawn == 7)) and pawn_best_move:
            return "Pawn", pawn_best_move
            

        score = {}
        for move in moves:
            x, y = move
            
            score[move] = min(abs(x - (x_pawn-1)) + abs(y - y_pawn - 1), abs(x - (x_pawn-1)) + abs(y - y_pawn + 1))


            if abs(x - x_pawn) <= 1 and abs(y - y_pawn) <= 1 and x_king == x_pawn:
                score[move] -= pawn_protected

            # King should stay in place
            if distance_from_pawn_side == 0:
                score[move] += STAY_IN_PLACE
            # If king comes beside the pawn
            if abs(x-x_pawn) <= 1 and abs(y-y_pawn) <= 1:
                score[move] -= BESIDE_PAWN
            
            # King should take the opposition
            if y == y_b_king and x == x_b_king + 2:
                score[move] -= OPOSITION_SCORE
            
            # if the king below the pawn go to more distant place
            if x_pawn < x_king and y_pawn == y_king and abs(x_pawn - x) <= 1:
                score[move] -= abs(y - y_b_king)
                
            # If the king is beside the pawn and above it, and protects 3 slots
            if abs(y-y_pawn) == 1 and 0 < x < x_pawn - 1 and not (abs(y_king - y_pawn) == 1 and x_king < x_pawn - 1 and x_king > 0):
                # The black king is not beside the pawn
                if not (abs(x_b_king - x_pawn) <= 1 and abs(y_b_king - y_pawn) <= 1) and not (y_b_king == y):
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
