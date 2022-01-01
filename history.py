




class MoveTracker():

    def __init__(self):
        self.stack = []

    def push(self, value, row, column):
        self.stack.append([(value, row, column)])

    def add_chain(self, value, row, column):
        self.stack[-1].append((value, row, column))

    def pop(self):
        result = self.stack[-1]
        del self.stack[-1]
        return result

    def __str__(self):
        result = ""
        for move in self.stack:
            result += "assigned {} to cell [{}, {}]\n".format(move[0][0], move[0][1], move[0][2])
            if len(move) > 1:
                for chain in move[1:]:
                    result += "     > chained to assign {} to cell [{}, {}]\n".format(chain[0], chain[1], chain[2])
        return result
