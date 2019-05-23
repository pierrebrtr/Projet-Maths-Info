###################################################################
#Script	: Client serveur
#Auteurs : Paul Lefay et Pierre Bertier
###################################################################
import socket

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.0.25"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()
        print("CONNEXION : ", self.id)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
