# ChessAI


## Info


To start the game run visualizer from the root and open the localhost linked in the console.


The main bot is in the folder smallModelBot and contains a small nn for evaluation in a minimax. The board representation is one node for every piece on every square. The nn only contains one hidden layer and uses the custom activation function squared clipped relu. If it is blacks turn in the position we just flip the board as if it was white to play instead of making the nn more complicated. We have tried using a bigger cnn but found it to give worse results.


The minimax currently only contains alpha beta pruning, basic move ordering and iterative deepening. The code also contains a transposition table although it is currently not used in the smallModelBot.



Chess library documentation: https://github.com/niklasf/python-chess


Downloaded games:


https://database.lichess.org/


https://www.kaggle.com/datasets/jw1912/2-8m-text-data/

