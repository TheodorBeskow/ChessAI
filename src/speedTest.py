import chess
import time

import chess
import numpy as np
import time
import os


def fen_to_board(fen):
    # Parse the FEN string
    parts = fen.split(" ")
    board_part = parts[0]
    isWhite = parts[1] == 'w'

    # Initialize the binary board
    binary_board = np.zeros((768,), dtype=np.float32)
    pieces = {'p': 0, 'r': 1, 'n': 2, 'b': 3, 'q': 4, 'k': 5,
              'P': 6, 'R': 7, 'N': 8, 'B': 9, 'Q': 10, 'K': 11}
    
    # Parse the board part of the FEN string
    rows = board_part.split('/')
    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                # Empty squares
                col += int(char)
            else:
                # Piece
                if isWhite:
                    binary_board[(i*8 + col)*12 + pieces[char]] = 1
                else:
                    binary_board[(63-(i*8 + col))*12 + (pieces[char]+6)%12] = 1
                col += 1

    return binary_board


def evaluate(fen):
    binary_boards = []
    binary_boards.append(fen_to_board(fen))
    binary_boards = np.array(binary_boards)

    res = model.predict(binary_boards, verbose=1)
    return res


from tensorflow.keras import regularizers, layers
import tensorflow as tf
from tensorflow.keras.utils import get_custom_objects

tf.compat.v1.disable_eager_execution()

def squared_clipped_relu(x):
    return tf.keras.activations.relu(x, max_value=1)**2

get_custom_objects().update({'squared_clipped_relu': squared_clipped_relu})

main_input = tf.keras.Input(shape=(768,), name='main_input')

x = layers.Dense(768, kernel_regularizer=regularizers.l2(0.01), activation="squared_clipped_relu")(main_input)

x = layers.Dropout(0.5)(x)

output = layers.Dense(1)(x)

model = tf.keras.Model(inputs=main_input, outputs=output)

model.compile(optimizer='adam',
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=['mae'])

model.load_weights(r"AI\TrainedModel3.keras")


board = chess.Board()
counter = 0
from smallModelBot.ZobristHash_s import ZobristHash

zob = ZobristHash()
startTime = time.time()
while time.time()-startTime <10:
    print(evaluate("8/8/4k3/8/8/3Q4/3K4/8 w - - 0 1"))
    counter+=1
print(counter)