import socket
import json

class Network:
    """A class that is responsible for connecting to the server"""
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a socket object
        self.server = "192.168.1.77"
        #self.server = "10.202.8.144"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.symbol = self.connect()  # Connect to the server and collect the data from it

    def connect(self):

        while True:
            try:
                self.client.connect(self.addr)  # Try and connect the socket object to the server
                print("Connected to server: {}".format(self.addr))
                break
            except:
                print("Attempt at connecting to server has failed")

    def send(self, data):
        """Responsible for sending data to the server"""
        try:
            self.client.send(data)
        except socket.error as e:
            print("Attempt at sending data to the server has failed")
            print(e)

    def recv(self):
        while True:
            try:
                return self.client.recv(2048)
            except socket.error as e:
                print("Attempt at receiving data from the server has failed")
                print(e)