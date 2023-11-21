import chess
import random
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import evaluate

CHECKMATE_SCORE = 1000000

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

class Bot:
    def __init__(self):
        self.board = chess.Board()
        self.pvmove = chess.Move.null
        self.startTime = 0
        

    def timeLimit(self):
        # print(self.startTime, time.time())
        return self.startTime<=time.time()

    def choose_move(self, board):
        self.board = board

        legal_moves = list(self.board.legal_moves)
        self.pvmove = random.choice(legal_moves)
        self.startTime = time.time()+1
        bestmove = random.choice(legal_moves)

        for depth in range(1, 100):
            self.search(depth, 0, -CHECKMATE_SCORE-1, CHECKMATE_SCORE+1)
            if self.timeLimit(): break
            # print(self.pvmove)
            print(depth)
            bestmove = self.pvmove

        return bestmove 
    
    def is_draw(self):
        return self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_repetition(3)


    def search(self, depth, ply, alpha, beta):
        if self.board.is_checkmate():
            return -CHECKMATE_SCORE
        if self.is_draw():
            return 0

        if depth <= 0:
            return evaluate.evaluate(self.board) * (1 if self.board.turn else -1)

        moves = list(self.board.legal_moves)

        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, ply+1, -beta, -alpha)
            self.board.pop()

            if self.timeLimit(): return 0
            # if ply == 0: 
            #     print(move, score)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                if ply == 0: self.pvmove = move

        return alpha
    

