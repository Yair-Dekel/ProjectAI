from piece import Piece

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
            return None, 1000
        
        x_b_king, y_b_king = black_king.position
        x_w_king, y_w_king = white_king.position
        x_pawn, y_pawn = self.position

        # check if the pawn cannot be captured by the king by no means
        if x_pawn < x_b_king and x_pawn > 0 and (x_pawn - 1, y_pawn) in moves:
            return (x_pawn - 1, y_pawn), 0
        if (y_b_king < y_pawn - x_pawn - 1 or y_b_king > y_pawn + x_pawn + 1) and (x_pawn - 1, y_pawn) in moves:
            return (x_pawn - 1, y_pawn), 0

        cost = {}
        defence_value = 2
        threat_value = 16
        initial_cost = 2
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
            if min(abs(x-x_b_king), abs(y-y_b_king)) <= min(abs(x-x_w_king), abs(y-y_w_king)):
                cost[move] += threat_value

        return min(cost, key=cost.get), cost[min(cost, key=cost.get)]


    def __str__(self):
        return 'P' if self.color == 'white' else 'p'
