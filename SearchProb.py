class SearchState:
    """
    Represents a class of the state of search problem. Each state will have unique "object" which defines current state.
    """
    def get_current_state(self):
        """
        Get an object which represent current state of this search problem
        """
        pass

    def get_actions(self):
        """
        Get list of valid actions from current state.
        """
        pass

    def execute_action(self, action):
        """
        Perform action from current state. Change the state according to the action, and return the cost of action.

        Args:
            action: Action to perform.

        Return:
            (state): State when action is executed.
            (float): Cost of the action.
        """
        pass

    def is_goal(self):
        """
        Check if current state is the goal or not.

        Return:
            (bool): True, if current state is the goal state. False, if not.
        """
        pass

    def state_equal(self, another_state):
        """
        Compare two states given as SearchState.

        Args:
            another_state (SearchProb): state object to compare against.

        Return:
            (bool): True, if state given is same as state of this state. False, if not.
        """
        pass
