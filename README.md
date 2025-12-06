# sudokuSolverAIProject

This is a repository which stores code and datasets used for sudoku solver program using AI algorithm. Uses search and CSP to solve Sudoku puzzles.

In this project, I have obtained a Sudoku puzzle dataset from “Sudoku.com” (www.Sudoku.com), and manually written text document of initial state of sudoku board. I have written a program in python which converts these text documents into Sudoku object that is suitable for running AI algorithms. 

The website defines different difficulties for Sudoku puzzle, from easiest to hardest, difficulties are named as: “easy”, “medium”, “hard”, “expert”, “master”, and “extreme”. Number of initially empty squares increases as the difficulty increase, and I have obtained two Sudoku data for each difficulty classes. 

Sudoku object is an object class that I created in python and contains 2D array which represents digits placement on each grid. The empty grid is represented as 0. The interaction with Sudoku board defined in this class includes obtaining current grid placements, placing a digit on next empty grid or any given grid, checking weather there exists any empty grids within the board, and weather the current placement of digits violates any Sudoku constraints.

For note, all programs are implemented by hand, and I did not use any outside library which helps me doing the algorithm, other than NumPy. 


## About code files:
“CSP.py”: The code which stores interface for CSP object class, and stores operations it can perform.

“CSPRunner.py”: The file which contains main program to run backtracking search and both versions of local search on Sudoku CSP problem.

“DepthFirstSearch.py”: Stores class which store operations of “SearchAlgo” interface which is unique to DFS.

“SearchAlgorithm.py”: Stores class which implements operations for search algorithm. 

“SearchGui.py”: Stores class which is responsible for displaying information as GUI during the search process.

“SearchProb.py”: Stores interface for search problem, which contains operations performed by SearchProb class.

“Sudoku.py”: Stores Sudoku class, which represents the Sudoku puzzle and will be used in various search algorithms.

“SudokuCSP.py”: Stores class which represented Sudoku problem as CSP.

“SudokuLocalSearch.py”: Stores a class which contains operations of “SudokuCSP” that works differently or is unique in local search.

“SudokuLocalSearchBlocks.py”: Stores a class which contains operations of “SudokuLocalSearch” that works differently or is unique in block-based local search.

“SudokuSearch.py”: Stores class for Sudoku puzzle converted to Search Problem, and operations necessary to solve it.

“SudokuSearchRunner.py”: Stores program to run the algorithm which solves Sudoku puzzle using DFS. 

All sample Sudoku text files are located in “sudoku_dataset” folder.

## Running Codes:
“SudokuSearchRunner.py”: 

Without changing anything, it runs DFS to solve Sudoku puzzles saved in this directory. Add or remove file names from “list_sudoku_txt” to run different set of Sudoku puzzles.

“CSPRunner.py”: 
-	“run_backtracking”: Runs backtracking search on given list of Sudoku puzzles. Add or remove file names from “list_sudoku_txt” to run different set of Sudoku puzzles. 
-	“run_local_search_modified”: Runs block-based local search on Sudoku puzzle on given file name. This function will terminate when maximum score of 27 is reached, or given number of iterations are passed. And prints the maximum score achieved, and optimal assignment which gave that maximum score.
-	“run_local_search_data”: Also runs block-based local search on Sudoku puzzle on given file name. This function will always run to given number of iterations. prints average score achieved throughout the search, and percentage of converging to score 27 during the search. 
-	NOTE: The “run_local_search” function will run non-block-based local search, but might encounter an error since I have not tested it since implementation of block-based local search. 

