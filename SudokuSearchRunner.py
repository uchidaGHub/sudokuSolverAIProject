import time

from final_project.DeapthFirstSearch import DepthFirstSearch
from final_project.Sudoku import Sudoku
from final_project.SudokuSearch import SudokuSearchState

# Add or remove file names from here to run DFS on different set of Sudoku puzzles.
list_sudoku_txt = [
    "sudoku_easy1.txt",
    "sudoku_easy2.txt",
    "sudoku_medium1.txt",
    "sudoku_medium2.txt",
    "sudoku_hard1.txt",
    "sudoku_hard2.txt",
    "sudoku_extreme1.txt",
    "sudoku_extreme2.txt",
    "sudoku_master1.txt",
    "sudoku_master2.txt",
    "sudoku_extreme1.txt",
    "sudoku_extreme2.txt"
]
total_runtime = 0

for sudoku_txt in list_sudoku_txt:
    print(sudoku_txt)
    sudoku_obj = Sudoku()
    sudoku_obj.load_from_txt("sudoku_dataset/" + sudoku_txt)

    start_time = time.perf_counter()

    sudoku_displayer = None  # SudokuGui(sudoku_obj.get_grids_filled())
    sudoku_search = SudokuSearchState(sudoku_obj.get_grid())
    dfs_runner = DepthFirstSearch(sudoku_search, sudoku_displayer, gui_flag=False)
    path = dfs_runner.search()
    print(path)

    end_time = time.perf_counter()

    print(end_time - start_time)
    total_runtime += end_time - start_time
    print()