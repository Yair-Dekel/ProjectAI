# We can use the python-chess library to probe Syzygy tablebases to determine the game result (win/draw/loss) and distance to mate (DTM) for a given board position. Here's an example of how to use the python-chess library to probe Syzygy tablebases:
#chess.syzygy
#python‑chess
import chess
import chess.syzygy
from play_pawn_game import run_KPvk_game

# Set up a board position (example: King and Pawn vs King)
board = chess.Board("3k4/8/8/8/8/8/1P2K3/8 w - - 0 1")



# Specify the directory where your Syzygy tablebase files are stored
tablebase_path = "c:\\Users\\Yair\\pythonProjects\\ProgectAI\\tables"

with chess.syzygy.open_tablebase(tablebase_path) as tablebase:
    wdl = tablebase.probe_wdl(board)  # Returns winning/drawing/losing info

print("WDL:", wdl)

fen = "8/8/8/8/4k2K/8/7P/8 w - - 0 1"

print(fen)
# Run the King vs Pawn vs King game
result = run_KPvk_game(tablebase_path, max_moves=50, print_board=True,random_positions=False, fen = fen)
print(result)

