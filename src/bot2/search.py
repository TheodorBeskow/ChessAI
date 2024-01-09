import chess
import random
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import evaluate2 as evaluate
from ZobristHash2 import ZobristHash as ZobristHash
from TranspositionTable2 import TranspositionTable as TranspositionTable

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
        self.startTime = 0
        

    def timeLimit(self):
        # print(self.startTime, time.time())
        return self.startTime<=time.time()

    def choose_move(self, board):
        self.board = board

        legal_moves = list(self.board.legal_moves)
        self.pvmove = random.choice(legal_moves)
        self.startTime = time.time()+0.1
        bestmove = random.choice(legal_moves)

        for depth in range(1, 100):
            self.search(depth, 0, -CHECKMATE_SCORE-1, CHECKMATE_SCORE+1)
            bestmove = self.pvmove
            if self.timeLimit(): break
        print(depth)

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

        bestMove = tt.lookup(zob.compute_hash(self.board), depth)

        moves = list(self.board.legal_moves)
        moves.sort(key=lambda move: self.score_move(move, bestMove), reverse=True)

        pvmove = None
        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, ply+1, -CHECKMATE_SCORE-1, CHECKMATE_SCORE+1)
            self.board.pop()

            if self.timeLimit(): return 0
            # if ply == 0 : 
            #     print(move)

            if score >= beta:
                return beta
            if score > alpha:
                pvmove = move
                alpha = score
                if ply == 0: self.pvmove = move

        tt.save(zob.compute_hash(self.board), depth, pvmove, alpha)
        return alpha
    


    def score_move(self, move, bestMove):
        moveScore = evaluate.piece_square_tables.get(self.board.piece_at(move.from_square).piece_type)[63-move.to_square if self.board.turn else move.to_square]-evaluate.piece_square_tables.get(self.board.piece_at(move.from_square).piece_type)[63-move.from_square if self.board.turn else move.from_square]
        if move == bestMove: 
            moveScore += 10000
        if self.board.is_capture(move):
            pass
            # moveScore += 100 + piece_values[self.board.piece_at(move.to_square).piece_type] - piece_values[self.board.piece_at(move.from_square).piece_type]
        if self.board.is_attacked_by(not self.board.turn, move.to_square):
            moveScore -= 100
        return moveScore
    

