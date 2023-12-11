import chess.pgn
import time
import os
import re

def extract_fen_and_score(pgn_file, output_folder, progress_file, max_file_size=90*1024*1024):
    total_size = os.path.getsize(pgn_file)
    processed_size = 0

    last_print_time = time.time()

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)


    file_index = 1
    output_file = os.path.join(output_folder, f'output_{file_index}.txt')
    out = open(output_file, 'a')

    # Read the progress file to know where to start from
    start_game = 0
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            start_game = int(f.read())

    game_count = 0
    with open(pgn_file) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break  # end of file

            current_time = time.time()
            if current_time - last_print_time >= 3:
                percentage = (game_count / total_size) * 100
                print(f"Processed: {percentage:.8f}%  {game_count <= start_game}")
                last_print_time = current_time
            game_count += 1
            processed_size += game.end().ply()
            if game_count <= start_game:
                continue

            
            
            if "eval" not in str(game): continue

            # Iterate over all positions in the game
            board = game.board()
            for node in game.mainline():
                board.push(node.move)
                fen = board.fen()

                # Extract the score from the comment if it exists
                comment = node.comment
                score = None
                match = re.search(r'\[%eval ([^\]]+)\]', comment)
                if match:
                    score = match.group(1)

                if score is not None:
                    out.write(f"{fen} {score}\n")
                    out.flush()
                    os.fsync(out.fileno())

                # Check the size of the output file
                if os.path.getsize(output_file) > max_file_size:
                    out.close()
                    file_index += 1
                    output_file = os.path.join(output_folder, f'output_{file_index}.txt')
                    out = open(output_file, 'a')

            # Write the progress to the progress file
            with open(progress_file, 'w') as f:
                f.write(str(game_count))

    out.close()

extract_fen_and_score('lichess_db_standard_rated_2019-04.pgn', 'AI/output_folder', 'AI/progress.txt')
