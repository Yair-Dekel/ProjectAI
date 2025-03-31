from play_pawn_game import run_kpvk_game, run_KPvk_game, check_result_by_syzygy, convert_board_to_fen, convert_fen_to_positions
import chess.syzygy
import sys
import os
import random

tablebase_path = "C:\\Users\\Yair\\pythonProjects\\ProgectAI\\tables"

# Run the King vs Pawn vs King game
result = run_KPvk_game(tablebase_path, max_moves=50, print_board=True,random_positions=False, fen ="8/8/8/5k2/8/8/4P3/3K4 w - - 0 1")
print(result)

with open("fen.txt", "r") as f:
    for line in f:
        if "except_draw_but_win" in line:
            fen = line.split()[0]
            fen = fen + " w - - 0 1"
            print(fen)
            result = run_KPvk_game(tablebase_path, max_moves=50, print_board=True,random_positions=False, fen =fen)
            print(result)