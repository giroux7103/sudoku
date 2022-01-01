

import cell
import itertools
import random
import history


class SudokuGroup():

    def __init__(self, num, type):
        self.need_values = set({1,2,3,4,5,6,7,8,9})
        self.group_number = num
        self.group_type = type
        self.data = []

    def needs(self):
        return self.need_values

    def now_needs(self, value):
        self.need_values.add(value)
        for c in self.data:
            c.possible_values.add(value)

    def no_longer_needs(self, value):
        self.need_values.discard(value)
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
        self.move_hist = history.MoveTracker()
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

    def check_single_option(self):
        for acell in self.cells:
            groups = [acell.row, acell.column, acell.grid]
            for group in groups:
                final = set()
                possible = set()
                for group_cell in group.data:
                    if group_cell.key != acell.key:
                        possible |= group_cell.possible_values
                final |= group.need_values - possible
                if len(final) == 1:
                    acell.set_value(final.pop(), is_chained=True)

    def fill(self, val=None):
        if val is None:
            vals = [1,2,3,4,5,6,7,8,9]
        else:
            vals = [val]
        for v in vals:
            for r in self.rows:
                for x in random_cols():
                    c = r.get_cells()[x]
                    if v in c.possible_values:
                        c.set_value(v)
                        break

def random_cols():
    init = [0,1,2,3,4,5,6,7,8]
    result = []
    for i in range(9):
        x = random.choice(init)
        result.append(x)
        init.remove(x)
    return result



def create_empty_board(seed_func=None):
    return SudokuBoard()

def create_random_board(seed_func=None):
    s = SudokuBoard()
    try:
        s.fill()
    except Exception as e:
        print(e)
        pass
    return s


#b = create_empty_board()
#try:
#    b.random_fill()
#except Exception as e:
#    print(e)
#    pass

#print("Move History:")
#print(b.move_hist)

#print("\n\nBoard:")
#print(b)
