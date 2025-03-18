from board import Board
from king import King
from pawn import Pawn
import random
import sys
import random
import chess
import chess.syzygy


def convert_board_to_fen(board):
    fen = ""
    for i in range(8):
        empty = 0
        for j in range(8):
            if board[i][j] == ' ':
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += str(board[i][j])
        if empty > 0:
            fen += str(empty)
        if i < 7:
            fen += "/"
    return fen + " w - - 0 1"

def check_result_by_syzygy(board, tablebase_path):
    fen = convert_board_to_fen(board)
    chess_board = chess.Board(fen)
    with chess.syzygy.open_tablebase(tablebase_path) as tablebase:
        return tablebase.probe_wdl(chess_board)

def run_kpvk_game(tablebase_path, max_moves=50):
    chess_board = Board()
    pieces = [
        King('black', "King", chess_board),
        King('white', "King", chess_board),
        Pawn('white', "Pawn", chess_board)
    ]
    
    # Place the black king
    position_black_king = (random.randint(0, 7), random.randint(0, 7))
    chess_board.add_piece(pieces[0], position_black_king)
    x_b_k, y_b_k = position_black_king

    # Place the white king
    position_white_king = position_black_king
    while not chess_board.check_empty(position_white_king):
        position_white_king = (random.randint(0, 7), random.randint(0, 7))
        x_w_k, y_w_k = position_white_king
        if abs(x_b_k - x_w_k) <= 1 and abs(y_b_k - y_w_k) <= 1:
            position_white_king = position_black_king
    chess_board.add_piece(pieces[1], position_white_king)

    # Place the white pawn
    position_pawn = position_black_king
    while not chess_board.check_empty(position_pawn):
        position_pawn = (random.randint(0, 6), random.randint(0, 7))
        x_p, y_p = position_pawn
        if x_b_k + 1 == x_p and abs(y_b_k - y_p) == 1:
            position_pawn = position_black_king
    chess_board.add_piece(pieces[2], position_pawn)

    # Evaluate the position with Syzygy
    wdl = check_result_by_syzygy(chess_board.board, tablebase_path)
    
    # Play the game
    white_turn = True
    for _ in range(max_moves):
        if white_turn:
            pawn_move, pawn_value = pieces[2].objective_function()
            white_king_move, white_king_value = pieces[1].objective_function_white()
            if pawn_value <= white_king_value:
                chess_board.move_piece(pieces[2], pawn_move)
            else:
                chess_board.move_piece(pieces[1], white_king_move)
        else:
            try:
                black_king_move, _ = pieces[0].objective_function_black()
                chess_board.move_piece(pieces[0], black_king_move)
            except Exception as e:
                if str(e) == "No possible moves":
                    return "Draw", wdl

        # Check for game-ending conditions
        if len(chess_board.pieces) < 3:
            return "Draw", wdl

        if pieces[2].position[0] == 0:
            return "White wins", wdl

        white_turn = not white_turn
    
    return "Draw", wdl




