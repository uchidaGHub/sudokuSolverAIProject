from final_project.SearchAlgorithm import ASearchAlgo


class DepthFirstSearch(ASearchAlgo):
    """
    EXTENDS ASearchAlgo
    Represents class which performs Depth First Search.
    """

    def pop_from_frontier(self):
        """
        OVERRIDE from ASearchAlgo
        In this class, the pop'ed element will be an element that is inserted at the last.
        """
        node = self.frontier[-1][0], self.frontier[-1][1]
        self.frontier = self.frontier[:-1]

        return node

