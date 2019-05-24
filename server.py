"""How this should work...maybe
Client connects to thread
Thread sends confirmation message in the form of "X" or "O"
Client sends back "Accepted"
Thread accepts
Thread ignores all data from client until playerTurn conditional is true
Client will send their mouse clicks which will be ignored until playerTurn conditional is true
When it is true, the server then accepts the data, checks and validates it, updates, and sends the new move to all clients
Each client then accepts that data and updates their own board accordingly
Each client (and server) then checks how they should change the status (i.e check for a tie/3 in a row, etc)


"""


import socket
from _thread import *
import json
from modelmvc import Model

server = "192.168.1.77"  # The IP address for the server - Currently set to my internal ip address (192.168.1.77)
port = 5555  # The port for the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Sets up a socket using IPV4 and TCP
Game = Model()

def threaded_client(conn, player):
    """When a client connects to the server, """


    # Sends some form of confirmation message - perhaps in the form of letting the client know what their symbol is

    """IDEA!!:
    
    The client constantly sends the location of the mouse, as well as whether the mouse is being clicked or not.
    
    if quiting blah blah blah
        stuff
    elif event.type == pygame.MOUSEBUTTONDOWN:
        # Send (mouseposition, True) if the mouse was clicked.
    else
        # Send (mouseposition, False) if the mouse wasn't clicked.
        
    
    The server would be constantly receiving input and accepting it. This way, the server can check whether the client
    is still connected. It can constantly accept the mousepos, but only act upon it if a) it's the players turn and
    b) the mouse was clicked!
        
    
    """

    conn.send(str.encode(player))  # Sends either "X" or "O" to the client
    reply = ""  # Will hold the reply from the client (Should come back as "Confirmed Symbol")

    while True:
        if Game.status == "{}_Turn".format(player):  # If it is the clients turn
            try:

                mouse_pos, clicked = json.loads(conn.recv(2048))  # Gets the mouse position from the client

                print(mouse_pos)

                if not mouse_pos:  # If the server is not receiving data
                    print("Disconnected")
                    break
                elif clicked == True:  # If the mouse was clicked
                    requested_cell = Game.find_cell(mouse_pos)  # Finds the specified cell from the mouse position
                    if Game.cell_occupied(requested_cell):  # If the cell is empty
                        conn.sendall(json.dumps[player, requested_cell])  # Sends the specified cell to all clients
                        Game.grid[requested_cell] = player  # Updates the server model
                        Game.toggle_turn()  # Changes the turn
                        Game.change_status()  # Updates the status

            except socket.error as e: # Will sprout a whole bunch of errors if there is no data (I think)
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
        print(str(e))

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