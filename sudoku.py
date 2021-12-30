

import cell
import itertools
import random


class SudokuGroup():

    def __init__(self, num, type):
        self.need_values = set({1,2,3,4,5,6,7,8,9})
        self.empty_cells = 9
        self.group_number = num
        self.group_type = type
        self.data = []

    def needs(self):
        return self.need_values

    def no_longer_needs(self, value):
        self.need_values.discard(value)
        self.empty_cells -= 1
        #print('     > {} now only needs {}'.format(self.group_type, self.need_values))
        for c in self.data:
            c.possible_values.discard(value)

    def append_cell(self, c):
        assert(isinstance(c, cell.Cell))
        self.data.append(c)

    def get_cells(self):
        return self.data

    def __str__(self):
        return ",".join(map(str, self.data)) + "\n"



class SudokuBoard():

    def __init__(self):
        self.cells = []
        self.assigned_cells = 0
        self.rows = [SudokuGroup(i, 'row') for i in range(9)]
        self.cols = [SudokuGroup(i, 'column') for i in range(9)]
        self.grids = [SudokuGroup(i, 'grid') for i in range(9)]

        for i in range(81):
            c = cell.Cell(i)
            c.board = self
            self.cells.append(c)
            self.grids[c.grid_num].append_cell(c)
            self.rows[c.row_num].append_cell(c)
            self.cols[c.column_num].append_cell(c)
            c.row = self.rows[c.row_num]
            c.column = self.cols[c.column_num]
            c.grid = self.grids[c.grid_num]


    def __str__(self):
        result = ""
        for r in self.rows:
            result += str(r)
        return result

    def random_fill(self):
        cell_key = 0
        while self.assigned_cells < 81:
            acell = self.cells[cell_key]
            if acell.is_empty():
                rvalue = random.choice(list(acell.possible_values))
                acell.set_value(rvalue)
                cell_key += 13
                if cell_key > 80:
                    cell_key = cell_key - 81
            else:
                cell_key += 1


def create_empty_board(seed_func=None):
    return SudokuBoard()


b = create_empty_board()
try:
    b.random_fill()
except Exception as e:
    print(e)
    pass

print(b)
