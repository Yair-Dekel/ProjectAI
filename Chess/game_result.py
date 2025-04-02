# We can use the python-chess library to probe Syzygy tablebases to determine the game result (win/draw/loss) and distance to mate (DTM) for a given board position. Here's an example of how to use the python-chess library to probe Syzygy tablebases:
#chess.syzygy
#python‑chess
import chess
import chess.syzygy
import sys
from play_pawn_game import run_KPvk_game
import os

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tablebase_path = os.path.join(project_root, "tables")
    fen = None
    max_moves=50
    pawn_pos, w_king_pos, b_king_pos = None, None, None
    white_turn=True
    print_board=False
    random_positions=True
    gui=False

    # get arguments from command line
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == 'fen' and i + 6 < len(args):
            fen = ' '.join(args[i + 1:i + 7]) 
            i += 6  # Move index forward
        elif args[i] == 'tablebase_path' and i + 1 < len(args):
            tablebase_path = args[i + 1]
            i += 1
        elif args[i] == 'max_moves' and i + 1 < len(args):
            max_moves = int(args[i + 1])
            i += 1
        elif args[i] == 'pawn_pos' and i + 2 < len(args):
            pawn_pos = (int(args[i + 1]), int(args[i + 2]))
            i += 2
        elif args[i] == 'w_king_pos' and i + 2 < len(args):
            w_king_pos = (int(args[i + 1]), int(args[i + 2]))
            i += 2
        elif args[i] == 'b_king_pos' and i + 2 < len(args):
            b_king_pos = (int(args[i + 1]), int(args[i + 2]))
            i += 2
        elif args[i] == 'not_white_turn':
            white_turn = False
        elif args[i] == 'gui':
            gui = True
        elif args[i] == 'print_board':
            print_board = True
        elif args[i] == 'not_random_positions':
            random_positions = False
        i += 1  

    print(fen)
    # Run the King vs Pawn vs King game
    result = run_KPvk_game(tablebase_path, max_moves=max_moves, print_board=print_board,random_positions=random_positions, fen = fen, gui=gui, pawn_pos=pawn_pos, w_king_pos=w_king_pos, b_king_pos=b_king_pos, white_turn=white_turn)
    print(result)

