import numpy as np


def same_digits(list_digits):
    """
    Given a list of digits, verify that it does not contain repeated digits 1 - 9. Ignore any 0's.

    Args:
        list_digits (list(int)): List of digits between 0 and 9.

    Return:
        (bool): True, if there are no repeated 1 - 9. False, if there is.
    """
    list_digits_new = list()

    for digit in list_digits:
        list_digits_new.append(int(digit))

    for idx in range(len(list_digits_new)):
        digit = list_digits_new[idx]

        if digit != 0:
            for another_digit in list_digits_new[idx+1:]:
                if another_digit == digit:
                    return True

    return False


def get_digits_square(x_start, y_start, grid):
    """
    Return list of digits in 3 by 3 square group starting from given position of given grid.

    Args:
        x_start (int): x position of top left of the 3 by 3 square.
        y_start (int): y position of top left of the 3 by 3 square.
        grid (np.array): A grid to process.

    Return:
        (list(int)): List of digits in the 3 by 3 square.
    """
    list_digits = list()

    for i in range(x_start, x_start + 3):
        for j in range(y_start, y_start + 3):
            list_digits.append(grid[i][j])

    return list_digits


class Sudoku:
    """
    Class which represent the board of Sudoku puzzle.

    Attrs:
        grid (np.array[][]): 2D array of integers which represents how digits are filled in the Sudoku board.
            - Size of the array is 9 by 9.
            - Index of outer array represents row, and index of inner array represents column. For example, index [i][j]
                means row i and column j, starting from the top left corner.
            - Each entry of the array is a single digit: 0 - 9. 1 - 9 represents digit that this entry is filled with.
                0 represents an empty entry.

        displayer (SudokuGui): GUI object to display current Sudoku board.
    """
    def __init__(self):
        """
        Initialize to empty Sudoku board.
        """
        list_col = list()

        for i in range(9):
            list_row = list()

            for j in range(9):
                list_row.append(0)

            list_col.append(list_row)

        self.grid = np.array(list_col)

    def get_grid(self):
        """
        Return 2d array of current grid.

        Return:
            (np.array): Array representing a grid.
        """
        return self.grid

    def is_valid(self):
        """
        Given a grid, determine whether it satisfies all conditions for Sudoku.
            (1) Size is 9 by 9. (2) All entries are integers 0 to 9. (3) No same digits in same row.
            (4) No same digits in same column. (5) No same digits in 3 by 3 square group.
            Note: conditions (3), (4), and (5) does not apply to digit 0.

        Args:
            grid (np.array): Array to check if it is a valid Sudoku grid.

        Return:
            (bool): True, if it satisfies all above conditions. False, if not.
        """
        if self.grid.shape != (9, 9):
            return False

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] < 0 or self.grid[i][j] > 9:
                    return False

        for i in range(9):
            if same_digits(self.grid[i]):
                return False

            list_col_i = list()

            for j in range(9):
                list_col_i.append(self.grid[j][i])

            if same_digits(list_col_i):
                return False

        for i in range(3):
            for j in range(3):
                list_square_group = get_digits_square(i * 3, j * 3, self.grid)

                if same_digits(list_square_group):
                    return False

        return True

    def load_from_txt(self, file_name):
        """
        Fill in digits to this Sudoku board according to the txt file with given name.

        Args:
            file_name (str): Name of the txt file which contains Sudoku data.
        """
        new_grid = np.genfromtxt(file_name, delimiter=' ')
        self.grid = new_grid

    def get_next_empty_pos(self):
        """
        Get x and y positions of next cell with 0, in increasing order of 10y + x.

        Return:
            (int): x-position of next cell with 0.
            (int): y-position of next cell with 0.
        """
        for idx_x in range(9):
            for idx_y in range(9):
                if self.grid[idx_x][idx_y] == 0:
                    return idx_x, idx_y

    def set_grid(self, grid_to_fill):
        """
        Set grid of this Sudoku to given grid.

        Args:
            grid_to_fill (np.array): Valid grid of Sudoku.
        """
        self.grid = grid_to_fill

    def add_digit_to_pos(self, row, col, digit):
        """
        Return a grid of when the given digit added to given position.

        Args:
            row (int): Row to place the digit.
            col (int): Column to place the digit.
            digit (int): Digit to place.

        Return:
            (np.array): Grid when given digit is placed on given position.
        """
        new_grid = self.grid.copy()
        new_grid[row][col] = digit
        self.grid = new_grid

    def add_digit_to_next_empty(self, digit):
        """
        Fill in digits to next position with digit 0. Position is defined by increasing order of 10y + x.

        Args:
            digit (int): Digit to fill in.

        Return:
            (np.array): Array of grid after given digit has been placed.
            (Sudoku): Sudoku object with given digit added to next position.
            OR
            (None): if addition of given digit results in invalid grid.
        """
        next_x, next_y = self.get_next_empty_pos()
        new_grid = self.grid.copy()
        new_grid[next_x][next_y] = digit

        return new_grid

    def is_complete(self):
        """
        Check if the Sudoku board is complete by checking if all grids are filled.

        Return:
            (bool): True, if all grids are filled with non-zero. False, if not.
        """
        for list_row in self.grid:
            for digit in list_row:
                if digit == 0:
                    return False

        return True

    def board_equals(self, another_board):
        """
        Given another 9 by 9 board, compare if these have same digits filled in same positions.

        Args:
            another_board (np.array): Array of int representing another board.

        Return:
            (bool): True, if two boards are equal. False, if not.
        """
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] != another_board[x][y]:
                    return False

        return True

    def get_grids_filled(self):
        """
        Return array of 9 * 9 grids of booleans, which contains True, if this Sudoku's grid at corresponding position is
        filled with some digits. False, if not.

        Return:
            (np.array): 9 * 9 array of boolean grids which shows positions that are filled with some digits.
        """
        list_grids_filled = list()

        for list_row in self.grid:
            list_grids_filled_row = list()

            for grid_pos in list_row:
                list_grids_filled_row.append(grid_pos != 0)

            list_grids_filled.append(list_grids_filled_row)

        return np.array(list_grids_filled)

    def copy(self):
        """
        Get another Sudoku object which has same attributes as this.

        Return:
            (Sudoku): Sudoku object with same attribute as this.
        """
        sudoku_copy = Sudoku()
        sudoku_copy.set_grid(self.grid)

        return sudoku_copy

    def get_score(self):
        """
        Get total number of valid rows, valid columns, and valid 3 * 3 square groups.

        Return:
            (int): Total score.
        """
        score = 0

        for i in range(9):
            if not same_digits(self.grid[i]):
                score += 1

            list_col_i = list()

            for j in range(9):
                list_col_i.append(self.grid[j][i])

            if not same_digits(list_col_i):
                score += 1

        for i in range(3):
            for j in range(3):
                list_square_group = get_digits_square(i * 3, j * 3, self.grid)

                if not same_digits(list_square_group):
                    score += 1

        return score

    def valid_placement(self, pos):
        """
        Check if the digit placed at the given position is valid or not.

        Args:
            pos ((int, int)): Position to check if placed digit is valid.
        """
        row, col = pos
        digit = self.grid[row][col]

        for i in range(9):
            if i != row:
                if self.grid[i][col] == digit:
                    return False

            if i != col:
                if self.grid[row][i] == digit:
                    return False

        block_row = row // 3
        block_col = col // 3

        for i in range(3):
            for j in range(3):
                r = 3 * block_row + i
                c = 3 * block_col + j

                if r != row or c != col:
                    if self.grid[r][c] == digit:
                        return False

        return True

    def get_nums_not_in_block(self, block_idx):
        """
        Get all digits 1 - 9 that are not placed in given block index.

        Args:
            block_idx (int): Index of block to check.

        Return:
            list_digit_in_block (list[int]): List of digits not placed on the block.
        """
        list_digits_in = list()
        r_start = (block_idx // 3) * 3
        c_start = (block_idx % 3) * 3

        for i in range(3):
            for j in range(3):
                digit = self.grid[r_start + i][c_start + j]
                list_digits_in.append(digit)

        list_digits_not_in = list()

        for i in range(1, 10):
            if i not in list_digits_in:
                list_digits_not_in.append(i)

        return list_digits_not_in
