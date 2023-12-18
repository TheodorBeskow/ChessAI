import chess
import random

class ZobristHash:
    def __init__(self):
        self.zobrist_table = self.init_zobrist()

    def init_zobrist(self):
        return [[[random.randint(1, 2**64 - 1) for _ in range(2)] for _ in range(64)] for _ in range(len(chess.PIECE_TYPES))]

    def compute_hash(self, board):
        h = 0
        for piece_type in chess.PIECE_TYPES:
            for color in [chess.WHITE, chess.BLACK]:
                for square in board.pieces(piece_type, color):
                    h ^= self.zobrist_table[piece_type - 1][square][int(color)]
        return h
