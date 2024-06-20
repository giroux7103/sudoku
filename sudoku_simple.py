

import random
import logging
import sys

formatter = logging.Formatter("%(levelname)-5.5s - %(message)s")
logger = logging.getLogger("Simple Sudoku")
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)
global_err_count = 0

# global board - just a 9x9 grid all initialized to 0 (unset cell)
board = [[0 for i in range(9)] for i in range(9)]

# global grid containing the set of runes each cell is allowed to have
# at first, this will be any rune 1-9
cell_can_have = [[set([1,2,3,4,5,6,7,8,9]) for i in range(9)] for i in range(9)]

# helpful structure to create lists of row/column coordinates for each "box"
# box numbers run from 0 to 8 with 0 being the top left and proceding in reading order
# (left to right, top to bottom)
box_coords = []
box_coords.append([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]) #0
box_coords.append([(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)]) #1
box_coords.append([(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)]) #2
box_coords.append([(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)]) #3
box_coords.append([(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)]) #4
box_coords.append([(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)]) #5
box_coords.append([(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)]) #6
box_coords.append([(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)]) #7
box_coords.append([(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)]) #8

# the move auditing structure holds a record of each
# move made (column selected for a particular rune on a particular row)
# it also holds a special list of "bad" moves so that we can exclude those
# and not repeat the same bad move over again
move_audit = [] # list of moves

# initialize move_audit with every possible move (81 of them)
# no position (column) set yet, just which rune and ordering the
# rows from top to bottom to randomly set that rune
random_runes = [1,2,3,4,5,6,7,8,9]
while len(random_runes) > 0:
    rune = random.choice(random_runes)
    random_runes.remove(rune)
    for row in range(9):
        move_audit.append({"rune":rune, "row":row, "col": None, "bad_cols": []})

def print_board():
    print("\nFinal board:")
    for row in range(9):
        print(board[row])

def print_moves():
    for move in move_audit:
        print(move)

def get_box(x, y):
    # you could use math to figure this out as well
    # but there is only 9 possible boxes
    if x <= 2:
        if y <= 2:
            return 0
        elif y <= 5:
            return 1
        else:
            return 2
    elif x <= 5:
        if y <= 2:
            return 3
        elif y <= 5:
            return 4
        else:
            return 5
    else:
        if y <= 2:
            return 6
        elif y <= 5:
            return 7
        else:
            return 8

def get_available_spaces(move_index):
    # important function used to determine for a given move (rune/row)
    # which columns can contain the rune
    # important to remove "bad" column positions previously set, but ended up
    # causing something bad later
    result = []
    row = move_audit[move_index]["row"]
    rune = move_audit[move_index]["rune"]
    for col in range(9):
        if board[row][col] == 0 and rune in cell_can_have[row][col]:
            result.append(col)
    for bad_col in move_audit[move_index]["bad_cols"]:
        result.remove(bad_col)
    return result


def get_runes_in_row(row):
    result = set()
    for col in range(9):
        if board[row][col] != 0:
            result.add(board[row][col])
    return result

def get_runes_in_col(col):
    result = set()
    for row in range(9):
        if board[row][col] != 0:
            result.add(board[row][col])
    return result

def get_runes_in_box(box):
    result = set()
    for row, col in box_coords[box]:
        if board[row][col] != 0:
            result.add(board[row][col])
    return result

def reset_cells_can_have():
    # brute force reset all cell_can_have values
    # this could definitely be improved
    for row in range(9):
        for col in range(9):
            box = get_box(row, col)
            already_set = set()
            already_set |= get_runes_in_row(row)
            already_set |= get_runes_in_col(col)
            already_set |= get_runes_in_box(box)
            cell_can_have[row][col] = set([1,2,3,4,5,6,7,8,9]) - already_set


def unset_value(move_index):
    # this function unsets a cell that was previously set
    # using the move_audit and the index passed, we can find the
    # row/column/rune and unset it back to 0 (unset).
    # then we need to re-calculate the cell_can_have structure
    # to make sure all cells are reporting the correct values
    # thay can possibly have.
    # we also need to reset all "bad" moves for any moves after this one
    # because as we keep going backwards to re-select another random spot
    # we can't rely on bad moves past this one

    global global_err_count
    global_err_count += 1
    row = move_audit[move_index]["row"]
    col = move_audit[move_index]["col"]

    board[row][col] = 0
    
    # can't blindly add rune back to row/col/box
    # need to build the availability
    reset_cells_can_have()

    move_audit[move_index]["bad_cols"].append(col)
    #print(f"move at index {move_index} using col {col} was bad.  Values tried and failed {move_audit[move_index]['bad_cols']}")
    
    #clear out subsequent bad cols if they exist
    for move in move_audit[move_index+1:]:
        move["bad_cols"] = []
    
    
def set_value(move_index, col):
    # set a value and record it on the board
    # given the current move (move_index) we can lookup the row and rune
    # and the col (column) passed that should have been randomly selected from
    # the fill_board() function
    # Once the board has been set, we update all "affected" cell_can_have
    # values for the assocaiated cells in the same row/column/box
    
    row = move_audit[move_index]["row"]
    rune = move_audit[move_index]["rune"]
    
    move_audit[move_index]["col"] = col
    board[row][col] = rune
    for x in range(9): 
        cell_can_have[row][x].discard(rune)
        cell_can_have[x][col].discard(rune)
    box = get_box(row, col)
    for r,c in box_coords[box]:
        cell_can_have[r][c].discard(rune)


def fill_board():
    # algorithm will use the move_audit which randomly chooses
    # a rune and goes through each ROW from top to bottom for 81 total moves.
    # This function will randomly select a COLUMN to place that
    # rune and keep track of the move
    # if we get to a situation where a row has no possible options
    # we know somewhere in the past we picked a "bad" move
    # so - we go back to the previous move, unset it and try again
    # the unset_value function will "remember" which previous selections were bad
    # and therefore not pick them again.  This will continue to "wobble" back up and down
    # as many moves as necessary until it eventually works out

    current_move = 0
    while current_move < len(move_audit):
        row = move_audit[current_move]["row"]
        rune = move_audit[current_move]["rune"]
        spaces = get_available_spaces(current_move)
        bad_moves = move_audit[current_move]['bad_cols']
        # get the available spaces (columns) of the row
        if len(spaces) > 0:
            # randomly choose one
            col = random.choice(spaces)
            #print(f"move {current_move}, rune {rune}, row {row} - available cols: {spaces} - ignore bad selections: {bad_moves} -> selected {col}")
            logger.info(f"move {current_move}, rune {rune}, row {row} - available cols: {spaces} - ignore bad selections: {bad_moves} -> selected {col}")
            set_value(current_move, col)
            current_move += 1
        else:
            # Current row has no available spaces, roll back previous move 
            #print(f"move {current_move} unsetting previous move - no available moves for rune {rune} on row {row}")
            logger.info(f"move {current_move} unsetting previous move - no available moves for rune {rune} on row {row}")
            current_move -= 1
            unset_value(current_move)

if __name__ == "__main__":
    try:
        fill_board()
    finally:
        print_board()
    print(f"\nNumber of moves retried: {global_err_count}")