from board import Board
from king import King
from pawn import Pawn
import random
import sys
import random
import chess
import chess.syzygy
import tkinter as tk
from chess_gui import ChessGUI
import threading
import time

def generate_random_positions():
    """Generate random valid positions for KPvK."""
    while True:
        b_king_pos = (random.randint(0, 7), random.randint(0, 7))
        w_king_pos = b_king_pos
        while abs(w_king_pos[0] - b_king_pos[0]) <= 1 and abs(w_king_pos[1] - b_king_pos[1]) <= 1:
            w_king_pos = (random.randint(0, 7), random.randint(0, 7))

        pawn_pos = (random.randint(1, 6), random.randint(0, 7))
        # the pawn not theat the black king
        if b_king_pos[0] + 1 != pawn_pos[0] or abs(b_king_pos[1] - pawn_pos[1]) != 1:
            # the pawn not the same place as the white king or the black king
            if not (b_king_pos[0] == pawn_pos[0] and b_king_pos[1] == pawn_pos[1]) and not (w_king_pos[0] == pawn_pos[0] and w_king_pos[1] == pawn_pos[1]):
                return pawn_pos, w_king_pos, b_king_pos
        
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

def convert_fen_to_positions(fen):
    rows = fen.split()[0].split('/')  # Get the board part of the FEN
    piece_positions = {}
    
    for x, row in enumerate(rows):
        y = 0
        for char in row:
            if char.isdigit():  # Empty squares
                y += int(char)
            else:
                if char == 'P':  # White pawn
                    piece_positions['Pawn'] = (x, y)
                elif char == 'K':  # White king
                    piece_positions['White King'] = (x, y)
                elif char == 'k':  # Black king
                    piece_positions['Black King'] = (x, y)
                y += 1
    
    return piece_positions

def check_result_by_syzygy(board, tablebase_path):
    fen = convert_board_to_fen(board)
    chess_board = chess.Board(fen)
    with chess.syzygy.open_tablebase(tablebase_path) as tablebase:
        return tablebase.probe_wdl(chess_board), fen

def run_kpvk_game(tablebase_path, max_moves=50, pawn_pos=None, w_king_pos=None, b_king_pos=None, white_turn=True, print_board=False):
    chess_board = Board()
    pieces = [
        King('black', "King", chess_board),
        King('white', "King", chess_board),
        Pawn('white', "Pawn", chess_board)
    ]
    
    if pawn_pos is None or w_king_pos is None or b_king_pos is None:
        pawn_pos, w_king_pos, b_king_pos = generate_random_positions()

    chess_board.add_piece(pieces[0], b_king_pos)   
    chess_board.add_piece(pieces[1], w_king_pos)
    chess_board.add_piece(pieces[2], pawn_pos)

    # Evaluate the position with Syzygy
    wdl, fen = check_result_by_syzygy(chess_board.board, tablebase_path)

    if print_board:
        chess_board.print_board()
    
    # Play the game
    for _ in range(max_moves):
        if white_turn:
            pawn_move, pawn_value = pieces[2].objective_function2()
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
        if print_board:
            chess_board.print_board()
        # Check for game-ending conditions
        if len(chess_board.pieces) < 3:
            return "Draw", wdl

        if pieces[2].position[0] == 0:
            # Check if the black king can capture the pawn immediately
            if abs(pieces[0].position[0] - pieces[2].position[0]) <= 1 and abs(pieces[0].position[1] - pieces[2].position[1]) <= 1:
                # If the white king is not protecting the pawn, it's a draw
                if not (abs(pieces[1].position[0] - pieces[2].position[0]) <= 1 and abs(pieces[1].position[1] - pieces[2].position[1]) <= 1):
                    return "Draw", wdl

            return "White wins", wdl

        white_turn = not white_turn
    
    return "Draw", wdl, fen

