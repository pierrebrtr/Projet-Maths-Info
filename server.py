###################################################################
#Script	: Serveur
#Auteurs : Paul Lefay et Pierre Bertier
###################################################################
import socket
from _thread import *
import sys
import time
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ''
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("En attente d'une connexion")

currentId = "0"
pos = ["0:NONE", "1:NONE"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    time.sleep(1)
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            print("Reception: " + reply)
            arr = reply.split(":")
            id = int(arr[0])
            pos[id] = reply
            if id == 0: nid = 1
            if id == 1: nid = 0
            reply = pos[nid][:]
            print("Envoi: " + reply)
            conn.sendall(str.encode(reply))
        except:
            break
    print("Fermeture de connexion")
    conn.close()
    currentId = "0"
    pos = ["0:NONE", "1:NONE"]




while True:
    conn, addr = s.accept()
    print("Connecté à: ", addr)

    start_new_thread(threaded_client, (conn,))
