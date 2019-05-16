###################################################################
#Script	: Jeu #1
#Bonus : jeu en multijoueur
#Auteurs : Paul Lefay et Pierre Bertier
###################################################################

from tkinter import *
import tkinter.filedialog
from math import *
from time import *
import time
import random



points = []
global verif
global triliste,canpoly,sommet1,sommet2,sommet3,width,height


print("""
   _  ___  _ _
  | || __|| | |
n_| || _| | U |
\__/ |___||___|

""")



def demarrer(w = 500, h = 500):
    global width
    global height
    global main
    width = w
    height = h
    main = Application()
    main.fen2.mainloop()
    main.fen.mainloop()


    return



#-----Classe principale-----#

class Application:

    def __init__(self):
        getperso()

        self.fen2 = Tk()
        self.fen2.title("Menu | JEU")
        self.bouton_rand = Button(self.fen2, text="Random", bg = "yellow",command=randomg)
        self.bouton_rand.pack()

        self.bouton_import = Button(self.fen2, text="Importer", bg = "brown2",command=importg)
        self.bouton_import.pack()

        self.fen = Tk()
        self.fen.title("Jouer")



        self.canvas = Canvas(self.fen, bg="white", width=width, height= height)
        self.canvas.configure(cursor="crosshair")
        self.canvas.pack(side="left")

        self.frame = Frame(self.fen)
        self.frame.pack(side="right")

        self.textbox = Label(self.frame,text="Menu",font=("Helvetica", 16))
        self.textbox.grid(row=0,column=1)

        self.bouton_valider = Button(self.frame, text="Valider", bg = "green",command=validate)
        self.bouton_valider.grid(row=2,column =1,pady=10)
        self.bouton_valider.config(state=DISABLED)

        self.bouton_quitter = Button(self.frame, text="Menu principal", bg = "red",command=leave)
        self.bouton_quitter.grid(row=3,column =1,pady=10)

    def clear(self):
        points.clear()
        main.canvas.delete("all")



