

import cell
import itertools
import random



class SudokuBoard():

    def __init__(self):
        self.cells = []
        self.rows = [[],[],[],[],[],[],[],[],[]]
        self.cols = [[],[],[],[],[],[],[],[],[]]
        self.grids = [[],[],[],[],[],[],[],[],[]]
        p_row = None
        p_col = None
        p_grid = None
        for i in range(81):
            c = cell.Cell(i)
            c.board = self
            self.cells.append(c)
            self.grids[c.grid].append(c)
            self.rows[c.row].append(c)
            self.cols[c.column].append(c)
            if c.column > 0 and c.column <= 8:
                self.rows[c.row][c.column-1].row_next = c
                if c.column == 8:
                    c.row_next = self.rows[c.row][0]
            if c.row > 0 and c.row <= 8:
                self.cols[c.column][c.row-1].col_next = c
                if c.row == 8:
                    c.col_next = self.cols[c.column][0]
            grid_len = len(self.grids[c.grid])
            if grid_len > 1:
                self.grids[c.grid][grid_len-2].grid_next = c
                if grid_len == 9:
                    c.grid_next = self.grids[c.grid][0]


    def __str__(self):
        result = ""
        for i in self.cells:
            result += str(i) + ","
        return result

    def random_fill(self):
        for acell in self.cells:
            rvalue = random.choice(list(acell.possible_values))
            print('assigning {} to cell {}, {}'.format(rvalue, acell.row, acell.column))
            acell.set_value(rvalue)

def create_empty_board(seed_func=None):
    return SudokuBoard()
