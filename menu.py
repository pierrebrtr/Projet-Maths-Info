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
    offset = complex(center[0], center[1] -20)
    newxy = []
    for x, y in array:
        v = cangle * (complex(x, y) - offset) + offset
        newxy.append(v.real)
        newxy.append(v.imag)
    canvas.coords(polygon_item, *newxy)

def editeur():
    fen.destroy()
    import projet as projetb


def click(event):
    x= event.x
    y = event.y
    if (x > 265 and x < 440 and y > 260 and y < 310):
        editeur()
    if (x > 265 and x < 440 and y > 340 and y < 390):
        print("jeux")
    if (x > 565 and x < 670 and y > 450 and y < 480):
        fen.destroy()

def anchor(event):
    x= event.x
    y = event.y
    if (x > 265 and x < 440 and y > 340 and y < 390):
        x1 = 260
        x2 = 437
        y1=337
        y2=385
        canvas.create_line(x1,y1,x2,y1,fill="red",width = 3,tags="rect")
        canvas.create_line(x1,y1,x1,y2,fill="red",width = 3,tags="rect")
        canvas.create_line(x2,y1,x2,y2,fill="red",width = 3,tags="rect")
        canvas.create_line(x1,y2,x2,y2,fill="red",width = 3,tags="rect")
    elif (x > 265 and x < 440 and y > 260 and y < 310):
        x1 = 260
        x2 = 437
        y1=260,
        y2=310
        canvas.create_line(x1,y1,x2,y1,fill="red",width = 3,tags="rect")
        canvas.create_line(x1,y1,x1,y2,fill="red",width = 3,tags="rect")
        canvas.create_line(x2,y1,x2,y2,fill="red",width = 3,tags="rect")
        canvas.create_line(x1,y2,x2,y2,fill="red",width = 3,tags="rect")
    elif(x > 565 and x < 670 and y > 450 and y < 480):
        x1 = 565
        x2 = 670
        y1=447
        y2=485
        canvas.create_line(x1,y1,x2,y1,fill="yellow",width = 3,tags="rect")
        canvas.create_line(x1,y1,x1,y2,fill="yellow",width = 3,tags="rect")
        canvas.create_line(x2,y1,x2,y2,fill="yellow",width = 3,tags="rect")
        canvas.create_line(x1,y2,x2,y2,fill="yellow",width = 3,tags="rect")
    else:
        canvas.delete("rect")





fen = Tk()
fen.title("Projet Maths Info | Paul & Pierre")

canvas = Canvas(fen, bg="white", width=width, height= height)
logo=PhotoImage(file="menu.png")
canvas.create_image(0,0,anchor=NW, image=logo)
canvas.pack()

canvas.bind("<Button-1>", click)
canvas.bind("<Motion>",anchor)



triangle = [(365, 167), (337, 233), (392, 235)]

polygon_item = canvas.create_polygon(triangle,fill="red")
center = 350, 350
i = 0
while True:
    try :
        i = i + 1
        if i >=360:
            i = 0
        fen.update()
        animate(i,triangle)
        time.sleep(0.04)
    except:
        False


fen.mainloop()
