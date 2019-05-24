# There's nothing to update grid


class Model:
    """This is the Model. Here, all the game data and logic is held"""

    def __init__(self):
        """Initialises game variables, such as the grid, player turn, etc"""
        self.status = "X_Turn"
        self.grid = [[None, None, None], [None, None, None], [None, None, None]]
        self.win_location = None, None
        self.game_message = "X's Turn"
        self.CELL_DIMENSIONS = 100

    def update_grid(self, row, col):
        """Updates the grid based on what was played"""
        if self.status == "X_Turn":
            self.grid[row][col] = "X"
        elif self.status == "O_Turn":
            self.grid[row][col] = "O"

    def board_full(self):  # Note. This may belong under control...
        """Checks to see if the board is full, and returns True or False. """

        for row in self.grid:  # For each of the lists inside grid (which is made up of three lists, representing rows
            if None in row:  # If there is a None in any of the rows
                return False  # The board isn't full yet
        return True  # Otherwise, if there isn't a None in any of the rows, the board is full

    def choose_message(self):
        """Determines what the game message is, based on the game status."""
        if self.status == "X_Turn":
            self.game_message = "X's Turn"
        elif self.status == "O_Turn":
            self.game_message = "O's Turn"
        elif self.status == "Tie":
            self.game_message = "A Tie!"
        elif self.status == "X_Win":
            self.game_message = "X has won!"
        elif self.status == "O_Win":
            self.game_message = "O has won!"

    def change_status(self):
        """Changes the game status to either a player win, player turn, or a tie."""
        grid = self.grid

        if self.board_full() == True:  # Checks to see if the board is full
            self.status = "Tie"  # Change the status to a tie
            self.win_location = None, None  # Sets the win location to None

        # Check for rows in which someone has won
        for row in range(0, 3):  # In any of the rows (i.e row 1, row 2, or row 3)
            # If the 1st, 2nd and 3rd values are the same and are not empty...
            if (grid[row][0] == grid[row][1] == grid[row][2]) and (grid[row][0] is not None):
                self.status = "{}_Win".format(grid[row][0])  # Sets the status to X_Win or O_Win
                # Creates the win_location variable (so that View knows where to draw the win line)
                self.win_location = "row", row

        # Check for columns in which someone has won
        for col in range(0, 3):  # In any of the columns (i.e column 1, column 2 or column 3 i
            # If the 1st, 2nd and 3rd values are the same and are not empty...
            if (grid[0][col] == grid[1][col] == grid[2][col]) and (grid[0][col] is not None):
                self.status = "{}_Win".format(grid[0][col])  # Sets the status to X_Win or O_Win
                # Creates the win_location variable (so that View knows where to draw the win line)
                self.win_location = "col", col

        # Check for diagonal wins
        # If the diagonal values starting from the top left are all the same and are not empty
        if (grid[0][0] == grid[1][1] == grid[2][2]) and (grid[0][0] is not None):
            self.status = "{}_Win".format(grid[0][0])  # Sets the status to X_Win or O_Win
            # Creates the win_location variable (so that the View class knows where to draw the win line)
            self.win_location = "diag1", None

        # If the diagonal values starting from the top right are all the same and are not empty
        if (grid[0][2] == grid[1][1] == grid[2][0]) and (grid[0][2] is not None):
            self.status = "{}_Win".format(grid[0][2])  # Sets the status to X_Win or O_Win
            # Creates the win_location variable (so that the View class knows where to draw the win line)
            self.win_location = "diag2", None


        """
        Note about the diag's. The reason the second value is None is because there is only 1 diag1/diag2.
        In the other cases, the format is "row", (which row), or "col", (which col).

        Also, the way Python checks through the if statements means that even if a player wins but uses the last
        space on the board, the code will first register a tie, then later change that in the code to a player win.
        """

    def cell_occupied(self, row, col):
        """Checks to see if a specified cell is occupied (Necessary in order to only draw if the space is empty"""
        cell = self.grid[col][row]  # Gets the value of the specified cell
        if cell != None:  # If theh cell is equal to X or O
            return True
        elif cell == None:  # If the cell is empty
            return False

    def toggle_turn(self):
        """Toggles the turn. Not much to it really."""
        if self.status == "X_Turn":  # If it was X's turn to play
            self.status = "O_Turn"  # Toggle it to O's turn
        elif self.status == "O_Turn":  # If it was O's turn to play
            self.status = "X_Turn"  # Toggle it to X's turn

    def find_cell(self, mouseX, mouseY):
        """Responsible for finding out which board space (i.e row, column) the user clicked in based on
        their mouse coordinates. Requires the coordinates the mouse clicked in."""
        point = mouseY // self.CELL_DIMENSIONS, mouseX // self.CELL_DIMENSIONS

        """Further information:
        First off, the reason point is in the form Y, X is because X represents the horizontal axis, which is the 
        column, while Y represents the vertical axis, which is the row. For that reason, I'm putting in the format
        row, col.

        Second off, the reason I've divided the coordinate by the cell dimensions (which represent the width and height
        of the cell) is so that I get the middle of the cell."""
        return point  # The point is which row and column the mouse clicked in