import chess
import numpy as np
import time
import os


def fen_to_board(fen):
    # Parse the FEN string
    parts = fen.split(" ")
    isWhite = parts[1] == 'w'

    # Create a chess board
    board = chess.Board(fen)

    # Convert the board position to a binary matrix
    binary_board = np.zeros((8, 8, 6), dtype=np.float32)
    piece_amount = np.zeros((12), dtype=np.float32)
    pieces = {'p': [0, 1.0], 'r': [1, 1.0], 'n': [2, 1.0], 'b': [3, 1.0], 'q': [4, 1.0], 'k': [5, 1.0],
              'P': [0, -1.0], 'R': [1, -1.0], 'N': [2, -1.0], 'B': [3, -1.0], 'Q': [4, -1.0], 'K': [5, -1.0]}

    for i in range(64):
        piece = board.piece_at(i)
        if piece:
            if isWhite:
                binary_board[i // 8, i % 8, pieces[str(piece)][0]] = pieces[str(piece)][1]
            else:
                binary_board[7-(i // 8), 7-(i % 8), pieces[str(piece)][0]] = -pieces[str(piece)][1]
            if isWhite ^ (pieces[str(piece)][1] < 0):
                piece_amount[pieces[str(piece)][0]] += 1
            else:
                piece_amount[pieces[str(piece)][0]+6] += 1

    return [binary_board, piece_amount]


def evaluate(model, fens):
    startTime = time.time()
    binary_boards = []
    piece_amounts = []

    for fen in fens:
        binary_board, piece_amount = fen_to_board(fen)
        binary_boards.append(binary_board)
        piece_amounts.append(piece_amount)

    binary_boards = np.array(binary_boards)
    piece_amounts = np.array(piece_amounts)

    res = model.predict([binary_boards, piece_amounts], verbose=1)
    # print(time.time()-startTime, 5)
    return res
