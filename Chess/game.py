from board import Board
from king import King
from rook import Rook
import random


class Game:
    def __init__(self, turns = 30, threat_val=69, decrease_moves_val=5):
        self.turns = turns
        self.threat_val = threat_val
        self.decrease_moves_val = decrease_moves_val

    def initalized_board(self):
        while True:
        # Create a new board
            chess_board = Board()

            pieces = []
            # Create a white king and a white rook
            pieces.append(King('black', "King", chess_board))
            pieces.append(King('white', "King", chess_board))
            pieces.append(Rook('white', "Rook", chess_board, self.threat_val, self.decrease_moves_val))
            pieces.append(Rook('white', "Rook", chess_board, self.threat_val, self.decrease_moves_val))


            # Place the king and rook on the board
            for piece in pieces:
                position = (random.randint(0, 7), random.randint(0, 7))
                while not chess_board.check_empty(position):
                    position = (random.randint(0, 7), random.randint(0, 7)) 
                chess_board.add_piece(piece, position)
            
            if not chess_board.is_in_check('black'):
                break
        
        return chess_board, pieces
    

    def start(self, chess_board, pieces):
        for i in range(self.turns):

            if white_turn:  # white turn
                rook1_move, rook1_value = pieces[2].objective_function()
                rook2_move, rook2_value = pieces[3].objective_function()
                white_king_move, white_king_value = pieces[1].objective_function()

                # move the pieces with the highest value
                if rook1_value >= rook2_value and rook1_value >= white_king_value:
                    chess_board.move_piece(pieces[2], rook1_move)
                elif rook2_value >= rook1_value and rook2_value >= white_king_value:
                    chess_board.move_piece(pieces[3], rook2_move)
                else:
                    chess_board.move_piece(pieces[1], white_king_move)

            else: # black turn

                black_king_move, black_king_value = pieces[0].objective_function()
                chess_board.move_piece(pieces[0], black_king_move)

            chess_board.print_board()
            print(' ')

            if len(pieces[0].possible_moves(chess_board)) == 0:
                print('White wins')
                break

            white_turn = not white_turn
                    


    def __repr__(self):
        return self.board.__repr__()