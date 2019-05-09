from tkinter import *
import tkinter as tk
from math import *
import time
import math,cmath




width = 700
height = 500
print("""

 _   _  ___  _  _  _ _ 
| \_/ || __|| \| || | |
| \_/ || _| | \\ || U |
|_| |_||___||_|\_||___|
                       
""")


def animate(angle,array):
    angle_degrees=angle
    cangle = cmath.exp(angle_degrees*1j*math.pi/180)
    offset = complex(center[0], center[1])
    newxy = []
    for x, y in array:
        v = cangle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    canvas.coords(polygon_item, *newxy)

def editeur():
    fen.destroy()
    import projet as projetb

fen = Tk()
fen.title("Projet Maths Info | Paul & Pierre")

canvas = Canvas(fen, bg="white", width=width, height= height)
canvas.pack()

canvas.create_text(350,70,fill="darkred",font=("Helvetica", 50),
                        text="MENU")
bt_editeur = Button(fen, text="Editeur",font=("Helvetica", 14), command=editeur)
bt_editeur_w = canvas.create_window(350, 250, window=bt_editeur)

bt_jeux = Button(fen, text="Jeux #1",font=("Helvetica", 14), command=lambda: print("COMMANDE"))
bt_jeux_w = canvas.create_window(350, 320, window=bt_jeux)


bt_quitter = Button(fen, text="Quitter",font=("Helvetica", 14),bg="red", command=fen.destroy)
bt_quitter_w = canvas.create_window(640, 460, window=bt_quitter)

triangle = [(50, 50), (150, 50), (150, 150)]

polygon_item = canvas.create_polygon(triangle)
center = 100, 100
i = 0
while True:
    
    i = i + 1
    if i >=360:
        i = 0
    fen.update()
    animate(i,triangle)
    time.sleep(0.04)

    
fen.mainloop()








