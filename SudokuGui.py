import pygame

from final_project.SearchGui import SearchGui


class SudokuGui(SearchGui):
    """
    Represents a Gui which displays status of Sudoku as GUI.

    Attrs:
        font (Font): Font object to display digits in Sudoku board as UI.
        filled_default (np.array): 2D array of boolean which contains True, if corresponding grid of Sudoku board is
            filled by default.
    """
    def __init__(self, filled_default):
        """
        Initialize the GUI, and display the 9 by 9 grid.

        Args:
            filled_default (np.array): 2D array of of boolean which contains information of grid positions that are
                filled by default.
        """
        super().__init__()
        self.filled_default = filled_default

        pygame.font.init()
        pygame.font.get_init()
        self.font = pygame.font.SysFont("freesanbold.ttf", 80)
        pygame.display.set_caption("Sudoku Search Visualization")

        for i in range(8):
            if i == 2 or i == 5:
                thickness = 10
            else:
                thickness = 3

            pygame.draw.line(self.screen, "white", [100 * i + 100, 0], [100 * i + 100, 900], thickness)
            pygame.draw.line(self.screen, "white", [0, 100 * i + 100], [900, 100 * i + 100], thickness)

        pygame.display.update()

    def update(self, grid):
        """
        Display given grid onto the screen.

        Args:
            grid (np.array): Array represents Sudoku board to display.
        """
        background = pygame.Surface(self.screen.get_size())

        for i in range(9):
            for j in range(9):
                text_digit = str(grid[i][j])[0]

                if self.filled_default[i][j]:
                    color = "White"
                else:
                    color = "Green"

                text_render = self.font.render(text_digit, True, color)
                text_rect = text_render.get_rect()
                text_rect.center = (j * 100 + 50, i * 100 + 50)
                self.screen.blit(background, text_rect, text_rect)

                if text_digit != '0':
                    self.screen.blit(text_render, text_rect)

        pygame.display.update()
