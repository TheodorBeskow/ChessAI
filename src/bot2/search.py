import chess
import random

class Bot:
    def choose_move(self, board):
        legal_moves = list(board.legal_moves)

        move = random.choice(legal_moves)

        return move
