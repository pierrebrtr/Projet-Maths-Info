from tkinter import *
from math import *

points = []
triliste = []


def demarrer(w = 500, h = 500):
    global width
    global height
    global main


    width = w
    height = h

    main = Application()
    main.canvas.bind("<Button-1>", point)
    main.canvas.bind("<Button-3>", clear)
    main.canvas.bind('<Motion>', move)
    main.canvas.old_coords = None
    main.fen.mainloop()

    return


class Application:

    def __init__(self):

        self.fen = Tk()
        self.fen.title("Projet Maths Info | Paul & Pierre")

        self.canvas = Canvas(self.fen, bg="white", width=width, height= height)
        self.canvas.configure(cursor="crosshair")
        self.canvas.pack()

   

        self.canvas.pack()



def clear(self):
        
        points.clear()
        main.canvas.delete("all")
        main.canvas.bind("<Motion>",move)
        main.canvas.bind("<Button-1>", point)


def point(event):
    points.append((event.x,event.y))
    if(len(points) >= 2):
        main.canvas.create_line(points, tags="line", width= 1)
        main.canvas.tag_lower("line")
    main.canvas.create_oval(event.x - 8, event.y - 8, event.x+8, event.y+8, fill="red",tags= 'first' if len(points) == 1 else 'sec',width="2")
    main.canvas.create_line(event.x,event.y,event.x +1,event.y + 1,fill="blue", width= 1,tags="line2")
    main.canvas.tag_bind("first","<Button-1>",polygon)
    return points

def polygon(event) :
    main.canvas.create_polygon(*points, fill='red')
    main.canvas.create_line(points[0][0],points[0][1],points[-1][0],points[-1][1], tags="line", width= 2)
    main.canvas.tag_raise("line")
    main.canvas.unbind("<Button 1>")
    main.canvas.unbind("<Motion>")
    main.canvas.delete("line2")
    drawT(trianguler(points))

   

def move(event):
    x, y = event.x, event.y
    if len(points)>=1:
        if main.canvas.old_coords:
            x1, y1 = main.canvas.old_coords
            main.canvas.tag_lower("line2")
            main.canvas.coords("line2", points[len(points)-1][0], points[len(points)-1][1], x1, y1)
        main.canvas.old_coords = x, y

def cotedroite(p0,p1,M):
    return (p1[0]-p0[0])*(M[1]-p0[1])-(p1[1]-p0[1])*(M[0]-p0[0])  

def voisin_sommet(n,i,di):
    return (i+di)%n

def danstriangle(triangle,M):
    p1 = triangle[0]
    p2 = triangle[1]
    p3 = triangle[2]
    return cotedroite(p1,p2,M) > 0 and cotedroite(p2,p3,M) > 0 and cotedroite(p3,p1,M) > 0

def sommetmax(points,p0,p1,p2,index):
    n = len(points)
    distance = 0.0
    j= None
    for i in range(n):
        if not(i in index):
            M = points[i]
            if danstriangle([p0,p1,p2],M):
                d = abs(cotedroite(p1,p2,M))
                if d > distance:
                    distance = d
                    j=i
    return j

def gauche(points):
    n = len(points)
    x = points[0][0]
    j = 0
    for i in range(1,n):
        if points[i][0] < x :
            x = points[i][0]
            j = i
    return j

def poly(points,start,finish):
    n = len(points)
    p= []
    i = start
    while i!=finish:
        p.append(points[i])
        i = voisin_sommet(n,i,1)
    p.append(points[finish])
    return p

def triangulationb(points,triliste):
    n = len(points)
    j0 = gauche(points)
    j1 = voisin_sommet(n,j0,1)
    j2 = voisin_sommet(n,j0,-1)
    p0 = points[j0]
    p1 = points[j1]
    p2 = points[j2]
    j = sommetmax(points, p0,p1,p2,[j0,j1,j2])
    if j == None:
        triliste.append([p0,p1,p2])
        polyb = poly(points,j1,j2)
        if len(polyb)==3:
            triliste.append(polyb)
        else:
            triangulationb(polyb,triliste)
    else:
        polyb = poly(points,j0,j)
        polybb = poly(points,j,j0)
        if len(polyb)==3:
            triliste.append(polyb)
        else :
            triangulationb(polyb,triliste)
        if len(polybb)==3:
            triliste.append(polybb)
        else :
            triangulationb(polybb,triliste)
    return triliste

def trianguler(points):
    liste = []
    triangulationb(points,liste)
    return liste

def drawT(liste):
    print(liste)
    for triangle in liste:
        print(triangle)
        main.canvas.create_line(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1], tags="triangl", width= 1)
        main.canvas.create_line(triangle[0][0],triangle[0][1],triangle[2][0],triangle[2][1], tags="triangl", width= 1)
        main.canvas.create_line(triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1], tags="triangl", width= 1)


demarrer()
