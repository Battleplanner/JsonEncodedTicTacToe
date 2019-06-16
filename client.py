import pygame
import json
from network import Network
from modelmvc import Model
from viewmvc import View
import sys

"""ERROR: The code gets caught up waiting for a move from user (in the method receive move, it will not continue until
it has received player and requested cell, therefore stopping the program."""


class Client:

    def __init__(self):
        self.Game = Model()
        self.Graphics = View()
        self.n = Network()
        self.clicked = False

        while True:
            try:
                symbol = self.n.recv().decode()
                self.symbol = symbol
                break
            except:
                print("Client couldn't receive the symbol from the server")


        print("Received symbol {} from the server".format(self.symbol))
        self.main()

    def main(self):
        """Main game loop"""
        while True:
            # Check to end the game
            print("The game status is currently {}".format(self.Game.status))
            if (self.Game.status == "X_Win") or (self.Game.status == "O_Win") or (self.Game.status == "Tie"):
                print(self.Game.game_message)
                break
            print("CHECKPOINT A")
            self.check_for_event()  # Checks to see if the window X button was pressed
            print("CHECKPOINT A.1")
            self.Game.change_status()  # Updates the status
            self.Game.choose_message()
            print("CHECKPOINT B")
            self.Graphics.draw_winning_line(self.Game.win_location)  # Draws the winning line (if needed)
            self.Graphics.draw_status(self.Game.game_message)  # Redraw the status with the new message
            self.Graphics.update_board()  # Redraws the board
            print("CHECKPOINT C")
            self.send_mouse_pos()
            self.receive_move()

    # Change clicked_board
    def send_mouse_pos(self):
        """When the mouse is clicked, sends the location to the server, where it will be checked and validated
        as a proper move."""

        mouseX, mouseY = 0, 0

        mouseX, mouseY = pygame.mouse.get_pos()
        data = [mouseX, mouseY, self.clicked]
        self.n.send(json.dumps(data).encode("utf-8"))
        self.clicked = False

    def receive_move(self):
        """Receives a move (either itself or the other player) from the server and adds it."""
        try:
            player, requested_cell = json.loads(self.n.recv())  # Gets the move from the player
            self.Game.update_grid(requested_cell[0], requested_cell[1])
            if player == "X":
                self.status = "O"
            elif player == "O":
                self.status = "X"
        except:
            print("Something went wrong while trying to receive move from the server")

    def check_for_event(self):
        """Checks for events like QUIT and MOUSEBUTTONDOWN"""
        for event in pygame.event.get(): # Finds events that are currently queued up
            if event.type == pygame.QUIT:  # If the window close button is pressed
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True


if __name__ == "__main__":
    Client()