import game as Game

games_results = {}
games_number = 200 # Number of games to play

fine_tuning = 30

for j in range(fine_tuning):
    threat_val = 69
    decrease_moves_val = 5
     

for i in range(games_number):
    try:
        game = Game.Game(30, 69, 5)
        chess_board, pieces = game.initalized_board()
        result = game.start(chess_board, pieces)
        #print(result)
    except Exception as e:
        print(f"An error occurred: {e}")
    if result in games_results:
        games_results[result] += 1
    else:
        games_results[result] = 1

for result in games_results:
        print(f"{result}: {games_results[result]} - {games_results[result]/games_number*100}%")

    