###################################################################
#Script	: Client serveur
#Auteurs : Paul Lefay et Pierre Bertier
###################################################################
import socket

#Classe gérant le côté client pour la liaison serveur client du jeu multijoueur
class Network:
    #Initialisation de la connexion avec demande de l'ip du serveur
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = input("Ip du serveur ? ->")
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()
        print("CONNEXION : ", self.id)
    #Connexion avec le client et reception de données
    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()
    #Envoi de données + réception si données en retour
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
