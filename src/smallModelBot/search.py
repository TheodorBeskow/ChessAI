import chess
import random
import time
import sys
import os
import tensorflow as tf

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import smallModelBot.evaluate_s as evaluate
from smallModelBot.ZobristHash_s import ZobristHash
from smallModelBot.TranspositionTable_s import TranspositionTable

CHECKMATE_SCORE = 1000000

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

tt = TranspositionTable()
zob = ZobristHash()


class Bot:
    def __init__(self):
        self.board = chess.Board()
        self.pvmove = chess.Move.null
        self.allocatedTime = 0
        self.c = 0


    def timeLimit(self):
        # print(self.allocatedTime, time.time())
        return self.allocatedTime<=time.time()

    def choose_move(self, board):
        self.board = board


        legal_moves = list(self.board.legal_moves)
        self.pvmove = random.choice(legal_moves)
        self.allocatedTime = time.time()+1

        self.c = 0
        for depth in range(1, 100):
            self.search(depth, 0, -CHECKMATE_SCORE-1, CHECKMATE_SCORE+1)
            if self.timeLimit(): break
        print(depth, self.c)


        return self.pvmove 
    
    def is_draw(self):
        return self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_repetition(3)


    def search(self, depth, ply, alpha, beta):
        if self.board.is_checkmate():
            return -CHECKMATE_SCORE
        if self.is_draw():
            return 0

        if depth <= 0:
            self.c+=1
            return evaluate.evaluate(self.board.fen())

        ttMove = "blabla"
        # ttMove = tt.lookup(zob.compute_hash(self.board), depth)

        moves = list(self.board.legal_moves)
        moves.sort(key=lambda move: self.score_move(move, ttMove), reverse=True)

        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, ply+1, -beta, -alpha)
            self.board.pop()

            if self.timeLimit(): return 0
            # if ply == 0: 
            #     print(move, score)

            if score > alpha:
                alpha = score
                ttMove = move
                if ply == 0: self.pvmove = move
            if score >= beta:
                return beta

        # tt.save(zob.compute_hash(self.board), depth, pvmove, alpha)
        return alpha
    


    def score_move(self, move, bestMove):
        moveScore = 0
        if move == bestMove: 
            moveScore += 10000
        if self.board.is_capture(move):
            pass
            # moveScore += 100 + piece_values[self.board.piece_at(move.to_square).piece_type] - piece_values[self.board.piece_at(move.from_square).piece_type]
        if self.board.is_attacked_by(not self.board.turn, move.to_square):
            moveScore -= 100
        return moveScore
    

