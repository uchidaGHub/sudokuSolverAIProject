import random

import numpy as np

from final_project.CSP import CSP
from final_project.Sudoku import Sudoku
from final_project.SudokuCSP import SudokuCSP
from final_project.SudokuGui import SudokuGui
import time

from final_project.SudokuLocalSearch import SudokuLocalSearch
from final_project.SudokuLocalSearchBlocks import SudokuLocalSearchBlocks


def backtracking_search(csp_prob: CSP, displayer=None):
    """
    Run backtracking search on given CSP problem.

    Args:
        csp_prob (CSP): CSP problem to solve.
        displayer (SudokuGui): Gui object to display current assignments.

    Return:
        (dict): Dictionary of assignments to variables.
    """
    if csp_prob.is_complete():
        return csp_prob.get_current_assignments()

    list_unassigned_vars = csp_prob.unassigned_vars()
    next_var = list_unassigned_vars[0]
    list_valid_vals = csp_prob.get_valid_values(next_var)

    for next_val in list_valid_vals:
        csp_prob.assign(next_var, next_val)

        if displayer is not None:
            time.sleep(0.1)
            displayer.update(csp_prob.get_assigned_object())

        if csp_prob.get_weight() == 0:
            continue

        list_new_domains = csp_prob.lookahead(next_var)
        recurse = True

        for new_domains in list_new_domains:
            if len(new_domains) == 0:
                recurse = False

        if recurse:
            result = backtracking_search(csp_prob, displayer=displayer)

            if result is not None:
                return result

        csp_prob.remove_assignment(next_var)

    return None


def max_score_val(list_value_score: list[tuple[dict, int]]):
    """
    Get the value assignments which given maximum score according to the given list of mappings to assignments and
    score.

    Args:
        list_value_score (list[dict, int]): List of mappings of assignments to score.

    Return:
        Assignments which are mapped to maximum score.
    """
    max_score = 0

    for val_assignment, score in list_value_score:
        if score > max_score:
            max_score = score

    list_assignments = list()

    for val_assignment, score in list_value_score:
        if score == max_score:
            list_assignments.append(val_assignment)

    return random.choice(list_assignments)


def local_search(csp_prob: CSP, converge_strike, num_random_restarts, accept_rate, decay_rate, num_remove,
                 displayer=None):
    """
    Run local search on given CSP problem.

    Args:
        csp_prob (CSP): CSP problem to solve.
        converge_strike (int): The local search will be considered to be converged if weight does not change after
            this number of consecutive iterations.
        num_random_restarts (int): Number of random restarts.
        displayer (SudokuGui): Gui object to display current assignments.
        accept_rate (float): Rate to accept the change when it made the score worse.
        decay_rate (float): Rate to decay the accept rate each time when worse changes are accepted.
        num_remove (int): Number of assignments to remove per time.

    Return:
        (dict): Dictionary of assignments to variables.
        (int): Weight which the optimal assignment will produce.
    """
    list_optimal_assignments = list()

    for i in range(num_random_restarts):
        if i % 10 == 0:
            print(f"Iteration {i}/{num_random_restarts}")

        csp_prob.assign_random()
        list_vars = csp_prob.get_variables()

        if displayer is not None:
            displayer.update(csp_prob.get_assigned_object())

        strike = 0
        crt_weight = 0
        optimal_assignment = None

        while strike < converge_strike:
            num_var_change = num_remove
            list_invalid_vars_idx = csp_prob.get_invalid_vars()
            list_next_idx = np.random.choice(list_invalid_vars_idx, size=num_var_change, replace=False)
            list_next_var = list()
            list_next_val = list()

            for next_idx in list_next_idx:
                var = list_vars[next_idx]
                csp_prob.remove_assignment(var)

            for next_idx in list_next_idx:
                list_next_var.append(list_vars[next_idx])
                list_values = csp_prob.get_possible_values(list_vars[next_idx])
                next_val = np.random.choice(list_values)
                list_next_val.append(next_val)

            if_score = csp_prob.get_if_score(list_next_var, list_next_val)
            accept_p = random.random()

            if if_score > crt_weight:
                strike = 0
                crt_weight = if_score
                csp_prob.assign_multiple(list_next_var, list_next_val)
                optimal_assignment = csp_prob.get_current_assignments()
            elif accept_p <= accept_rate:  # accept
                accept_rate *= decay_rate
                csp_prob.assign_multiple(list_next_var, list_next_val)
            else:  # reject
                strike += 1

            if displayer is not None:
                time.sleep(0.01)
                displayer.update(csp_prob.get_assigned_object())

        print("Itr:", i)
        print("Score", crt_weight)

        list_optimal_assignments.append((optimal_assignment, crt_weight))

    max_weight = 0
    max_weight_idx = 0

    for idx in range(num_random_restarts):
        assignment, weight = list_optimal_assignments[idx]

        if weight > max_weight:
            max_weight = weight
            max_weight_idx = idx

    return list_optimal_assignments[max_weight_idx][0], max_weight


