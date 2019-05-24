import socket
import json

class Network:
    """A class that is responsible for connecting to the server"""
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a socket object
        self.server = "192.168.1.77"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()  # Connect to the server and collect the data from it


    def connect(self):

        try:
            self.client.connect(self.addr)  # Try and connect the socket object to the server
            return json.loads(self.client.recv(2048))  # Receives data from the server
        except:
            print("Attempt at connecting to server has failed")

    def send(self, data):
        """Responsible for sending data to the server"""
        try:
            self.client.send(json.dumps(data))
        except socket.error as e:
            print(e)