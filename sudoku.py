




class Cell():
    
    def __init__(self, row, col):
        self._available_runes = set([1,2,3,4,5,6,7,8,9])
        self._value = None



class SudokuSlice():

    def __init__(self) -> None:
        self._cells = []
        self._needed_runes = set([1,2,3,4,5,6,7,8,9])

    def add_cell(self, cell):
        self._cells.append(cell)


class SudokuRow(SudokuSlice):

    def __init__(self) -> None:
        super().__init__()

class SudokuColumn(SudokuSlice):

    def __init__(self) -> None:
        super().__init__()

class SudokuBox(SudokuSlice):

    def __init__(self) -> None:
        super().__init__()


class SudokuBoard():

    def __init__(self) -> None:
        self._rows = [SudokuRow() for i in range(9)]
        self._cols = [SudokuColumn() for i in range(9)]
        self._boxes = [SudokuBox() for i in range(9)]


    def get_row(self, row_number):
        # for indexes - subtract 1
        return self._rows[row_number-1]
    
    def get_col(self, col_number):
        return self._cols[col_number-1]
    
    def get_box(self, box_number):
        return 

    def __str__(self):
        return "Hello, World!"




myboard = SudokuBoard()

print(myboard)