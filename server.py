import socket
from _thread import *
import json
from modelmvc import Model

server = "192.168.1.77"  # The IP address for the server - Currently set to my internal ip address (192.168.1.77)
#server = "10.202.8.144"
port = 5555  # The port for the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Sets up a socket using IPV4 and TCP
Game = Model()


def threaded_client(conn, player):
    """When a client connects to the server, """

    # Sends some form of confirmation message - perhaps in the form of letting the client know what their symbol is
    try:
        conn.send(json.dumps(player).encode())  # Sends either "X" or "O" to the client
        print("Sent symbol '{}' to client".format(player))
    except socket.error as e:
        print("Failed to send symbol to client")
        print(e)

    while True:
        if Game.status == "{}_Turn".format(player):  # If it is the clients turn
            try:

                print("Getting mouse data from server...")
                mouseX, mouseY, clicked = json.loads(conn.recv(2048))
                print(mouseX, mouseY, clicked)
                mouse_pos = int(mouseX), int(mouseY)
                print(mouse_pos)

                if not mouse_pos:  # If the server is not receiving data
                    print("Disconnected")
                    break
                elif clicked:  # If the mouse was clicked
                    requested_cell = Game.find_cell(mouse_pos[0], mouse_pos[1])  # Finds the specified cell from the mouse position
                    print("The following is which cell the server thinks the client wants.")
                    print(requested_cell)
                    if None in requested_cell:  # If the mouse isn't above one of the cells
                        print("None found")
                        print(requested_cell)
                        break
                    if Game.cell_occupied(requested_cell[0], requested_cell[1]):  # If the cell is empty
                        conn.sendall(json.dumps([player, requested_cell]))  # Sends the specified cell to all clients
                        Game.grid[requested_cell] = player  # Updates the server model
                        Game.toggle_turn()  # Changes the turn
                        Game.change_status()  # Updates the status

            except socket.error as e:  # Will sprout a whole bunch of errors if there is no data (I think)
                print(e)

    # When the while loop ends (through disconnected or an error)
    print("Lost Connection")
    conn.close()


def main():
    """The main server function"""

    # The reason I'm using a try/except is in case something isn't right with server/port i.e already being used, etc
    try:
        s.bind((server, port))  # Binds the server and port to the socket
    except socket.error as e:
        print(e)

    s.listen(2)  # Opens up the port and allows connections
    print("Waiting for a connection, Server Started")

    Numofplayers = 0

    while True:
        """Continuously looks for a connection"""
        conn, address = s.accept()  # Accepts the connection object and the address of a client
        print("Connected to: {}".format(address))

        if Numofplayers == 0:
            start_new_thread(threaded_client, (conn, "X"))  # Starts a new thread for the threaded_client function
            Numofplayers += 1
        elif Numofplayers == 1:
            start_new_thread(threaded_client, (conn, "O"))  # Starts a new thread for the threaded_client function
            Numofplayers += 1


main()