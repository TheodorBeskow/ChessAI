


class TranspositionTable:
    def __init__(self):
        self.table = {}

    def save(self, hash_value, depth, move, score):
        if hash_value in self.table:
            if self.table[hash_value][0]>depth: return
        self.table[hash_value] = (depth, move, score)

    def lookup(self, hash_value, depth):
        if hash_value in self.table:
            stored_depth, stored_move, stored_score = self.table[hash_value]
            return stored_move
        return None

