from piece import Piece

class Pawn(Piece):

    def print_piece(self):
        print(f'{self.color} Pawn at {self.position}')
    
    def possible_moves(self, board):
        x, y = self.position
        moves = []
        
        if self.color == 'white':
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
        moves = self.possible_moves(self.board)
        if len(moves) == 0:
            return None, -1
        
        best_move = moves[0]
        best_value = -1

        for move in moves:
            new_board = self.board.pseudo_copy()
            new_board.move_piece(self, move)
            value = self.evaluate_board(new_board)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move, best_value
