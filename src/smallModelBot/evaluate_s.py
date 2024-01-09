import chess
import numpy as np
import time
import os
import tensorflow as tf
from keras.models import load_model
from keras.utils import disable_interactive_logging
from keras.utils import get_custom_objects


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

import tensorflow as tf
from keras.models import load_model
from keras.utils import get_custom_objects

def squared_clipped_relu(x):
    return tf.keras.activations.relu(x, max_value=1)**2

tf.compat.v1.disable_eager_execution()
get_custom_objects().update({'squared_clipped_relu': squared_clipped_relu})

graph = tf.Graph()
with graph.as_default():
    session = tf.compat.v1.Session()
    with session.as_default():
        # Define your model architecture
        main_input = tf.keras.Input(shape=(768,), name='main_input')
        x = tf.keras.layers.Dense(768, kernel_regularizer=tf.keras.regularizers.l2(0.01), activation="squared_clipped_relu")(main_input)
        x = tf.keras.layers.Dropout(0.5)(x)
        output = tf.keras.layers.Dense(1)(x)
        model = tf.keras.Model(inputs=main_input, outputs=output)

        # Load the weights
        model.load_weights(r'AI\TrainedModel4.keras')

def evaluate(fen):
    binary_board = np.array(fen_to_board(fen))
    binary_board = np.expand_dims(binary_board, axis=0)

    with graph.as_default():
        with session.as_default():
            res = model.predict(binary_board, verbose=1)

    return res[0][0]

