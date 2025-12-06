import time

from final_project.SearchProb import SearchState
from final_project.SudokuSearch import SudokuSearchState


class ASearchAlgo:
    """
    Class which represents generic search algorithms.

    Attrs:
        frontier (list): List which stores nodes. Seen states will be pushed, and explored states will be pop'ed.
        explored (list): List of explored states.
        displayer (SudokuGui): Object which displays current status of state.
    """
    def __init__(self, init_state:SearchState, displayer, gui_flag):
        """
        Initialize the search problem.

        Attrs:
            init_state (SearchState): Initial state of the search problem.
            displayer (SudokuGui): Object which displays current status of state.
            gui_flag (bool): True, if want to enable the GUI.
        """
        self.frontier = [(init_state.get_current_state(), list())]
        self.explored = list()

        if gui_flag:
            self.displayer = displayer
            self.displayer.update(init_state.get_current_state())
        else:
            self.displayer = None

    def pop_from_frontier(self):
        """
        Pop a node from the frontier. Delete it from the frontier.

        Return:
            (node): A single node in the frontier, with first priority defined by each subclasses.
        """
        pass

    def is_explored(self, state):
        """
        Check if given state is in the explored list.

        Args:
            state (SearchSTate): State to search for.

        Return:
            (bool): True if state is in the explored list. False, if not.
        """
        for state_explored in self.explored:
            if state.state_equal(state_explored):
                return True

        return False

    def search(self):
        """
        Run the search problem.

        Return:
            (list(action)): List of actions found to the goal state. Or None if path does not exist.
        """
        while len(self.frontier) > 0:
            crt_state, crt_path = self.pop_from_frontier()
            crt_state_obj = SudokuSearchState(crt_state)
            list_actions = crt_state_obj.get_actions()

            if self.displayer is not None:
                time.sleep(0.1)
                self.displayer.update(crt_state)

            if crt_state_obj.is_goal():
                return crt_path

            if self.is_explored(crt_state_obj):
                continue

            for action in list_actions:
                next_state, cost = crt_state_obj.execute_action(action)

                if next_state is not None:
                    next_path = crt_path + [action]
                    next_node = (next_state.get_current_state(), next_path)
                    self.frontier.append(next_node)

            self.explored.append(crt_state)

        return None