def local_search_single(csp_prob: SudokuLocalSearchBlocks, converge_strike, init_accept_rate, decay_rate,
                        displayer=None):
    """
    Run single iteration of local search.

    Args:
        csp_prob (CSP): CSP problem to solve.
        converge_strike (int): The local search will be considered to be converged if weight does not change after
            this number of consecutive iterations.
        displayer (SudokuGui): Gui object to display current assignments.
        init_accept_rate (float): Rate to accept the change when it made the score worse.
        decay_rate (float): Rate to decay the accept rate each time when worse changes are accepted.

    Return:
        (dict): Optimal variable assignment obtained during this iteration.
        (int): Weight which the optimal assignment will produce.
    """
    csp_prob.assign_random()

    if displayer is not None:
        displayer.update(csp_prob.get_assigned_object())

    strike = 0
    crt_weight = 0
    optimal_assignment = None
    crt_block = 0
    accept_rate = init_accept_rate

    while strike < converge_strike and crt_weight < 27:
        swapped_p = csp_prob.swap(crt_block)
        score = csp_prob.get_weight()
        accept_p = random.random()

        if not swapped_p:
            pass
        elif score > crt_weight:
            strike = 0
            optimal_assignment = csp_prob.get_current_assignments()
            crt_weight = score
            accept_rate = init_accept_rate
        elif accept_p <= accept_rate:  # accept
            accept_rate *= decay_rate
            strike += 1
        else:  # reject
            csp_prob.undo()
            accept_rate = init_accept_rate
            strike += 1

        if displayer is not None:
            time.sleep(0.01)
            displayer.update(csp_prob.get_assigned_object())

        if crt_block == 8:
            crt_block = 0
        else:
            crt_block += 1

    return optimal_assignment, crt_weight


def local_search_modified(csp_prob: SudokuLocalSearchBlocks, converge_strike, num_random_restarts, init_accept_rate,
                          decay_rate, displayer=None):
    """
    Run local search on given CSP problem. Modified for Sudoku problem. Stop immediately if converged to global optimum.

    Args:
        csp_prob (CSP): CSP problem to solve.
        converge_strike (int): The local search will be considered to be converged if weight does not change after
            this number of consecutive iterations.
        num_random_restarts (int): Number of random restarts.
        displayer (SudokuGui): Gui object to display current assignments.
        init_accept_rate (float): Rate to accept the change when it made the score worse.
        decay_rate (float): Rate to decay the accept rate each time when worse changes are accepted.

    Return:
        (dict): Dictionary of assignments to variables.
        (int): Weight which the optimal assignment will produce.
    """
    list_optimal_assignments = list()

    for i in range(num_random_restarts):
        optimal_assignment, crt_weight = local_search_single(csp_prob, converge_strike, init_accept_rate, decay_rate,
                        displayer)

        print("Itr:", i)
        print("Score", crt_weight)

        list_optimal_assignments.append((optimal_assignment, crt_weight))

        if crt_weight == 27:
            break

    max_weight = 0
    max_weight_idx = 0

    for idx in range(len(list_optimal_assignments)):
        assignment, weight = list_optimal_assignments[idx]

        if weight > max_weight:
            max_weight = weight
            max_weight_idx = idx

    return list_optimal_assignments[max_weight_idx][0], max_weight


