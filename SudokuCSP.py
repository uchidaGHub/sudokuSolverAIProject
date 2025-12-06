import random

from final_project.CSP import CSP
from final_project.Sudoku import Sudoku


class SudokuCSP(CSP):
    """
    Represents formulation of Sudoku as a CSP. In this class, variables are row and column of position in the Sudoku
    board. Note that positions that are filled by default are NOT included. Values are number to be filled in this
    position.

    In ths class,
        var ((int, int)): Position within the grid
        val (int): Integer to fill.

    Attrs:
        board (Sudoku): Sudoku board represented in this CSP.
        assignments (dict): Dictionary which represents variables and assignment to them. In this class:
            Key ((int, int)): Row and column of position in the Sudoku board. Note that positions that are filled by
                default are NOT included.
            Val (int): Number to be filled in this position.
    """
    def __init__(self, sudoku_obj):
        """
        Create the search problem of Sudoku. Load the board, if given one. Create list of variables as a key of
        dictionary, contains all positions of empty grid.

        Args:
            sudoku_obj (Sudoku): If defined, self.board will be set directly to it.
        """
        self.board = sudoku_obj
        self.assignments: dict[(int, int), None or int] = dict()

        grid_filled = self.board.get_grids_filled()

        for idx_row in range(9):
            for idx_col in range(9):
                if not grid_filled[idx_row][idx_col]:
                    self.assignments[(idx_row, idx_col)] = None

    def get_current_assignments(self):
        """
        OVERRIDE from CSP
        """
        return self.assignments.copy()

    def get_variables(self):
        """
        OVERRIDE from CSP

        Return:
            ((int, int)): List of grid positions that are not filled by default.
        """
        return list(self.assignments.keys())

    def get_possible_values(self, var):
        """
        OVERRIDE from CSP
        Possible values are integers between 1 and 9.

        Args:
            var ((int, int)): Position within the grid.
        """
        return [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def is_complete(self):
        """
        OVERRIDE from CSP
        Return True if no values in dictionary of assignments is None.
        """
        for var in self.assignments.keys():
            if self.assignments[var] is None:
                return False

        return True

    def assign(self, var, val):
        """
        OVERRIDE from CSP
        Fill the given position of grid with a given digit.

        Args:
            var ((int, int)): Position within the grid.
            val (int): Digit to assign.
        """
        self.assignments[var] = val

    def assign_all(self):
        """
        Get a Sudoku object of when all assignment of variables are reflected.

        Return:
            (Sudoku): Sudoku object with all assignments reflected.
        """
        sudoku_obj = self.board.copy()

        for row, col in self.assignments.keys():
            digit = self.assignments[(row, col)]

            if digit is not None:
                sudoku_obj.add_digit_to_pos(row, col, digit)

        return sudoku_obj

    def get_weight(self):
        """
        OVERRIDE from SCP
        Weight will be 1 if current assignment produces a valid Sudoku. 0, if not.
        """
        sudoku_temp = self.assign_all()

        if sudoku_temp.is_valid():
            return 1
        else:
            return 0

    def get_valid_values(self, var):
        """
        OVERRIDE from CSP
        Get all values that can be placed on the position given as a variable.

        Args:
            var ((int, int)): Position within the Sudoku grid to check.

        Return:
            (list[int]): List of digits that can be placed.
        """
        list_vals = self.get_possible_values(var)
        list_valid_digits = list()
        row, col = var

        for digit in list_vals:
            sudoku_temp = self.assign_all()
            sudoku_temp.add_digit_to_pos(row, col, digit)

            if sudoku_temp.is_valid():
                list_valid_digits.append(digit)

        return list_valid_digits

    def get_affected_vars(self, var):
        """
        OVERRIDE from CSP
        In this case, affected values are all horizontal, vertical, and in same 3 * 3 block of the grid.
        """
        row, col = var
        list_affected_vars = list()
        block_idx_row = row // 3
        block_idx_col = col // 3

        for other_row, other_col in self.assignments.keys():
            if other_row != row or other_col != col:
                if other_row == row or other_col == col:
                    list_affected_vars.append((other_row, other_col))
                elif other_row // 3 == block_idx_row and other_col // 3 == block_idx_col:
                    list_affected_vars.append((other_row, other_col))

        return list_affected_vars

    def unassigned_vars(self):
        """
        OVERRIDE from CSP
        """
        list_unassigned_vars = list()

        for var in self.assignments.keys():
            if self.assignments[var] is None:
                list_unassigned_vars.append(var)

        return list_unassigned_vars

    def lookahead(self, var):
        """
        OVERRIDE from CSP
        """
        list_dependent_vars = self.get_affected_vars(var)
        list_domains = list()

        for another_var in list_dependent_vars:
            domains = self.get_valid_values(another_var)
            list_domains.append(domains)

        return list_domains

    def get_assigned_object(self):
        """
        OVERRIDE from CSP

        Return:
            (np.array): 9 * 9 grid of Sudoku board when current assignments are actually placed.
        """
        sudoku_temp = self.assign_all()

        return sudoku_temp.get_grid()

    def assign_random(self):
        """
        OVERRIDE from SCP
        """
        for var in self.assignments.keys():
            list_vals = self.get_possible_values(var)
            self.assignments[var] = random.choice(list_vals)

    def remove_assignment(self, var):
        """
        OVERRIDE from CSP
        """
        self.assignments[var] = None

    def increment(self, dict_index, max_index):
        """
        Increment dictionary of index by adding the value of first entry by 1. If doing so would result it to go over
        given maximum value, then reset it to 0, and increment the value of second entry, and so on. If last element would
        go over the limit, then return None.

        Args:
            dict_index (dict[Any, int]): Current index.
            max_index (dict[Any, int]): Maximum index for each entry.

        Return:
            (dict[Any, int] or None): Incremented dictionary, or None if given is the maximum.
        """
        num_vars = len(dict_index.keys())
        new_dict = dict_index.copy()

        for i in range(num_vars):
            key = list(dict_index.keys())[i]
            max_val = max_index[key]
            next_val = dict_index[key] + 1

            if next_val < max_val:
                new_dict[key] += 1

                return new_dict
            else:
                new_dict[key] = 0

        return None

    def get_permutations(self, dict_possible_values):
        """
        Return list of all combinations of values for each variable.

        Args:
            dict_possible_values (dict[Any, list]): Dictionary which store name of variables and list of values that
                can be assigned to each.

        Return:
            (list[dict]): List of all combinations of values to each variable. Each element in the list is mapping of name
                of the variable to assignment of value.
        """
        list_permutations = list()
        dict_index = dict()
        max_index = dict()

        for var in dict_possible_values.keys():
            dict_index[var] = 0
            max_index[var] = len(dict_possible_values[var])

        while True:
            dict_comb = dict()

            for var in dict_possible_values.keys():
                idx_var = dict_index[var]
                dict_comb[var] = dict_possible_values[var][idx_var]

            list_permutations.append(dict_comb)
            dict_index = self.increment(dict_index, max_index)

            if dict_index is None:
                return list_permutations

    def get_score_after(self, list_var):
        """
        OVERRIDE from CSP
        """
        dict_possible_values = dict()

        for var in list_var:
            self.remove_assignment(var)
            dict_possible_values[var] = self.get_possible_values(var)

        list_val_score: list[tuple[dict, int]] = list()
        list_value_combinations = self.get_permutations(dict_possible_values)

        for val_comb in list_value_combinations:
            sudoku_temp = self.assign_all()

            for var in list(val_comb.keys()):
                row, col = var
                val = val_comb[var]
                sudoku_temp.add_digit_to_pos(row, col, val)

            if sudoku_temp.is_valid():
                list_val_score.append((val_comb, 1))
            else:
                list_val_score.append((val_comb, 0))

        return list_val_score

    def copy(self):
        """
        OVERRIDE from CSP
        """
        sudoku_new = self.board.copy()
        sudoku_new.set_grid(self.board.get_grid())
        csp_new = SudokuCSP(sudoku_new)

        for var, val in self.assignments.items():
            csp_new.assign(var, val)

        return csp_new

    def get_if_score(self, list_vars, list_vals):
        """
        OVERRIDE from CSP
        """
        sudoku_obj = self.assign_all()

        for idx in range(len(list_vars)):
            row, col = list_vars[idx]
            digit = list_vals[idx]
            sudoku_obj.add_digit_to_pos(row, col, digit)

        if sudoku_obj.is_valid():
            return 1
        else:
            return 0

    def assign_multiple(self, list_vars, list_val):
        """
        OVERRIDE from CSP
        """
        for idx in range(len(list_vars)):
            var = list_vars[idx]
            val = int(list_val[idx])
            self.assign(var, val)

    def get_invalid_vars(self):
        """
        OVERRIDE form CSP
        """
        list_invalid_vars_idx = list()
        sudoku_temp = self.assign_all()

        for r, c in self.get_variables():
            if not sudoku_temp.valid_placement((r, c)):
                list_invalid_vars_idx.append((r, c))

        return list_invalid_vars_idx
