class CSP:
    """
    Represents the class for Condition Satisfaction Problem.
    Contains variables and factors.
    """
    def get_current_assignments(self):
        """
        Get current list of values assigned to each variable.

        Return:
            (dict): Dictionary which represents assignment of values into variables.
                Key: Represents variable.
                Val: Represents value assigned to the variable.
        """
        pass

    def get_variables(self):
        """
        Get all variables which can have some values assigned.

        Return:
            (list): List of all variables in this CSP.
        """
        pass

    def get_possible_values(self, var):
        """
        Get list of all possible values of given variable.

        Args:
            var: Variables to search for.

        Return:
            (list): List of all possible assignments to given variable.
        """
        pass

    def is_complete(self):
        """
        Is the current assignment complete?

        Return:
            (bool): Return True if values are assigned to all variables. False, if not.
        """
        pass

    def assign(self, var, val):
        """
        Assign given value to given variable.

        Args:
            var: Variable to assign.
            val: Value to assign to that variable.
        """
        pass

    def get_weight(self):
        """
        Calculate weight of current assignment.

        Return:
            (float): Weight of the current assignment.
        """
        pass

    def get_valid_values(self, var):
        """
        Get list of all assignments of values to the given variable, which makes the assignment consistent with
        assignments to all other variables.

        Args:
            var: Variable to check.

        Return:
            (list): List of value assignments which makes the system consistent.
        """
        pass

    def get_affected_vars(self, var):
        """
        Get list of all variables which are in the scope of all factors that the given variable is involved in.

        Args:
            var: Variable to check.

        Return:
            (list): List of variables which are in the scope of all factors that the given variable is involved in.
        """
        pass

    def unassigned_vars(self):
        """
        Get list of all variables with values not assigned.

        Return:
            (list): List of variables with no values assigned.
        """
        pass

    def lookahead(self, var):
        """
        Get list of valid values for each variable that is dependent on given variable.

        Args:
            var: Variable to start at.

        Return:
            (list[list]): 2D list of valid values for each dependent variables.
        """
        pass

    def get_assigned_object(self):
        """
        Get an object which represents this CSP when current variables are assigned.

        Return:
            Object which represents this CSP when current variables are assigned.
        """
        pass

    def assign_random(self):
        """
        Assign random possible values for each variable in this CSP.
        """
        pass

    def remove_assignment(self, var):
        """
        Remove the assignment of given variable by assigning None.

        Args:
            var: Variable to remove assignment from.
        """
        pass

    def get_score_after(self, list_var):
        """
        Get dictionary of total weight for each possible values can be assigned to all given variables.

        Args:
            list_var: List of variables to assign values to.

        Return:
            (list): List which shows total weight of assigning each values.
                [0] (dict): Values to be assigned to each variable.
                [1] (int): Weight when these values are assigned.
        """
        pass

    def copy(self):
        """
        Get the new CSP object with this exact attribute.

        Return:
            (CSP): CSP object with this exact attribute.
        """
        pass

    def get_if_score(self, list_vars, list_vals):
        """
        Get if score of when given list of values are assigned to each given list of variables.

        Args:
            list_vars (list): List of variables to check.
            list_vals (list): List of values to test for each variable.
        """
        pass

    def assign_multiple(self, list_vars, list_val):
        """
        Assign to all variables in the given list, corresponding value in the given list.

        Args:
            list_vars (list): List of variables to assign to.
            list_val (list): List of values to assign to variables.
        """
        pass

    def get_invalid_vars(self):
        """
        Get list of variables in self.get_variables() which contains overlapping digits.

        Return:
            (list[(int, int)]): List of invalid variables which contains overlapping digits.
        """
        pass
