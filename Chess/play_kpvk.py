from play_pawn_game import run_kpvk_game, run_KPvk_game, check_result_by_syzygy, convert_board_to_fen, convert_fen_to_positions
import chess.syzygy
import sys
import os
import random

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tablebase_path = os.path.join(project_root, "tables")
    max_moves = 50
    games_num = 100
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == 'tablebase_path' and i + 1 < len(args):
            tablebase_path = args[i + 1]
            i += 1
        elif args[i] == 'max_moves' and i + 1 < len(args):
            max_moves = int(args[i + 1])
            i += 1
        elif args[i] == 'games_num' and i + 1 < len(args):
            games_num = int(args[i + 1])
            i += 1
        i += 1 


    except_win_but_draw = 0
    except_draw_but_win = 0
    except_draw_and_draw = 0
    except_win_and_win = 0


    with open("fen.txt", "w") as f:
        for _ in range(games_num):
            result = run_KPvk_game(tablebase_path, max_moves=50, print_board=False)
            if result[0] == "White wins" and result[1] == 0:
                f.write(result[2] + "   except_draw_but_win" + "\n")
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