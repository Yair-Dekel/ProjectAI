# We can use the python-chess library to probe Syzygy tablebases to determine the game result (win/draw/loss) and distance to mate (DTM) for a given board position. Here's an example of how to use the python-chess library to probe Syzygy tablebases:
#chess.syzygy
#python‑chess
import chess
import chess.syzygy

# Set up a board position (example: King and Pawn vs King)
board = chess.Board("8/5P2/8/2K5/6k1/8/8/8 w - - 0 1")



# Specify the directory where your Syzygy tablebase files are stored
tablebase_path = "c:\\Users\\Yair\\pythonProjects\\ProgectAI\\tables"

with chess.syzygy.open_tablebase(tablebase_path) as tablebase:
    wdl = tablebase.probe_wdl(board)  # Returns winning/drawing/losing info

print("WDL:", wdl)
# The `probe_wdl` method returns a tuple containing the winning/drawing/losing information for the given board position. The values are represented as follows: