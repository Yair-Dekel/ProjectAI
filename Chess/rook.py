
from piece import Piece
import math
import copy

class Rook(Piece):

    def search_for_king(self):
        oposite_color = 'black' if self.color == 'white' else 'white'
        return self.board.get_king(oposite_color)
        
    '''

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

    '''
   
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

    def objective_function(self):
        moves = self.possible_moves(self.board)
        king_position = self.search_for_king()
        b_king = self.board.get_piece_at(king_position)
        possible_king_moves = b_king.possible_moves(self.board)
            

        layers = self.board.make_layers()
        layer_of_king = self.find_king_layer(king_position, layers)

        threat_places = self.cuurent_threat()
        layers = [[position for position in layer if position in threat_places] for layer in layers]
        current_score = 0
        for i, layer in enumerate(layers):
            current_score += (4-i)**2 * len(layer)
        
        check = False
        checkmate = False
        blocking_way = False
        too_close = False
        threat = False
        check_value = 1
        threat_value = 50

        objective = {}
        if self.position in possible_king_moves:
            threat = True
            for move in moves:
                objective[move] = threat_value
        else:
            for move in moves:
                objective[move] = 0

        king_x ,king_y = king_position   

        for move in moves:
            new_board = self.board.pseudo_copy()
            new_rook = new_board.get_piece_at(self.position)
            new_board.move_piece(new_rook, move)

            #objective[move] -= current_score
            x, y = move
            if abs(x-king_x) <= 1 and abs(y-king_y) <= 1:
                objective[move] = -1
                continue

            new_rook_possible_moves = new_rook.threat_places(new_board)

            for move in new_rook_possible_moves:
                if abs(move[0] - king_x) > 1 or abs(move[1] - king_y) > 1:
                    new_rook_possible_moves.remove(move)

            #intersection between the possible moves of the king and the rook
            #intersection = [move for move in new_rook_possible_moves if move in possible_king_moves]
            layers_division = self.board.make_layers() 



            #keep only the moves that are in the intersection
            layers_division = [[position for position in layer if position in new_rook_possible_moves] for layer in layers_division]

            for i, layer in enumerate(layers_division):
                objective[move] += (4-i)**2 * len(layer)
            
            
            distance = 0

            distance = abs(x - king_x) + abs(y - king_y)
            distance = math.floor(math.log(distance, 2)) if distance != 0 else 0
            objective[move] += distance
            
                       
            if new_board.is_in_checkmate('black'):
                objective[move] += 1000

        #return the move with the highest objective value
        return max(objective, key=objective.get), objective[max(objective, key=objective.get)]

   
    def cuurent_threat(self):
        king_position = self.search_for_king()
        moves = self.possible_moves(self.board)
        x_k, y_k = king_position
        threat = []
        for move in moves:
            x, y = move
            if abs(x - x_k) <= 1 and abs(y - y_k) <= 1:
                threat.append(move)
        
        return threat
                


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
