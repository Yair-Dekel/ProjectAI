
from piece import Piece
import math

class Rook(Piece):

    def search_for_king(self):
        oposite_color = 'black' if self.color == 'white' else 'white'
        return self.board.get_king(oposite_color)
        


    def objective_function(self):
        moves = self.possible_moves(self.board)
        king_position = self.search_for_king(moves)
        
        check = False
        checkmate = False
        blocking_way = False
        too_close = False
        check_value = 10


        objective = {}

        for move in moves:
            objective[move] = 0


        king_x ,king_y = king_position


        for move in moves:
            x, y = move
            distance = 0
            
            #-------------------set the parameters-------------------
            if ((x == king_x) and (y == king_y)):
                checkmate = True

            elif ((x == king_x) or (y == king_y)):
                check = True
                if (abs(x-king_x) == 1) or (abs(y-king_y) == 1):
                    too_close = True                
                
                if (x == king_x):
                    distance = abs(x - king_x)
                elif (y == king_y):
                    distance = abs(y - king_y)
                
            if ((x == (king_x+1)) or (x == (king_x-1)) or 
                (y == (king_y+1)) or (y == (king_y-1))):
                blocking_way = True

            if (abs(x-king_x) == 1) and (abs(y-king_y) == 1):
                too_close = True
            
            #------------------- evaluate the objective-------------------
            # i upload the changes to the GIT

            if checkmate:
                objective[move] = float('inf')
            else:
                if check:
                    objective[move] += check_value
                
                objective[move] += distance
                
                if too_close:
                    objective[move] = 0

        
        

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
