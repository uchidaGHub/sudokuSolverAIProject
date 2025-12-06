import random

from final_project.SudokuLocalSearch import SudokuLocalSearch


class SudokuLocalSearchBlocks(SudokuLocalSearch):
    """
    Represents a class which runs local search, while remaining the block constraints.
    Block: Integer 0 - 8, current block of the sudoku to process. Defined as:
            0 1 2
            3 4 5
            6 7 8

    Attrs:
        prev_swapped_vars (int): List of previously swapped variables.
    """
    def __init__(self, sudoku_obj):
        """
        OVERRIDE from SudokuCSP
        """
        super().__init__(sudoku_obj)
        self.prev_swapped_vars = None

    def get_block_idx(self, pos):
        """
        Given (x, y), determine which blocks it is in.

        Args:
            pos ((int, int)): Position to check

        Return:
            (int): Block index according to definition above.
        """
        r, c = pos

        return (r // 3) * 3 + (c // 3)

    def assign_random(self):
        """
        OVERRIDE from CSP

        Assign randomly, but each blocks must satisfy block constraints.
        """
        sudoku_obj = self.board.copy()

        for pos_r, pos_c in self.get_variables():
            block_idx = self.get_block_idx((pos_r, pos_c))
            list_valid_values = sudoku_obj.get_nums_not_in_block(block_idx)
            digit = random.choice(list_valid_values)
            sudoku_obj.add_digit_to_pos(pos_r, pos_c, digit)
            self.assign((pos_r, pos_c), digit)

    def get_var_in_block(self, block_idx):
        """
        Get list of variables that are in the given block index.

        Args:
            (int): Block index

        Return:
            (list[int, int]): Get list of variables in this csp_prob that are in given block index.
        """
        list_var_in_block = list()

        for var in self.get_variables():
            r, c = var

            if (r // 3) * 3 + c // 3 == block_idx:
                list_var_in_block.append(var)

        return list_var_in_block

    def swap_two_vars(self, var1, var2, track=True):
        """
        Swap assignments of two given variables.

        Args:
            var1, var2 ((int, int)): Variables to swap values of.
            track (bool): If given True, change self.prev_swapped_vars
        """
        val1 = self.get_current_assignments()[var1]
        val2 = self.get_current_assignments()[var2]
        self.assign(var1, val2)
        self.assign(var2, val1)

        if track:
            self.prev_swapped_vars = (var1, var2)

    def swap(self, block_idx):
        """
        Swap random two invalid assignments to variables within the given block. If given block has less than one
        invalid variable, do nothing.

        Args:
            block_idx (idx) = Block index

        Return:
            (bool): Return true if values were swapped. False, if not.
        """
        list_var_in_block = self.get_var_in_block(block_idx)

        if len(list_var_in_block) < 2:  # nothing to do
            return False

        max_if_score = 0
        var_to_swap = None

        for idx1 in range(len(list_var_in_block) - 1):
            for idx2 in range(idx1 + 1, len(list_var_in_block)):
                var1 = list_var_in_block[idx1]
                var2 = list_var_in_block[idx2]
                self.swap_two_vars(var1, var2, track=False)
                if_score = self.get_weight()

                if if_score > max_if_score:
                    max_if_score = if_score
                    var_to_swap = (var1, var2)

                self.swap_two_vars(var1, var2, track=False)

        var1, var2 = var_to_swap
        self.swap_two_vars(var1, var2)

        return True

    def undo(self):
        """
        Swap two variables that are previously swapped.
        """
        var1, var2 = self.prev_swapped_vars
        self.swap_two_vars(var1, var2)

