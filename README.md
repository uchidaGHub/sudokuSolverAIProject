# sudokuSolverAIProject

This is a repository which stores code and datasets used for sudoku solver program using AI algorithm. Uses search and CSP to solve Sudoku puzzles.

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

