import chess
import chess.engine

# Function to find the number of lines in a file
def count_lines(file_path):
    with open(file_path, "r") as file:
        return sum(1 for _ in file)

# File paths
positions_file = "AI/positions2.txt"
ratings_file = "AI/fen_ratings2.txt"

# Read already processed lines in the ratings file
processed_rows = count_lines(ratings_file)

# Open the file containing FEN strings
with open(positions_file, "r") as file:
    fen_list = file.readlines()

# Open a file to append new FEN numbers and their ratings
with open(ratings_file, "a") as output_file:
    for count, fen in enumerate(fen_list[processed_rows:], start=processed_rows + 1):
        print(f"Processing position {count}...")
        output_line = fen.strip()

        # Initialize the chess board from the FEN string
        board = chess.Board(fen.strip())

        # Path to the Stockfish engine executable
        stockfish_path = "AI\stockfish\stockfish-windows-x86-64-avx2.exe"

        # Create a Stockfish engine instance
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

        # Get the evaluation from Stockfish for the given position
        eval_info = engine.analyse(board, chess.engine.Limit(time=1))  # You can adjust the time limit

        # Adjust the evaluation score if it's Black's turn
        if board.turn == chess.BLACK:
            eval_info["score"].relative = -eval_info["score"].relative

        # Append evaluation score to the output line
        output_line += " " + str(eval_info["score"].relative) + "\n"

        # Write the FEN string and its evaluation to the file
        output_file.write(output_line)

        # Close the engine instance
        engine.quit()

print("Data processing complete.")
