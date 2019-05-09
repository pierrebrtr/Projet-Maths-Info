from tkinter import *
from math import *
import time


width = 700
height = 500
print("""

 _   _  ___  _  _  _ _ 
| \_/ || __|| \| || | |
| \_/ || _| | \\ || U |
|_| |_||___||_|\_||___|
                       
""")

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

fen.mainloop()



