

import itertools
import math


class Cell():

    def __init__(self, key):
        self.possible_values = set({1,2,3,4,5,6,7,8,9})
        self.cant_values = set()
        self.key = key
        self.value = None
        self.row_num = math.floor(key / 9)
        self.column_num = (key % 9)
        self.grid_num = math.floor(self.row_num/3) + math.floor(self.column_num/3) + (2*math.floor(self.row_num/3))
        self.board = None
        self.row = None
        self.column = None
        self.grid = None

    def unset_value(self):
        if self.is_empty():
            raise Exception("Unsetting an empty cell [{},{}]".format(self.row_num, self.column_num))
        cur_val = self.value
        self.value = None
        self.cant_values.add(cur_val)
        self.possible_values.add(cur_val)
        self.board.assigned_cells -= 1
        self.row.now_needs(cur_val)
        self.column.now_needs(cur_val)
        self.grid.now_needs(cur_val)

    def set_value(self, value, is_chained=False):
        if value not in self.possible_values:
            raise Exception("Error setting {} to [{},{}] - possibles: {}".format(value, self.row_num, self.column_num, self.possible_values))
        if is_chained:
            self.board.move_hist.add_chain(value, self.row_num, self.column_num)
        else:
            self.board.move_hist.push(value, self.row_num, self.column_num)
        self.value = value
        self.possible_values = set({}) # empty set
        self.board.assigned_cells += 1
        self.row.no_longer_needs(value)
        self.column.no_longer_needs(value)
        self.grid.no_longer_needs(value)

        self.check_related_groups()

        self.board.check_single_option()
        #self.column.check_single_option()
        #self.grid.check_single_option()

    def check_related_groups(self):
        group_nums = set()
        groups = []
        for c in self.row.get_cells():
            if c.row.group_number not in group_nums:
                groups.append(c.row)
                group_nums.add(c.row.group_number)
        for c in self.column.get_cells():
            if c.column.group_number not in group_nums:
                groups.append(c.column)
                group_nums.add(c.column.group_number)
        for c in self.grid.get_cells():
            if c.grid.group_number not in group_nums:
                groups.append(c.grid)
                group_nums.add(c.grid.group_number)
        # got all groups, now check for needing a value but not possible
        possible = set()
        for g in groups:
            for c in g.get_cells():
                possible |= c.possible_values
            if len(g.need_values - c.possible_values) > 0:
                self.unset_value()

    def set_groups(self, row, col, grid):
        self.row = row
        self.column = col
        self.grid = grid

    def is_empty(self):
        return (self.value is None)

    def __str__(self):
        return str(self.value) if self.value is not None else "empty"