def run_game(max_moves=50, white_turn=True, print_board=False, fen=None, pieces=None, wdl=None, chess_board=None, gui=False):
        
    # Play the game
    for _ in range(max_moves):
        if gui:
            time.sleep(0.5)
        if white_turn:
            piece, move = pieces[1].objective_function_white2()
            if move == None:
                return "Draw", wdl, fen
            if piece == "Pawn":
                chess_board.move_piece(pieces[2], move)
            if piece == "King":
                chess_board.move_piece(pieces[1], move)

        else:
            try:
                black_king_move, _ = pieces[0].objective_function_black()
                chess_board.move_piece(pieces[0], black_king_move)
            except Exception as e:
                if str(e) == "No possible moves":
                    return "Draw", wdl, fen
                
        if print_board:
            chess_board.print_board()

        # Check for game-ending conditions
        if len(chess_board.pieces) < 3:
            return "Draw", wdl, fen

        if pieces[2].position[0] == 0:
            # Check if the black king can capture the pawn immediately
            if abs(pieces[0].position[0] - pieces[2].position[0]) <= 1 and abs(pieces[0].position[1] - pieces[2].position[1]) <= 1:
                # If the white king is not protecting the pawn, it's a draw
                if not (abs(pieces[1].position[0] - pieces[2].position[0]) <= 1 and abs(pieces[1].position[1] - pieces[2].position[1]) <= 1):
                    return "Draw", wdl, fen

            return "White wins", wdl, fen

        white_turn = not white_turn
    
    return "Draw", wdl, fen

def run_KPvk_game(tablebase_path, max_moves=50, pawn_pos=None, w_king_pos=None, b_king_pos=None, white_turn=True, print_board=False, random_positions=True, fen=None, gui=False):

    chess_board = Board()
    pieces = [
        King('black', "King", chess_board),
        King('white', "King", chess_board),
        Pawn('white', "Pawn", chess_board)
    ]
    
    if random_positions:
        pawn_pos, w_king_pos, b_king_pos = generate_random_positions()
    if fen and not random_positions:
        positions = convert_fen_to_positions(fen)
        pawn_pos = positions['Pawn']
        w_king_pos = positions['White King']
        b_king_pos = positions['Black King']

    chess_board.add_piece(pieces[0], b_king_pos)   
    chess_board.add_piece(pieces[1], w_king_pos)
    chess_board.add_piece(pieces[2], pawn_pos)

    # Evaluate the position with Syzygy
    wdl, fen = check_result_by_syzygy(chess_board.board, tablebase_path)

    if print_board:
        chess_board.print_board()
    
    if gui:
        root = tk.Tk()
        gui = ChessGUI(root, chess_board)


        game_thread = threading.Thread(target=run_game, args=(max_moves, white_turn, False, fen, pieces, wdl, chess_board, True), daemon=True)

        game_thread.start()

        # Start Tkinter main loop
        root.mainloop()

    else:
        return run_game(max_moves, white_turn, print_board, fen, pieces, wdl, chess_board)

    '''   
    # Play the game
    for _ in range(max_moves):
        if white_turn:
            piece, move = pieces[1].objective_function_white2()
            if move == None:
                return "Draw", wdl, fen
            if piece == "Pawn":
                chess_board.move_piece(pieces[2], move)
            if piece == "King":
                chess_board.move_piece(pieces[1], move)

        else:
            try:
                black_king_move, _ = pieces[0].objective_function_black()
                chess_board.move_piece(pieces[0], black_king_move)
            except Exception as e:
                if str(e) == "No possible moves":
                    return "Draw", wdl, fen
                
        if print_board:
            chess_board.print_board()

        # Check for game-ending conditions
        if len(chess_board.pieces) < 3:
            return "Draw", wdl, fen

        if pieces[2].position[0] == 0:
            # Check if the black king can capture the pawn immediately
            if abs(pieces[0].position[0] - pieces[2].position[0]) <= 1 and abs(pieces[0].position[1] - pieces[2].position[1]) <= 1:
                # If the white king is not protecting the pawn, it's a draw
                if not (abs(pieces[1].position[0] - pieces[2].position[0]) <= 1 and abs(pieces[1].position[1] - pieces[2].position[1]) <= 1):
                    return "Draw", wdl, fen

            return "White wins", wdl, fen

        white_turn = not white_turn
    
    return "Draw", wdl, fen
'''



