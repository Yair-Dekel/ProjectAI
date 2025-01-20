from board import Board
from king import King
from pawn import Pawn
import random


# Create a new board
chess_board = Board()

pieces = []
# Create a white king and a white rook
pieces.append(King('black', "King", chess_board))
pieces.append(King('white', "King", chess_board))
pieces.append(Pawn('white', "Pawn", chess_board))


# Place the king and rook on the board
chess_board.add_piece(pieces[0], (4, 5))
chess_board.add_piece(pieces[1], (6, 6))
chess_board.add_piece(pieces[2], (6, 7))

# Print the initial board setup
chess_board.print_board()


white_turn = True

for i in range(30):
    if white_turn:
        try:
            pawn_move, pawn_value = pieces[2].objective_function()
        except Exception as e:
            print(f"An error occurred: {e}")
            break
        white_king_move, white_king_value = pieces[1].objective_function_white()

        # move the pieces with the highest value
        if pawn_value < white_king_value:
            chess_board.move_piece(pieces[2], pawn_move)
        else:
            chess_board.move_piece(pieces[1], white_king_move)

    else:
        black_king_move, black_king_value = pieces[0].objective_function_black()
        chess_board.move_piece(pieces[0], black_king_move)

    chess_board.print_board()
    print(' ------------- ')

    if len(chess_board.pieces) < 3:
        print('black wins')
        break
    pawn_pos_x, pawn_pos_y = pieces[2].position

    if pawn_pos_x == 0:
        print('white wins')
        break

    white_turn = not white_turn


print(' ****************************************** ')

# Create a new board
chess_board = Board()

pieces = []
# Create a white king and a white rook
pieces.append(King('black', "King", chess_board))
pieces.append(King('white', "King", chess_board))
pieces.append(Pawn('white', "Pawn", chess_board))

position_black_king = (random.randint(0, 7), random.randint(0, 7))
chess_board.add_piece(pieces[0], position_black_king)
x_b_k, y_b_k = position_black_king

position_white_king = position_black_king
while not chess_board.check_empty(position_white_king):
    position_white_king = (random.randint(0, 7), random.randint(0, 7))
    x_w_k, y_w_k = position_white_king
    if abs(x_b_k - x_w_k) <= 1 and abs(y_b_k - y_w_k) <= 1:
        position_white_king = position_black_king
chess_board.add_piece(pieces[1], position_white_king)

position_pawn = position_black_king
while not chess_board.check_empty(position_pawn):
    position_pawn = (random.randint(0, 6), random.randint(0, 7))
    x_p, y_p = position_pawn
    if x_b_k + 1 == x_p and abs(y_b_k - y_p) == 1:
        position_pawn = position_black_king
chess_board.add_piece(pieces[2], position_pawn)
'''
# Print the initial board setup
chess_board.print_board()


white_turn = True

for i in range(30):
    if white_turn:
        pawn_move, pawn_value = pieces[2].objective_function()
        white_king_move, white_king_value = pieces[1].objective_function_white()

        # move the pieces with the highest value
        if pawn_value < white_king_value:
            chess_board.move_piece(pieces[2], pawn_move)
        else:
            chess_board.move_piece(pieces[1], white_king_move)

    else:
        black_king_move, black_king_value = pieces[0].objective_function_black()
        chess_board.move_piece(pieces[0], black_king_move)

    chess_board.print_board()
    print(' ')

    if len(chess_board.pieces) < 3:
        print('black wins')
        break
    pawn_pos_x, pawn_pos_y = pieces[2].position

    if pawn_pos_x == 0:
        print('white wins')
        break


    white_turn = not white_turn
'''