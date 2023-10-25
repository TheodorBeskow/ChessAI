import chess

# Create a new chess board
board = chess.Board()

# Print the chess board
print(board)

# Make a move
board.push_san("e4")

# Print the updated board
print(board)

# Check if the game is over
if board.is_game_over():
    print("Game Over")
else:
    print("Game not over yet")
