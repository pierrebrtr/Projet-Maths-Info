###################################################################
#Script	: Fonctions reponses à la notice
#Auteurs : Paul Lefay et Pierre Bertier
###################################################################

from tkinter import *

print("""

 _  _  _ ___  _  __  ___
| \| |/ \_ _|| |/ _|| __|
| \\ ( o ) | | ( (_ | _|
|_|\_|\_/|_| |_|\__||___|

""")
global points
points = [(186, 119), (345, 113), (426, 235), (363, 347), (127, 348), (91, 211)]

def coef(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersects(A,B,C,D):
    return coef(A,C,D) != coef(B,C,D) and coef(A,B,C) != coef(A,B,D)

def tracer_poly():
    global points
    canvas.create_polygon(*points, fill='red',width=1,outline="black")


def tracer_diago():
    global points
    for i in range(len(points)):
        for j in range(len(points)):
            if points[i] != points[j]:
                canvas.create_line(points[i][0],points[i][1],points[j][0],points[j][1],fill="blue", width= 1)

fen = Tk()
fen.title("Notice")
w = 500
h = 500
canvas = Canvas(fen, bg="white", width=w, height= h)
canvas.pack()
tracer_poly()
tracer_diago()
fen.mainloop()
