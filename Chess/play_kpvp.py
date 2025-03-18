from play_pawn_game import run_kpvk_game, check_result_by_syzygy, convert_board_to_fen
import chess.syzygy
import sys
import os
import random

tablebase_path = "C:\\Users\\Yair\\pythonProjects\\ProgectAI\\tables"

# Run the King vs Pawn vs King game
result = run_kpvk_game(tablebase_path, max_moves=50, print_board=True, pawn_pos=(6, 5), w_king_pos=(2, 1), b_king_pos=(0, 4))
print(result)