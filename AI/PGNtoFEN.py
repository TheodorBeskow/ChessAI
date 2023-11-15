import chess.pgn
import time
import os
 
# Load your PGN file
pgn_path = "AI/lichess_db_standard_rated_2013-03.pgn"
pgn = open(pgn_path)
 
# Open the output file
output = open("AI/fen_strings.txt", "w")
 
# Get the total size of the PGN file for progress calculation
total_size = os.path.getsize(pgn_path)
processed_size = 0
 
# Record the start time
start_time = time.time()
while True:
 
    # Read the next game from the PGN file
    game = chess.pgn.read_game(pgn)
 
    if game is None:
        # All games have been read
        break
 
    # Get the board for the game
    board = game.board()
 
    # Loop over all moves and write the FEN after each move to the file
    for move in game.mainline_moves():
        board.push(move)
        output.write(board.fen() + "\n")
 
    # Update the processed size
    processed_size += len(str(game))
 
    # If 3 seconds have passed, print the progress
    if time.time() - start_time >= 3:
        print(f"Processed {processed_size / total_size * 100:.2f}% of the file")
        # Record the start time
        start_time = time.time()
 
# Close the output file
output.close()