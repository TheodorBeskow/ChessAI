import chess
import time

# board = chess.Board()
# counter = 0
# from smallModelBot.ZobristHash_s import ZobristHash

# zob = ZobristHash()
# startTime = time.time()
# while time.time()-startTime <1:
#     zob.compute_hash(board)
#     counter+=1
# print(counter)

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_custom_objects

def squared_clipped_relu(x):
    return tf.keras.activations.relu(x, max_value=1)**2

get_custom_objects().update({'squared_clipped_relu': squared_clipped_relu})
model = load_model(r"AI\TrainedModel.keras")



# with custom_object_scope({'squared_clipped_relu': squared_clipped_relu}):
#     new_model = load_model('src\smallModelBot\TrainedModel.h5')
