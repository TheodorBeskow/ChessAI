import chess
import chess.engine
import importlib.util
import time
import random


def game():
    # Get bots
    spec1 = importlib.util.spec_from_file_location("bot1", "src/bot1/search.py")
    bot1_module = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(bot1_module)
    bot1 = bot1_module.Bot()

    spec2 = importlib.util.spec_from_file_location("bot2", "src/bot2/search.py")
    bot2_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(bot2_module)
    bot2 = bot2_module.Bot()

    # board.set_fen("8/6k1/8/3r4/8/3R4/8/K7 w - - 0 1")

    # Play the game
    while True:
        gameturn = 0
        board = chess.Board()
        while not board.is_game_over():
            if random.randint(0, 12) < 4 or gameturn < 4: 
                move = random.choice(list(board.legal_moves))
                print("rand")
            elif board.turn:
                move = bot1.choose_move(board)
            else:
                move = bot1.choose_move(board)

            gameturn+=1

            # Check if the move is legal
            if move not in list(board.legal_moves):
                print("Illegal move: " + str(move))
                break
            # time.sleep(1)

            # print(board)
            # print("----------")
            board.push(move)
            # print(board)

            with open("AI/BotData.txt", "a") as output_file:
                #Eval with stochfish
                stockfish_path = "AI\stockfish\stockfish-windows-x86-64-avx2.exe"
                engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
                eval_info = engine.analyse(board, chess.engine.Limit(time=1)) 
                if board.turn == chess.BLACK:
                    eval_info["score"].relative = -eval_info["score"].relative

                output_line = board.fen().strip() + " " + str(eval_info["score"].relative) + "\n"

                print(output_line)
                output_file.write(output_line)
                engine.quit()
            
            if random.randint(0, 10) == 0: break




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
        elif board.halfmove_clock >= 100 and any(board.generate_legal_moves()):
            print("The game is a draw due to the 50-move rule")
        elif board.is_repetition(3):
            print("The game is a draw due to threfold repetition")
        else:
            print("Unsure of reason of end to game")

if __name__ == "__main__":
    game()