def local_search_track(csp_prob: SudokuLocalSearchBlocks, converge_strike, num_random_restarts, init_accept_rate,
                          decay_rate, displayer=None):
    """
    Run local search on given CSP problem. But track how many times which the local search has converged to global
    optimum, and average score. Will not stop even if local search has converged to global optimum.

    Args:
        csp_prob (CSP): CSP problem to solve.
        converge_strike (int): The local search will be considered to be converged if weight does not change after
            this number of consecutive iterations.
        num_random_restarts (int): Number of random restarts.
        displayer (SudokuGui): Gui object to display current assignments.
        init_accept_rate (float): Rate to accept the change when it made the score worse.
        decay_rate (float): Rate to decay the accept rate each time when worse changes are accepted.

    Return:
        (list): List of scores obtained for each iteration of local search.
    """
    list_scores = list()

    for i in range(num_random_restarts):
        optimal_assignment, crt_weight = local_search_single(csp_prob, converge_strike, init_accept_rate, decay_rate,
                                                             displayer)

        print("Itr:", i)
        print("Score", crt_weight)

        list_scores.append(crt_weight)

    return list_scores


def run_backtracking(list_sudoku_txt, gui=False):
    """
    Run backtracking search for multiple sudoku puzzle, and measure runtime for them.

    Args:
        list_sudoku_txt (list[str]): List of names of text file of Sudoku puzzles to run.
        gui (bool): Display GUI?
    """
    total_runtime = 0

    for sudoku_txt in list_sudoku_txt:
        sudoku_obj = Sudoku()
        sudoku_obj.load_from_txt("sudoku_dataset/" + sudoku_txt)
        csp_sudoku = SudokuCSP(sudoku_obj)

        start_time = time.perf_counter()

        if gui:
            sudoku_displayer = SudokuGui(sudoku_obj.get_grids_filled())
        else:
            sudoku_displayer = None

        assignments = backtracking_search(csp_sudoku, displayer=sudoku_displayer)
        end_time = time.perf_counter()

        print(sudoku_txt)
        print(assignments)
        print(end_time - start_time)
        total_runtime += end_time - start_time
        print()

    print(f"Average execution time: {total_runtime / len(list_sudoku_txt):.6f} seconds")


def run_local_search(sudoku_file, converge_strike, accept_rate, decay_rate, num_remove, gui=False):
    """
    Run local search for single  sudoku puzzle, and measure runtime for it.

    Args:
        sudoku_file (str): Name of the file which contains the sudoku puzzle to run.
        converge_strike (int): Number of "strikes" for local search to run before convergence.
        accept_rate (float): Rate of acceptance when change made the score worse.
        decay_rate (float): Amount to decay accept rate per iteration of local search.
        num_remove (int): Number of assignments to reset per iteration of local search.
        gui (bool): Display GUI?

    Return:
        assignments (dict): Optimal assignments of variables obtained by this local search.
        max_weight (int): Score of assigning above assignments to Sudoku.
    """
    sudoku_obj = Sudoku()
    sudoku_obj.load_from_txt("sudoku_dataset/" + sudoku_file)
    cspl_sudoku = SudokuLocalSearch(sudoku_obj)

    num_random_restarts = 10 * num_remove

    if gui:
        sudoku_displayer = SudokuGui(sudoku_obj.get_grids_filled())
    else:
        sudoku_displayer = None

    assignments, max_weight = local_search(cspl_sudoku, converge_strike, num_random_restarts, accept_rate, decay_rate,
                                            num_remove, displayer=sudoku_displayer)

    return assignments, max_weight


