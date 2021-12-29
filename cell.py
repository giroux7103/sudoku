

import itertools
import math


class Cell():

    def __init__(self, key):
        self.possible_values = set({1,2,3,4,5,6,7,8,9})
        self.key = key
        self.value = None
        self.row_num = math.floor(key / 9)
        self.column_num = (key % 9)
        self.grid_num = math.floor(self.row_num/3) + math.floor(self.column_num/3) + (2*math.floor(self.row_num/3))
        self.board = None
        self.row = None
        self.column = None
        self.grid = None

    def set_value(self, value):
        assert(value in self.possible_values)
        self.value = value
        self.possible_values = set({}) # empty set
        self.board.assigned_cells += 1
        print('assignment [{}]: {} to cell {}, {}'.format(self.board.assigned_cells, value, self.row.group_number, self.column.group_number))
        if self.board.assigned_cells == 81:
            print("Done!")
            return
        self.row.no_longer_needs(value)
        self.column.no_longer_needs(value)
        self.grid.no_longer_needs(value)
        # check every cell, this is pretty brute force
        # set it recursively
        for c in self.board.cells:
            if not c.is_empty():
                continue
            # for this cell - is there only one option?
            possible = c.possible_values
            row_set = c.row.needs()
            col_set = c.column.needs()
            grid_set = c.grid.needs()
            final = possible & row_set & col_set & grid_set
            if len(final) == 1:
                print('      > cell {}, {} can only be {}'.format(c.row.group_number, c.column.group_number, final))
                c.set_value(final.pop())
                break

    def set_groups(self, row, col, grid):
        self.row = row
        self.column = col
        self.grid = grid

    def is_empty(self):
        return (self.value is None)

    def __str__(self):
        return str(self.value) if self.value is not None else "empty"
