import random

class ZobristHash:
    def __init__(self, board_size):
        self.board_size = board_size
        self.zobrist_table = self.init_zobrist()

    def init_zobrist(self):
        return [[[random.randint(1, 2**64 - 1) for _ in range(12)] for _ in range(self.board_size)] for _ in range(self.board_size)]

    def compute_hash(self, board):
        h = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] != 0: 
                    piece = board[i][j]
                    h ^= self.zobrist_table[i][j][piece]
        return h
    