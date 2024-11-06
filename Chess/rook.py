
from piece import Piece
import math
import copy

class Rook(Piece):

    def search_for_king(self):
        oposite_color = 'black' if self.color == 'white' else 'white'
        return self.board.get_king(oposite_color)
        


    def objective_function(self):
        moves = self.possible_moves(self.board)
        king_position = self.search_for_king()

        layers = self.board.make_layers()
        layer_of_king = self.find_king_layer(king_position, layers)
        
        check = False
        checkmate = False
        blocking_way = False
        too_close = False
        check_value = 1

        king_x ,king_y = king_position
        objective = {}

        for move in moves:
            if abs(king_x - self.position[0]) == 1 and abs(king_y - self.position[1]) == 1:
                objective[move] = 500
            else:
                objective[move] = 0


        
        # if the king threating the rook
        


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

            if checkmate:
                objective[move] = float('inf')
            else:
                if check:
                    objective[move] += check_value
                
                objective[move] += distance
                
                if too_close:
                    objective[move] = 0

            
            new_board = self.board.pseudo_copy()
            new_rook = new_board.get_piece_at(self.position)

            #new_rook = copy.deepcopy(new_board.get_piece_at(self.position))

            new_board.move_piece(new_rook, move)

            minimal_king_layer = new_rook.search_minimal_king_layer(new_board, layers)
            if minimal_king_layer is not None:
                if minimal_king_layer > layer_of_king:
                    objective[move] += 200
                elif minimal_king_layer == layer_of_king:
                    objective[move] += 5
                else:
                    objective[move] -= 5
            if new_board.is_in_checkmate(self.color):
                objective[move] += 1000

        #return the move with the highest objective value
        return max(objective, key=objective.get), objective[max(objective, key=objective.get)]

   
    def objective_function2(self, board):
        layers = self.board.make_layers()
        king_position = self.search_for_king()
        layer_of_king = self.find_king_layer(king_position, layers)
        moves = self.possible_moves(board)
        
        objective = {}

        for move in moves:
            new_board = board.copy()
            new_board.move_piece(self, move)
            minimal_king_layer = self.search_minimal_king_layer(new_board, layers)
            if minimal_king_layer is not None:
                if minimal_king_layer > layer_of_king:
                    objective[move] = 1
                else:
                    objective[move] = 0
            else:
                objective[move] = 0


    def search_minimal_king_layer(self, board, layers):
        king = board.get_piece_at(self.search_for_king())
        possible_moves = king.possible_moves(board)

        minimal_layer = math.inf
        for move in possible_moves:
            for i, layer in enumerate(layers):
                if move in layer:
                    if i < minimal_layer:
                        minimal_layer = i
        
        return minimal_layer if minimal_layer != math.inf else None



    def find_king_layer(self, king_position, layers):
        for i, layer in enumerate(layers):
            if king_position in layer:
                return i    

    def possible_moves(self, board):
        x, y = self.position
        moves = []
        # Vertical and horizontal moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target == None:
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy

        return moves
    
    def threat_places(self, board):
        x, y = self.position
        moves = []
        # Vertical and horizontal moves
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target == None:
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    if target.type != "King":
                        break
                else:
                    break
                nx, ny = nx + dx, ny + dy

        return moves
    
    

    def __str__(self):
        return 'R' if self.color == 'white' else 'r'
