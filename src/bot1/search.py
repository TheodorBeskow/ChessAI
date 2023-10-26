import chess
import random
from evaluate import evaluate

CHECKMATE_SCORE = 1000000

class Bot:
    def __init__(self):
        self.board = chess.Board()
        self.pvmove = chess.Move.null

    def choose_move(self, board):
        self.board = board

        legal_moves = list(self.board.legal_moves)
        pvmove = random.choice(legal_moves)

        self.search(2, 0, -CHECKMATE_SCORE, CHECKMATE_SCORE)
        return pvmove 
    
    def is_draw(self):
        return self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_repetition(3)


    def search(self, depth, ply, alpha, beta):
        if self.board.is_checkmate():
            return CHECKMATE_SCORE
        if self.is_draw():
            return 0

        if depth <= 0:
            return evaluate(self.board)

        moves = list(self.board.legal_moves)

        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, ply+1, -beta, -alpha)
            self.board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                if ply == 0: self.pvmove = move

        return alpha
