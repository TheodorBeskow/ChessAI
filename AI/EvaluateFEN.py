import chess
import chess.engine

count = 0

# Open the file containing FEN strings
with open("AI/positions.txt", "r") as file:
    fen_list = file.readlines()

for fen in fen_list:
    count += 1
    print(f"Position {count}:")
    print(fen.strip())  # Print the FEN string

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

    # Print the evaluation score
    print("Evaluation:", eval_info["score"])

    # Close the engine instance
    engine.quit()
