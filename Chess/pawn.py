from piece import Piece
DEFENCE_VALUE = 2
THREAT_VALUE = 16
INITIAL_COST = 2
MAX_RETURN = 1000

class Pawn(Piece):

    def print_piece(self):
        print(f'{self.color} Pawn at {self.position}')
    
    def possible_moves(self, board):
        x, y = self.position
        moves = []
        
        if self.color == 'white' and x < 7 and x > 0:
            if x == 6:
                if board.check_empty((x - 1, y)):
                    moves.append((x - 1, y))
                    if board.check_empty((x - 2, y)):
                        moves.append((x - 2, y))
            else:
                if board.check_empty((x - 1, y)):
                    moves.append((x - 1, y))
            if y > 0:
                if not board.check_empty((x - 1, y - 1)):
                    if board.get_piece_at((x - 1, y - 1)).color != self.color:
                        moves.append((x - 1, y - 1))
            if y < 7:
                if not board.check_empty((x - 1, y + 1)):
                    if board.get_piece_at((x - 1, y + 1)).color != self.color:
                        moves.append((x - 1, y + 1))
            
        else:
            if x < 7 and x > 0:
                if x == 1:
                    if board.check_empty((x + 1, y)):
                        moves.append((x + 1, y))
                        if board.check_empty((x + 2, y)):
                            moves.append((x + 2, y))
                else:
                    if board.check_empty((x + 1, y)):
                        moves.append((x + 1, y))
                if y > 0:
                    if not board.check_empty((x + 1, y - 1)):
                        if board.get_piece_at((x + 1, y - 1)).color != self.color:
                            moves.append((x + 1, y - 1))
                if y < 7:
                    if not board.check_empty((x + 1, y + 1)):
                        if board.get_piece_at((x + 1, y + 1)).color != self.color:
                            moves.append((x + 1, y + 1))
                
        return moves
    
    def objective_function(self):
        for piece in self.board.pieces:
            if piece.type == "King" and piece.color != self.color:
                black_king = piece
            if piece.type == "King" and piece.color == self.color:
                white_king = piece
        black_king_moves = black_king.possible_moves(self.board)
        white_king_moves = white_king.possible_moves(self.board)
        moves = self.possible_moves(self.board)
        if len(moves) == 0:
            return None, MAX_RETURN
        
        x_b_king, y_b_king = black_king.position
        x_w_king, y_w_king = white_king.position
        x_pawn, y_pawn = self.position

        # check if the pawn cannot be captured by the king by no means
        if x_pawn < x_b_king and x_pawn > 0 and (x_pawn - 1, y_pawn) in moves:
            return (x_pawn - 1, y_pawn), 0
        if (y_b_king < y_pawn - x_pawn - 1 or y_b_king > y_pawn + x_pawn + 1) and (x_pawn - 1, y_pawn) in moves:
            return (x_pawn - 1, y_pawn), 0

        cost = {}
        defence_value = DEFENCE_VALUE
        threat_value = THREAT_VALUE
        initial_cost = INITIAL_COST
        move_away_value = 8
        for move in moves:
            x, y = move
            cost[move] = initial_cost
            #if move in white_king_moves:
            #    cost[move] -= defence_value
            #if move in black_king_moves:
            #    cost[move] += threat_value
            #if abs(x - x_king) + abs(y - y_king) > abs(x_pawn - x_king) + abs(y_pawn - y_king):
            #    cost[move] -= move_away_value
            if abs(x-x_w_king) <= 1 and abs(y-y_w_king) <= 1:
                cost[move] -= defence_value
            elif max(abs(x-x_b_king), abs(y-y_b_king)) < max(abs(x-x_w_king), abs(y-y_w_king)):
                cost[move] += threat_value

        return min(cost, key=cost.get), cost[min(cost, key=cost.get)]

    def objective_function2(self):
        for piece in self.board.pieces:
            if piece.type == "King" and piece.color != self.color:
                black_king = piece
            if piece.type == "King" and piece.color == self.color:
                white_king = piece

        black_king_moves = black_king.possible_moves(self.board)
        white_king_moves = white_king.possible_moves(self.board)
        moves = self.possible_moves(self.board)
        if len(moves) == 0:
            return None, MAX_RETURN

        x_b_king, y_b_king = black_king.position
        x_w_king, y_w_king = white_king.position
        x_pawn, y_pawn = self.position

        cost = {}
        defence_value = DEFENCE_VALUE
        threat_value = THREAT_VALUE
        initial_cost = INITIAL_COST
        move_away_value = 8
        waiting_bonus = 15  # Increased: Stronger reward for waiting
        protected_bonus = 10  # Increased: White king should be close
        danger_penalty = 20  # New: Penalize unsafe advances

        for move in moves:
            x, y = move
            cost[move] = initial_cost

            # 1. **Encourage Waiting if Black King is Far Away**
            distance_to_black_king = abs(x_b_king - x_pawn) + abs(y_b_king - y_pawn)
            if distance_to_black_king > 3:  # If black king is far, waiting is better
                cost[move] -= waiting_bonus

            # 2. **Discourage Advancing if White King is Not Close**
            distance_to_white_king = abs(x_w_king - x) + abs(y_w_king - y)
            if distance_to_white_king > 2:
                cost[move] += danger_penalty  # Moving is bad if White king is not nearby

            # 3. **Discourage Advancing if It Creates Vulnerability**
            if move in black_king_moves and move not in white_king_moves:
                cost[move] += danger_penalty

            # 4. **Reward Moves that Bring Pawn Closer to the White King**
            if abs(x - x_w_king) + abs(y - y_w_king) < abs(x_pawn - x_w_king) + abs(y_pawn - y_w_king):
                cost[move] -= protected_bonus

        return min(cost, key=cost.get), cost[min(cost, key=cost.get)]

    def objective_function3(self):
        for piece in self.board.pieces:
            if piece.type == "King" and piece.color != self.color:
                black_king = piece
            if piece.type == "King" and piece.color == self.color:
                white_king = piece

        moves = self.possible_moves(self.board)

        if len(moves) == 0:
            return "can't move", None
        
        x_b_king, y_b_king = black_king.position
        x_w_king, y_w_king = white_king.position
        x_pawn, y_pawn = self.position        

        # check if the pawn cannot be captured by the king by no means
        if moves[-1][0]+1 < x_b_king and x_pawn > 0 and (x_pawn - 1, y_pawn) in moves:
            return "must move on", moves[-1]
        if (y_b_king < y_pawn - (moves[-1][0] + 1) or y_b_king > y_pawn + moves[-1][0]+1):
            return "must move on", moves[-1]
        
        '''if moves[-1][0] < x_b_king and abs(moves[-1][1] - y_b_king) > 1:
            return "must move on", moves[-1]'''

        
        # the pawn shouldn't pass the king unless it in the last rows
        if x_pawn <= x_w_king and x_pawn > 2:
            return "pass the king, can't move", moves[0]

        # the pawn next to the king
        if abs(x_pawn - x_w_king) <= 1 and abs(y_pawn - y_w_king) <= 1:
            return "defended, can move", moves[-1]
        
        # the pawn not next to the king
        else:
            # the panw can advance to be next to the king
            if abs(moves[0][0] - x_w_king) <= 1 and abs(moves[0][1] - y_w_king) <= 1:
                title = "not defended, can move"
                next_move = moves[0]
            
            # not next to the king and can't move next to the king
            # the pawn should move on if it in the columns next to the king, and the white king is above the black king (or in the same row)
            elif abs(y_pawn - y_w_king) <= 1 and x_b_king <= x_w_king:
                return "must move on", moves[0]
            
            # if the white king between the black king and the pawn, the pawn should move on
            elif (y_pawn < y_w_king - 1 and y_w_king + 1 < y_b_king) or (y_pawn > y_w_king + 1 and y_w_king - 1 > y_b_king):
                return "must move on", moves[-1]    # advance as much as possible
            
            else:
                title = "not defended, can't move"
                next_move = moves[0]
            return title, next_move

    def __str__(self):
        return 'P' if self.color == 'white' else 'p'