def point(event):
    points.append((event.x,event.y))
    if(len(points) >= 2):
        main.canvas.create_line(points, tags="line", width= 1)
        main.canvas.tag_lower("line")
    main.canvas.create_oval(event.x - 8, event.y - 8, event.x+8, event.y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt"],width="2",)
    main.canvas.create_line(event.x,event.y,event.x +1,event.y + 1,fill="blue", width= 1,tags="line2")
    main.canvas.tag_bind("first","<Button-1>",polygon)
    return points

def polygon(event) :
    global canpoly
    canpoly = True
    main.canvas.create_line(points[0][0],points[0][1],points[-1][0],points[-1][1], tags="line", width= 1)
    main.canvas.create_polygon(*points, fill='red')
    main.canvas.tag_raise("line")
    main.canvas.unbind("<Button 1>")
    main.canvas.delete("line2")
    print(points)


def leave():
    try:
        main.fen.destroy()
        main.fen2.destroy()
    except:
        print("")
    import menu as menub
    exit()

def getperso():
    global sommet1,sommet2,sommet3
    try:
        with open("fav.txt","r") as f:
            lines=f.readlines()
            sommet1 = lines[1].strip().replace(" ", "")
            sommet2 = lines[2].strip().replace(" ", "")
            sommet3 = lines[3].strip().replace(" ", "")
    except :
        #si le fichier n'existe pas :
        print("Problème sur le fichier, résolution en cours")
        sommet1 = "red"
        sommet2 = "green"
        sommet3 = "blue"
        with open("fav.txt","w") as f:
            f.write("Perso\n")
            f.write("red\n")
            f.write("green\n")
            f.write("blue\n")
            f.close()



#-----Modes de jeu-----#

def randomg():
    global width,height
    print("Random g")
    main.fen2.destroy()
    for i in range(0,5):
        points.append((random.randint(1,width -1),random.randint(1,height - 1)))

    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        main.canvas.create_oval(x - 8, y - 8, x+8, y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt"],width="2",)
        main.canvas.create_polygon(*points, fill='red',width=1,outline="black")

def importg():
    main.clear()
    fname = tkinter.filedialog.askopenfilename(filetypes=(('text files', 'txt'),))
    if (fname):
        with open(fname,"r") as f:
            liste = [ligne.strip() for ligne in f]
            for z in range(len(liste)):
                el = liste[z].split(",")
                (x,y) = int(el[0]),int(el[1])
                liste[z] = (x,y)
            for i in range(len(liste)):
                x = liste[i][0]
                y = liste[i][1]
                points.append((x,y))
                main.canvas.create_oval(x - 8, y - 8, x+8, y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt"],width="2",)
                main.canvas.create_polygon(*points, fill='red',width=1,outline="black")

            print("POINTS",points)
        main.fen2.destroy()
        main.bouton_valider.config(state=NORMAL)
        startg()

#-----Début de partie-----#

def startg():
    trianguler()
    global sommet1,sommet2,sommet3
    colors = [sommet1,sommet2,sommet3]
    global bliste,triliste
    bliste = []
    for el in triliste:
        bliste.append(el)
    for j in range (0,3):

        main.canvas.create_oval(bliste[0][j][0] - 8, bliste[0][j][1] - 8, bliste[0][j][0]+8,bliste[0][j][1]+8, fill=colors[j],tags=str(bliste[0][j][0])+","+str(bliste[0][j][1]),width="2")
        print("colorin",getColor(bliste[0][j]))
    for x in range(2,len(bliste)):
        for j in range (0,3):
            if not getColor(bliste[x][j]):
                main.canvas.create_oval(bliste[x][j][0] - 8, bliste[x][j][1] - 8, bliste[x][j][0]+8,bliste[x][j][1]+8, fill="yellow",tags=str(bliste[x][j][0])+","+str(bliste[x][j][1]),width="2")
                main.canvas.tag_bind((str(bliste[x][j][0])+","+str(bliste[x][j][1])), "<Button-1>", clickb)



def clickb(event):
    global sommet1,sommet2,sommet3
    x = event.x
    y = event.y
    el = main.canvas.find_closest(x,y)
    color = main.canvas.itemcget(el, "fill")
    if(color == "yellow"):
        color = sommet1
    elif(color == sommet1):
        color = sommet2
    elif (color == sommet2):
        color = sommet3
    elif (color == sommet3):
        color = sommet1
    main.canvas.itemconfig(el, fill=color)


def validate():
    print("Validation ...")
    init = []
    global bliste,verif
    for el in bliste:
        for j in range(0,3):
            if ((el[j][0],el[j][1]),getColor(el[j])) not in init :
                init.append(((el[j][0],el[j][1]),getColor(el[j])))
    print("INIT", init)
    coloration()
    if verif == init:
        print("WINNNNNN")


#-----Triangulation-----#

def gauche(points):
    n = len(points)
    x = points[0][0]
    j = 0
    for i in range(1,n):
        if points[i][0] < x :
            x = points[i][0]
            j = i
    return j

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
        start = perf_counter()
        triliste = triangulerbis(points)
        drawT(triliste)
        dt = perf_counter() - start
        print("Performance triangulation:",round(dt * 10**3, 2), " ms pour ", len(points), "points")


def chiffre():
    global triliste
    if (len(points)>=4):
        liste = triliste
        for i in range(len(liste)):
            x = (liste[i][0][0]+liste[i][1][0]+liste[i][2][0])/3
            y = (liste[i][0][1]+liste[i][1][1]+liste[i][2][1])/3
            main.canvas.create_text(x,y,text=i)

#-----Tri-Coloration-----#

def segmentation(t1,t2):
    success = False
    if((t1[0] in t2 and t1[1] in t2)  or (t1[2] in t2 and t1[1] in t2) or (t1[0] in t2 and t1[2] in t2)):
        success = True

    return (success)


global bliste

def coloration():
    global sommet1,sommet2,sommet3,verif
    verif = []
    colors = [sommet1,sommet2,sommet3]
    global bliste,triliste
    bliste = []
    for el in triliste:
        bliste.append(el)
    for j in range (0,3):
        verif.append(((bliste[0][j][0],bliste[0][j][1]),colors[j]))
    subliste = []
    for x in range(len(bliste)):
        if (0 != x and bliste[x] not in subliste):
            if(segmentation(bliste[0],bliste[x])):
                subliste.append(x)
    for el in subliste:
        recurTricolor(el,0)
    print("LISTE VERIF", verif)

def getPoint(t1,t2):
    color = []
    colorb = []
    for el in t2:
        color.append((el,getColor(el)))
    for el in color:
        colorb.append(el)
    for i in range(3):
        for j in range(3):
            if(color[j][0] == t1[i]):
                colorb.remove(color[j])
    liste = []
    for el in t1:
        liste.append(el)
    for i in range(3):
        for j in range(3):
            if t1[i] == t2[j]:
                liste.remove(t1[i])
    return (liste,colorb[0])

def getColor(pt):
    return (main.canvas.itemcget(main.canvas.find_withtag(str(pt[0])+","+str(pt[1])), "fill"))

def recurTricolor(index,indexb):
    global verif
    global bliste
    point = getPoint(bliste[index],bliste[indexb])[0][0]
    couleur = getPoint(bliste[index],bliste[indexb])[1][1]
    verif.append(((point[0],point[1]),couleur))
    subliste = []
    for x in range(len(bliste)):
        if (index != x and indexb != x and bliste[x] not in subliste):
            if(segmentation(bliste[index],bliste[x])):
                subliste.append(x)
    for el in subliste:
        recurTricolor(el,index)


#-----Initialisation-----#


demarrer()
