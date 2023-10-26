import chess
import random

CHECKMATE_SCORE = 1000000

class Bot:
    def __init__(self):
        self.board = chess.Board()

    def choose_move(self, board):
        self.board = board
        legal_moves = list(self.board.legal_moves)

        best_move = None
        best_score = -CHECKMATE_SCORE

        for move in legal_moves:
            self.board.push(move)
            score = -self.search(1, -CHECKMATE_SCORE, CHECKMATE_SCORE)
            self.board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    
    def is_draw(self):
        return self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_repetition(3)
    
    def evaluate(self):
        # Define piece values
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }

        # Calculate material value for each color
        white_value = sum(piece_values.get(self.board.piece_at(square).piece_type, 0) for square in self.board.pieces(chess.KING, chess.WHITE))
        black_value = sum(piece_values.get(self.board.piece_at(square).piece_type, 0) for square in self.board.pieces(chess.KING, chess.BLACK))

        # Return the difference in material value
        return white_value - black_value


    def search(self, depth, alpha, beta):
        if self.board.is_checkmate():
            return CHECKMATE_SCORE
        if self.is_draw():
            return 0

        if depth <= 0:
            return self.evaluate()

        moves = list(self.board.legal_moves)

        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, -beta, -alpha)
            self.board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha
