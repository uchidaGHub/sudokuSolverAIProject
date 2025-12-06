from final_project.SudokuCSP import SudokuCSP


class SudokuLocalSearch(SudokuCSP):
    """
    Special Class for Sudoku CSP which weight calculation is designed in the way that is suitable for local search.
    """
    def __init__(self, sudoku_obj):
        """
        OVERRIDE from SudokuCSP
        """
        super().__init__(sudoku_obj)

    def get_weight(self):
        """
        In this case, weight is calculated as total number of valid rows, columns, and squares.
        If the whole board is valid, then the weight will be 27.
        """
        sudoku_temp = self.assign_all()
        return sudoku_temp.get_score()

    def get_score_after(self, list_var):
        """
        OVERRIDE from CSP
        """
        csp_temp = self.copy()
        dict_possible_values = dict()

        for var in list_var:
            csp_temp.remove_assignment(var)
            dict_possible_values[var] = csp_temp.get_possible_values(var)

        list_val_score: list[tuple[dict, int]] = list()
        list_value_combinations = self.get_permutations(dict_possible_values)

        for val_comb in list_value_combinations:
            sudoku_temp = csp_temp.assign_all()

            for var in list(val_comb.keys()):
                row, col = var
                val = val_comb[var]
                sudoku_temp.add_digit_to_pos(row, col, val)

            score = sudoku_temp.get_score()
            list_val_score.append((val_comb, score))

        return list_val_score

    def get_if_score(self, list_vars, list_vals):
        """
        OVERRIDE from CSP
        """
        sudoku_obj = self.assign_all()

        for idx in range(len(list_vars)):
            row, col = list_vars[idx]
            digit = list_vals[idx]
            sudoku_obj.add_digit_to_pos(row, col, digit)

        return sudoku_obj.get_score()

