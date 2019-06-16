import pygame
import sys


class View:
    """Is responsible for dealing with everything the user sees (i.e GUI)"""

    def __init__(self):
        pygame.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        WINDOW_DIMENSIONS = 300, 325 # Width and Height
        self.LINE_THICKNESS = 5

        """Sets up the window"""

        # Creates the surface with the given width and height
        self.ttt = pygame.display.set_mode(WINDOW_DIMENSIONS)

        # Sets the caption for the game
        pygame.display.set_caption("Tic Tac Toe")

        """Initialises the board"""

        # Setup background surface
        background = pygame.Surface(self.ttt.get_size())

        # Creates a surface object with the window size
        background = background.convert()  # Converts toe background to pixel format
        background.fill(self.WHITE)  # Converts the backgorund to a WHITE color (I think)

        # Draw Grid Lines

        # Vertical lines
        pygame.draw.line(background, (self.BLACK), (100, 0), (100, 300), 2)
        pygame.draw.line(background, (self.BLACK), (200, 0), (200, 300), 2)

        # horizontal lines...
        pygame.draw.line(background, (self.BLACK), (0, 100), (300, 100), 2)
        pygame.draw.line(background, (self.BLACK), (0, 200), (300, 200), 2)

        # Note about lines: Draws the lines with the Surface, Color, Start pos, End pos, and width

        self.board = background

    def update_board(self):
        """You guessed it! Updates the surface by redrawing the board onto it. Gets board from Model."""

        # Draw/redraws the status info at the bottom of the board

        # Places the board onto the display at the very base coordinates (top left corner)
        self.ttt.blit(self.board, (0, 0))
        pygame.display.flip()  # Updates the entire display

    def draw_status(self, game_message):
        """Updates the status with info on who's turn it is and who's won. Will receive the message from Controller"""

        font = pygame.font.Font(None, 24) # Creates a default font object with the size of 24 pixels

        text = font.render(game_message, True, (self.BLACK)) # Creates a surface with the existing message on it

        """Notes: Pygame doesn't allow you to add to an existing surface, so we'll have to 'blit' this surface
        onto the main one. After that, we set antialiasing to true. It then sets the color of the text to BLACK."""

        self.board.fill(self.WHITE, (0, 300, 300, 25))
        self.board.blit(text, (10, 300)) # Pastes the status onto the board at the position 10, 300.

    def draw_winning_line(self, win_location):
        """Draws the line that represents a win. Receives info about who won (and where) from Model"""
        win_state,value = win_location

        if win_state == "row":
            row = value
            pygame.draw.line(self.board, (self.RED), (0, (row + 1) * 100 - 50), (300, (row + 1) * 100 - 50), self.LINE_THICKNESS)

        elif win_state == "column":
            col = value
            pygame.draw.line(self.board, (self.RED), ((col + 1) * 100 - 50, 0), ((col + 1) * 100 - 50, 300), self.LINE_THICKNESS)

        elif win_state == "diag1":
            pygame.draw.line(self.board, (self.RED), (50, 50), (250, 250), self.LINE_THICKNESS)

        elif win_state == "diag2":
            pygame.draw.line(self.board, (self.RED), (250, 50), (50, 250), self.LINE_THICKNESS)

    def draw_move(self, game_status, board_row, board_col, CELL_DIMENSIONS):
        """Draws either an X or an O on a specific row and column on the board. Recieves who and where from Controller"""

        # Finds the center of the box we will draw in
        centerX = ((board_col) * CELL_DIMENSIONS) + (CELL_DIMENSIONS // 2)
        centerY = ((board_row) * CELL_DIMENSIONS) + (CELL_DIMENSIONS // 2)

        # Draws the appropriate symbol
        if game_status == "O_Turn":  # If the game status is O, draw a circle in the specified square
            pygame.draw.circle(self.board, (self.BLACK), (centerX, centerY), 33, 2)
        elif game_status == "X_Turn":
            # If the game status is X, draw two lines (i.e an X) in the specified square
            pygame.draw.line(self.board, (self.BLACK), (centerX - 22, centerY - 22), (centerX + 22, centerY + 22), 2)
            pygame.draw.line(self.board, (self.BLACK), (centerX + 22, centerY - 22), (centerX - 22, centerY + 22), 2)