

import itertools
import math


class Cell():

    def __init__(self, key):
        self.possible_values = set([1,2,3,4,5,6,7,8,9])
        self.key = key
        self.value = None
        self.row = math.floor(key / 9)
        self.column = (key % 9)
        self.grid = math.floor(self.row/3) + math.floor(self.column/3) + (2*math.floor(self.row/3))
        self.board = None
        self.row_next = None
        self.col_next = None
        self.grid_next = None

    def set_value(self, value):
        assert(value in self.possible_values)
        self.value = value
        self.possible_values.remove(value)
        check_key = self.key
        tmp_row = self
        tmp_col = self
        tmp_grid = self
        while True:
            tmp_row = tmp_row.row_next
            tmp_col = tmp_col.col_next
            tmp_grid = tmp_grid.grid_next

            tmp_row.possible_values.discard(value)
            tmp_col.possible_values.discard(value)
            tmp_grid.possible_values.discard(value)
            if tmp_row.row_next.key == check_key:
                break

    def get_possible_values(self):
        return self.possible_values

    def __str__(self):
        return str(self.value) if self.value is not None else "empty"
