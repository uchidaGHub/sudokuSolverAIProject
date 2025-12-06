import pygame


class SearchGui:
    """
    A class which represents generic Gui object.

    Attrs:
        screen (display): Window to display the current environment.
    """
    def __init__(self):
        """
        Initialize the GUI by setting up the screen

        Args:
            filled_default (np.array): 2D array of of boolean which contains information of grid positions that are
                filled by default.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((900, 900))
        pygame.display.update()

    def update(self, env):
        """
        Display current environment onto the screen.

        Args:
            env: Object which represents current environment to display.
        """
        pass