def run_local_search_modified(sudoku_file, converge_strike, num_random_restarts, accept_rate, decay_rate, gui=False):
    """
    Run local search for single  sudoku puzzle, and measure runtime for it.

    Args:
        sudoku_file (str): Name of the file which contains the sudoku puzzle to run.
        converge_strike (int): Number of "strikes" for local search to run before convergence.
        num_random_restarts (int): Number of time to do random restart.
        accept_rate (float): Rate of acceptance when change made the score worse.
        decay_rate (float): Amount to decay accept rate per iteration of local search.
        gui (bool): Display GUI?

    Return:
        assignments (dict): Optimal assignments of variables obtained by this local search.
        max_weight (int): Score of assigning above assignments to Sudoku.
    """
    sudoku_obj = Sudoku()
    sudoku_obj.load_from_txt("sudoku_dataset/" + sudoku_file)
    cspl_sudoku = SudokuLocalSearchBlocks(sudoku_obj)

    if gui:
        sudoku_displayer = SudokuGui(sudoku_obj.get_grids_filled())
    else:
        sudoku_displayer = None

    assignments, max_weight = local_search_modified(cspl_sudoku, converge_strike, num_random_restarts, accept_rate, decay_rate,
                                            displayer=sudoku_displayer)

    return assignments, max_weight


def run_local_search_data(sudoku_file, converge_strike, num_random_restarts, init_accept_rate, decay_rate):
    """
    Run local search for single sudoku puzzle, and track average score and convergence probability.

    Args:
        sudoku_file (str): Name of the file which contains the sudoku puzzle to run.
        converge_strike (int): Number of "strikes" for local search to run before convergence.
        num_random_restarts (int): Number of time to do random restart.
        init_accept_rate (float): Rate of acceptance when change made the score worse.
        decay_rate (float): Amount to decay accept rate per iteration of local search.

    Return:
        avg_score (float): Average score obtained.
        convergence_prob (float): Probability of converging to global optimum.
    """
    sudoku_obj = Sudoku()
    sudoku_obj.load_from_txt("sudoku_dataset/" + sudoku_file)
    cspl_sudoku = SudokuLocalSearchBlocks(sudoku_obj)
    list_scores = local_search_track(cspl_sudoku, converge_strike, num_random_restarts, init_accept_rate,
                                     decay_rate, displayer=None)
    total_score = 0
    converged = 0

    for score in list_scores:
        total_score += score

        if score == 27:
            converged += 1

    return total_score / num_random_restarts, converged / num_random_restarts


list_sudoku_txt = [
    "sudoku_easy1.txt",
    "sudoku_easy2.txt",
    "sudoku_medium1.txt",
    "sudoku_medium2.txt",
    "sudoku_hard1.txt",
    "sudoku_hard2.txt",
    "sudoku_expert1.txt",
    "sudoku_expert2.txt",
    "sudoku_master1.txt",
    "sudoku_master2.txt",
    "sudoku_extreme1.txt",
    "sudoku_extreme2.txt"
]

# Runs backtracking search on given list of Sudoku puzzles.
# Add or remove file names from above “list_sudoku_txt” to run different set of Sudoku puzzles.
run_backtracking(list_sudoku_txt, gui=False)

# Runs block-based local search on Sudoku puzzle on given file name.
# his function will terminate when maximum score of 27 is reached, or given number of iterations are passed.
# And prints the maximum score achieved, and optimal assignment which gave that maximum score.
assignments, weight = run_local_search_modified("sudoku_easy1.txt", 1000, 100,
                                                0.6, 0.999, gui=False)
print(assignments)
print(weight)

# Also runs block-based local search on Sudoku puzzle on given file name.
# This function will always run to given number of iterations.
# prints average score achieved throughout the search, and percentage of converging to score 27 during the search.
avg_score, converge_rate = run_local_search_data("sudoku_expert2.txt", 2000,
                                                 100, 0.6, 0.9999)
print("Average Score =", avg_score)
print("Converge Rate =", converge_rate)

