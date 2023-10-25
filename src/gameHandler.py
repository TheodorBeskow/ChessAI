import chess
import importlib.util


def game():
    # Get bots
    spec1 = importlib.util.spec_from_file_location("bot1", "/src/bot1/search.py")
    bot1_module = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(bot1_module)
    bot1 = bot1_module.Bot()

    spec2 = importlib.util.spec_from_file_location("bot2", "/src/bot2/search.py")
    bot2_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(bot2_module)
    bot2 = bot2_module.Bot()

    board = chess.Board()

    # Play the game
    while not board.is_game_over():
        if board.turn:
            move = bot1.choose_move(board)
        else:
            move = bot2.choose_move(board)

        # Check if the move is legal
        if move not in board.legal_moves:
            print("Illegal move: " + str(move))
            break

        board.push(move)


    # Print the result of the game
    if board.is_checkmate():
        if board.turn:
            print("Bot 2 wins by checkmate")
        else:
            print("Bot 1 wins by checkmate")
    elif board.is_stalemate():
        print("The game is a draw due to stalemate")
    elif board.is_insufficient_material():
        print("The game is a draw due to insufficient material")
    elif board.is_seventyfive_moves():
        print("The game is a draw due to the 75-move rule")
    elif board.is_fivefold_repetition():
        print("The game is a draw due to fivefold repetition")
    elif board.is_variant_draw():
        print("The game is a draw due to variant-specific rules")

if __name__ == "__main__":
    game()
