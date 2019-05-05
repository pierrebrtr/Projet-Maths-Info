from tkinter import *
from math import *
import time

print("""
      
 _____ ___ _  __  __  _  __ _  _ _    __ _____ _  __  __  _  
|_   _| _ \ |/  \|  \| |/ _] || | |  /  \_   _| |/__\|  \| | 
  | | | v / | /\ | | ' | [/\ \/ | |_| /\ || | | | \/ | | ' | 
  |_| |_|_\_|_||_|_|\__|\__/\__/|___|_||_||_| |_|\__/|_|\__| 


""")

points = []
global triliste


def demarrer(w = 500, h = 500):
    global width
    global height
    global main

    width = w
    height = h

    main = Application()
    main.canvas.bind("<Button-1>", point)
    main.canvas.bind("<Button-3>", Application.clear)
    main.canvas.bind('<Motion>', move)
    main.canvas.old_coords = None
    main.fen.mainloop()

    return

class Application:

    def __init__(self):

        self.fen = Tk()
        self.fen.title("Projet Maths Info | Paul & Pierre")

##        self.menubar = Frame(self.fen)
##        self.menubar.pack(side="top",fill=X)
##        self.fbutton = Menubutton(self.menubar,text="Menu",underline = 0)
##        self.fbutton.pack(side="left")
##
##        self.filemenu = Menu(self.fbutton)
##        self.filemenu.add_command(label="Quit",command = self.fen.destroy)
##        self.fbutton.config(menu=self.filemenu)

        self.canvas = Canvas(self.fen, bg="white", width=width, height= height)
        self.canvas.configure(cursor="crosshair")
        self.canvas.pack(side="left")
        
        self.frame = Frame(self.fen)
        self.frame.pack(side="right")

        self.textbox = Label(self.frame,text="Menu",font=("Helvetica", 16))
        self.textbox.grid(row=0,column=1)
        ##,ipady=100
        

        self.bouton_trianguler = Button(self.frame, text="Trianguler", bg = "grey",command=trianguler)
        self.bouton_trianguler.grid(row=2,column =1,pady=10)

        self.bouton_coloration = Button(self.frame, text="Coloration", bg = "blue",command=coloration)
        self.bouton_coloration.grid(row=4,column =1,pady=10)

        self.bouton_clear = Button(self.frame, text="Effacer", bg = "grey",command=self.clear)
        self.bouton_clear.grid(row=5,column =1,pady=10)

        self.bouton_quitter = Button(self.frame, text="Quitter", bg = "red",command=self.fen.destroy)
        self.bouton_quitter.grid(row=6,column =1,pady=10)

        self.bouton_chiffre = Button(self.frame, text="Chiffres", bg = "green",command=chiffre)
        self.bouton_chiffre.grid(row=3,column =1,pady=10)

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

def triangulerbis(points):
    liste = []
    triangulationb(points,liste)
    return liste

def drawT(liste):
    for triangle in liste:
        main.canvas.create_line(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1], tags="triangl", width= 1)
        main.canvas.create_line(triangle[0][0],triangle[0][1],triangle[2][0],triangle[2][1], tags="triangl", width= 1)
        main.canvas.create_line(triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1], tags="triangl", width= 1)

def trianguler():
    global triliste
    if len(points)>=4:
        triliste = triangulerbis(points)
        drawT(triliste)


def chiffre():
    global triliste
    if (len(points)>=4):
        liste = triliste
        for i in range(len(liste)):
            x = (liste[i][0][0]+liste[i][1][0]+liste[i][2][0])/3
            y = (liste[i][0][1]+liste[i][1][1]+liste[i][2][1])/3
            main.canvas.create_text(x,y,text=i)


colors = ["blue","red","green"]

