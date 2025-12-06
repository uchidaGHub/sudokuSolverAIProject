from final_project.SearchProb import SearchState
from final_project.Sudoku import Sudoku


class SudokuSearchState(SearchState):
    """
    Represents state of the Sudoku search problem. Object which represents the state will be the board of the Sudoku.

    Attrs:
        sudoku_obj (Sudoku): Sudoku object which represents current state.
    """
    def __init__(self, grid):
        """
        Create the search state of Sudoku by loading the given Sudoku object.

        Args:
            grid (np.array): Array represents assignment of numbers to Sudoku board of current state.
        """
        sudoku_obj = Sudoku()
        sudoku_obj.set_grid(grid)
        self.board = sudoku_obj

    def get_current_state(self):
        """
        OVERRIDE from SearchProb
        In this class, return the 9 * 9 grid of the Sudoku board.
        """
        return self.board.get_grid()

    def get_actions(self):
        """
        OVERRIDE from SearchProb
        In this search problem, return list of integers 1 to 9.
        """
        return [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def execute_action(self, action):
        """
        OVERRIDE from SearchProb
        Place given digit in next empty cell of this board. Cost will be 1, if this is valid placement, infinity
        (999999) if not.
        In this case, action is an integer which represents which digit to place on next empty value.
        """
        next_board = self.board.add_digit_to_next_empty(action)
        new_state = SudokuSearchState(next_board)

        if new_state.board.is_valid():
            return new_state, 1
        else:
            return None, 999999

    def is_goal(self):
        """
        OVERRIDE from SearchProb
        Return true, if all grid is filled. False, if not.
        """
        return self.board.is_complete()

    def state_equal(self, another_state):
        """
        OVERRIDE from SearchProb
        Compare each digits in each grid, and return True when all grids are filled with same digits.
        """
        return self.board.board_equals(another_state)
