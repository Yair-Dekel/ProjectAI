from play_pawn_game import run_kpvk_game, run_KPvk_game, check_result_by_syzygy, convert_board_to_fen
import chess.syzygy
import sys
import os
import random

tablebase_path = "C:\\Users\\Yair\\pythonProjects\\ProgectAI\\tables"

# Run the King vs Pawn vs King game
result = run_KPvk_game(tablebase_path, max_moves=50, print_board=True, pawn_pos=(1, 0), w_king_pos=(6, 3), b_king_pos=(1, 2))
print(result)

except_win_but_draw = 0
except_draw_but_win = 0
except_draw_and_draw = 0
except_win_and_win = 0

with open("fen.txt", "w") as f:
    for _ in range(1000):
        result = run_KPvk_game(tablebase_path, max_moves=50, print_board=False)
        if result[0] == "White wins" and result[1] == 0:
            f.write(result[2] + "\n")
            except_draw_but_win += 1
        elif result[0] == "Draw" and result[1] == 2:
            f.write(result[2] + "\n")
            except_win_but_draw += 1
        elif result[0] == "Draw" and result[1] == 0:
            except_draw_and_draw += 1
        elif result[0] == "White wins" and result[1] == 2:
            except_win_and_win += 1

print(f"Except win but draw: {except_win_but_draw}")
print(f"Except draw but win: {except_draw_but_win}")
print(f"Except draw and draw: {except_draw_and_draw}")
print(f"Except win and win: {except_win_and_win}")