##def testar(t1,t2):
##    colorsb = ["blue","red","green"]
##    success = False
##    pos = 0
##    p1 = t1[0]
##    p2 = t1[1]
##    p3 = t1[2]
##    main.canvas.create_text(p1[0],p1[1],text="1")
##    main.canvas.create_text(p2[0],p2[1],text="2")
##    main.canvas.create_text(p3[0],p3[1],text="3")
##    p1b = t2[0]
##    p2b = t2[1]
##    p3b = t2[2]
##    i1 = -1
##    i2 = -1
##    i3=-1
##    try:
##        i1 = t1.index(p1b)
##        try:
##            i2 = t1.index(p2b)
##            success = True
##            pos = 3
##        except:
##            try:
##                i3 = t1.index(p3b)
##                success = True
##                pos = 2
##            except:
##                success = False
##    except:
##        try:
##            i2 = t1.index(p2b)
##            try:
##                i1 = t1.index(p1b)
##                success = True
##                pos = 3
##            except:
##                try:
##                    i3 = t1.index(p3b)
##                    success = True
##                    pos = 1
##                except:
##                    success = False
##        except: 
##            try:
##                i3 = t1.index(p3b)
##                try:
##                    i1 = t1.index(p1b)
##                    success = True
##                    pos = 2
##                except:
##                    try:
##                        i2 = t1.index(p2b)
##                        success = True
##                        pos = 1
##                    except:
##                        success = False
##            except:
##                print("")
##    if success :
##        if (i1 != -1):
##            colorsb.remove(main.canvas.itemcget(main.canvas.find_withtag(str(t1[i1][0])+","+str(t1[i1][1])), "fill"))
##        if (i2 != -1):
##            colorsb.remove(main.canvas.itemcget(main.canvas.find_withtag(str(t1[i2][0])+","+str(t1[i2][1])), "fill"))
##        if (i3 != -1):
##            colorsb.remove(main.canvas.itemcget(main.canvas.find_withtag(str(t1[i3][0])+","+str(t1[i3][1])), "fill"))
##    else :
##        colorsb = ["grey"]
##    return (success,pos - 1,colorsb[0])      
##
##
##


def segmentation(t1,t2):
    success = False
    if((t1[0] in t2 and t1[1] in t2)  or (t1[2] in t2 and t1[1] in t2) or (t1[0] in t2 and t1[2] in t2)):
        success = True
        
    return (success)


global bliste

def coloration():
    colors = ["red","green","blue"]
    global bliste,triliste
    bliste = triliste
    print("------")
    print("Triangle 1")
    for j in range (0,3):
        main.canvas.create_oval(bliste[0][j][0] - 8, bliste[0][j][1] - 8, bliste[0][j][0]+8,bliste[0][j][1]+8, fill=colors[j],tags=str(bliste[0][j][0])+","+str(bliste[0][j][1]),width="2")
        print("Point n°" + str(j + 1) + " : ",main.canvas.itemcget(main.canvas.find_withtag(str(bliste[0][j][0])+","+str(bliste[0][j][1])), "fill"),str(bliste[0][j][0])+","+str(bliste[0][j][1]))
    index = 0
    print("------")
    recur(0)


subliste = []         
def recur(index):
    print("RECURSION AVEC " + str(index))
    global bliste
    c = 0
    for x in range(len(bliste)):
        if (bliste[x] != "N" and bliste[index] != "N" and index != x):
            if(segmentation(bliste[index],bliste[x])):
                c= c +1
                subliste.append((bliste[x],bliste[index]))
    print("Nb d'occurences : " + str(c))

    
    for x in range(len(bliste)):
        if (bliste[x] != "N" and bliste[index] != "N" and index != x):
            if(segmentation(bliste[index],bliste[x])):
                print("Triangle n°" + str(x) + " collé à triangle n°" + str(index))
                triangle = bliste[x]
                colors = ["red","green","blue"]
                ide = [0,1,2]
                for i in range (len(triangle)):
                    if (triangle[i] in bliste[index]):
                        colors.remove(main.canvas.itemcget(main.canvas.find_withtag(str(triangle[i][0])+","+str(triangle[i][1])), "fill"))
                        ide.remove(i)
                y = ide[0]
                main.canvas.create_oval( triangle[y][0]- 8, triangle[y][1] - 8, triangle[y][0]+8,triangle[y][1]+8, fill=colors[0],tags=str(triangle[y][0])+","+str(triangle[y][1]),width="2")
                bliste[index] = "N"
                print("NEXT ->", str(x))
                recur(x)




demarrer()
