import pygame
from network import Network
from modelmvc import Model
from viewmvc import View
import sys

class Client:

    def __init__(self):
        self.Game = Model()
        self.Graphics = View()
        self.n = Network()
        self.clicked = False
        self.main()


    def main(self):
        """Main game loop"""
        while True:
            # Check to end the game
            if (self.Game.status == "X_Win") or (self.Game.status == "O_Win") or (self.Game.status == "Tie"):
                break
            self.check_for_event()  # Checks to see if the window X button was pressed
            self.send_mouse_pos()
            self.Game.change_status()  # Updates the status
            self.Game.choose_message()
            self.Graphics.draw_winning_line(self.Game.win_location)  # Draws the winning line (if needed)
            self.Graphics.draw_status(self.Game.game_message)  # Redraw the status with the new message
            self.Graphics.update_board()  # Redraws the board


    # Change clicked_board
    def send_mouse_pos(self):
        """When the mouse is clicked, sends the location to the server, where it will be checked and validated
        as a proper move."""

        #print(pygame.mouse.get_pos())
        mouseX, mouseY = pygame.mouse.get_pos()
        self.n.send(((mouseX, mouseY), self.clicked))
        self.clicked = False

    def receive_move(self):
        """Receives a move (either itself or the other player) from the server and adds it."""
        pass

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