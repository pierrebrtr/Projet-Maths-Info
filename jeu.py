###################################################################
#Script	: Jeu #1
#Bonus : Jeu en multijoueur en temps réel !
#Auteurs : Paul Lefay et Pierre Bertier
##################################################################
    #Tableau des variables:
    #verif -> Liste verifiant si la partie est gagnée
    #triliste,bliste,sumb  -> Liste des triangles après la triangulation
    #canpoly-> Test pour savoir si le polygone peut être tracé
    #sommet1,2,3 -> Couleurs liées au fichier de personnalisation
    #winmulti -> Booléen testant l'issue de la partie
    #g -> Classe liée à la partie multijoueur
    #datab,xm,ym,colorm -> Données transferées entre les threads
###################################################################

from tkinter import *
import tkinter.filedialog
from math import *
from time import *
import time
import random
import os
from client import Network
from _thread import *
from tkinter import messagebox
import queue
from rpolygon import GPoly

points = []
global verif
global triliste,canpoly,sommet1,sommet2,sommet3,width,height
global sumb
global winmulti

print("""
   _  ___  _ _
  | || __|| | |
n_| || _| | U |
\__/ |___||___|

""")

#Initialisation de l'application
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

#Application principale
class Application:

    def __init__(self):
        getperso()

        self.fen2 = Tk()
        self.fen2.title("Menu | JEU")
        self.bouton_rand = Button(self.fen2, text="Random", bg = "SpringGreen2",command=randomg)
        self.bouton_rand.grid(row=1,column=1)

        self.textmenu = Label(self.fen2,text="Menu",font=("Helvetica", 16))
        self.textmenu.grid(row=0,column=2)

        self.bouton_import = Button(self.fen2, text="Importer", bg = "SpringGreen2",command=importg)
        self.bouton_import.grid(row=1,column=3)

        self.bouton_import = Button(self.fen2, text="En ligne", bg = "SpringGreen2",command=multiplayer)
        self.bouton_import.grid(row=1,column=2)

        self.bouton_leave = Button(self.fen2, text="Menu principal", bg = "brown2",command=leave)
        self.bouton_leave.grid(row=3,column=2,pady=10)

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

        self.bouton_quitter = Button(self.frame, text="Menu", bg = "red",command=leave)
        self.bouton_quitter.grid(row=3,column =1,pady=10)

    def clear(self):
        points.clear()
        main.canvas.delete("all")

    def multi(self):
        self.canvas2 = Canvas(self.fen, bg="white", width=width, height= height)
        self.canvas2.configure(cursor="crosshair")
        self.canvas2.pack(side="bottom")


#Fonction permettant de créer un point au click de la souris
def point(event):
    points.append((event.x,event.y))
    if(len(points) >= 2):
        main.canvas.create_line(points, tags="line", width= 1)
        main.canvas.tag_lower("line")
    main.canvas.create_oval(event.x - 8, event.y - 8, event.x+8, event.y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt"],width="2",)
    main.canvas.create_line(event.x,event.y,event.x +1,event.y + 1,fill="blue", width= 1,tags="line2")
    main.canvas.tag_bind("first","<Button-1>",polygon)
    return points

#Fonction permettant de créer le polygone suite au click de fermeture avec le premier point créé
def polygon(event) :
    global canpoly
    canpoly = True
    main.canvas.create_line(points[0][0],points[0][1],points[-1][0],points[-1][1], tags="line", width= 1)
    main.canvas.create_polygon(*points, fill='red')
    main.canvas.tag_raise("line")
    main.canvas.unbind("<Button 1>")
    main.canvas.delete("line2")
    print(points)

#Fonction permettant de retourner au menu principal
def leave():
    try:
        main.fen.destroy()
        main.fen2.destroy()
    except:
        print("")
    os.system('python menu.py')
    exit()

#Fonction qui récupère les données de personnalisation
def getperso():
    global sommet1,sommet2,sommet3
    try:
        with open("fav.txt","r") as f:
            lines=f.readlines()
            sommet1 = lines[1].strip().replace(" ", "")
            sommet2 = lines[2].strip().replace(" ", "")
            sommet3 = lines[3].strip().replace(" ", "")
    except :
        #Si le fichier n'existe pas :
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

#Classe permettant de manipuler la partie multijoueur
global g,datab
global xm,ym,colorm

class Game:


    def __init__(self):
        global datab,winmulti
        winmulti = False
        datab = "none"
        try:
            self.net = Network()
        except:
            print("Erreur de connexion")
            try:
                main.fen.destroy()
                main.fen2.destroy()
            except:
                print("")
            os.system('python jeu.py')
            exit()
        self.player = Player()
        self.player2 = Player()


    def update(self):
        global winmulti,datab
        while winmulti != True:
            self.player2.up = self.parse_data(self.send_data())
            print("RECV",self.player2.up)
            time.sleep(1)
        datab = "WINNER"
        self.player2.up = self.parse_data(self.send_data())
        time.sleep(1)

    def send_data(self):
        global datab
        data = str(self.net.id) + ":" + str(datab)
        reply = self.net.send(data)
        return reply


    @staticmethod
    def parse_data(data):
        global xm,ym,colorm,g
        try:
            d = data.split(":")[1]
            print("Data : ",d)
            if ("WINNER" in d):
                if messagebox.askyesno("C'est perdu !","Dommage ! Rejouer ?"):
                    main.fen.destroy()
                    os.system('python jeu.py')
                else:
                    main.fen.destroy()
                    os.system('python menu.py')
            else:
                if("NONE" not in d):
                    xm = d.split(",")[0].replace("(","")
                    xm = int(xm.replace(" ",""))
                    ym = d.split(",")[1]
                    ym = int(ym.replace(" ",""))
                    colorm = d.split(",")[2].replace(")","")
                    colorm = colorm.replace("'","")
                    colorm = colorm.replace(" ","")
            return d
        except:
            return 0


#Fonction actualisant le canvas n°2
def updatep2():
    try:
        el = main.canvas2.find_closest(xm,ym)
        main.canvas2.itemconfig(el, fill=colorm)
    except Exception as e: pass
    main.fen.after(50, updatep2)

#Classe gérant le joueur en multijoueur
class Player():

    def __init__(self):
        self.up = 0

#Fonction permettant de configurer la partie multijoueur
def multiplayer():
    global xm,ym,colorm
    global g
    main.multi()
    main.clear()
    g = Game()
    conn = "yey"
    start_new_thread(gupdate, (conn,))

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
                main.canvas2.create_oval(x - 8, y - 8, x+8, y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt"],width="2",)
                main.canvas2.create_polygon(*points, fill='red',width=1,outline="black")
        main.fen2.destroy()
        main.bouton_valider.config(state=NORMAL)
        main.bouton_valider.config(command=validateb)
        startg()
        startgb()

        updatep2()
        main.fen.mainloop()

def gupdate(*args):
    g.update()

#Fonction permettant de configurer une partie en mode aléatoire
def randomg():
    global width,height,points
    print("Random g")
    main.fen2.destroy()
    nb = 6
    points = GPoly(nb).generate(nb)
    print("PT save : " ,points)
    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        main.canvas.create_oval(x - 8, y - 8, x+8, y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt"],width="2",)
        main.canvas.create_polygon(*points, fill='red',width=1,outline="black")
    main.bouton_valider.config(state=NORMAL)
    startg()

#Fonction permettant de configurer une partie en mode import
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

#Fonction permettant de demarrer une partie après l'import
def startg():
    global g
    trianguler()
    global sommet1,sommet2,sommet3
    colors = [sommet1,sommet2,sommet3]
    global bliste,triliste,sumb
    sumb = []
    for el in triliste:
        sumb.append(el)
    bliste = []
    for el in triliste:
        bliste.append(el)
    for j in range (0,3):
        main.canvas.create_oval(bliste[0][j][0] - 8, bliste[0][j][1] - 8, bliste[0][j][0]+8,bliste[0][j][1]+8, fill=colors[j],tags=str(bliste[0][j][0])+","+str(bliste[0][j][1]),width="2")
        print("colorin",getColor(bliste[0][j]))
    for x in range(1,len(bliste)):
        for j in range (0,3):
            if not getColor(bliste[x][j]):
                main.canvas.create_oval(bliste[x][j][0] - 8, bliste[x][j][1] - 8, bliste[x][j][0]+8,bliste[x][j][1]+8, fill="yellow",tags=str(bliste[x][j][0])+","+str(bliste[x][j][1]),width="2")
                main.canvas.tag_bind((str(bliste[x][j][0])+","+str(bliste[x][j][1])), "<Button-1>",clickbb)

#Fonction permettant de demarrer une partie après l'import bis
def startgb():
    global sommet1,sommet2,sommet3
    colors = [sommet1,sommet2,sommet3]
    global bliste2,triliste,sumb
    bliste2 = []
    for el in sumb:
        bliste2.append(el)
    for j in range (0,3):
        main.canvas2.create_oval(bliste2[0][j][0] - 8, bliste2[0][j][1] - 8, bliste2[0][j][0]+8,bliste2[0][j][1]+8, fill=colors[j],tags=str(bliste2[0][j][0])+","+str(bliste2[0][j][1]),width="2")
    for x in range(1,len(bliste2)):
        for j in range (0,3):
            if not getColorb(bliste2[x][j]):
                main.canvas2.create_oval(bliste2[x][j][0] - 8, bliste2[x][j][1] - 8, bliste2[x][j][0]+8,bliste2[x][j][1]+8, fill="yellow",tags=str(bliste2[x][j][0])+","+str(bliste2[x][j][1]),width="2")

#Fonction permettant de changer la couleur du point cliqué
def clickbb(event):
    global g,datab
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
    datab = (x,y,color)
    main.canvas.itemconfig(el, fill=color)

#Fonction permettant de changer la couleur du point cliqué bis
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

#Fonction validant la tricoloration ou non (Mode solo)
def validate():
    init = []
    global bliste,verif
    for el in bliste:
        for j in range(0,3):
            if ((el[j][0],el[j][1]),getColor(el[j])) not in init :
                init.append(((el[j][0],el[j][1]),getColor(el[j])))
    coloration()
    if verif == init:
        print("-> WIN")
        if messagebox.askyesno("C'est gagné !","Rejouer ?"):
            main.fen.destroy()
            os.system('python jeu.py')
        else:
            main.fen.destroy()
            os.system('python menu.py')
    else :
        messagebox.showinfo("Perdu", "Hum, il me semble que cela ne soit pas la bonne réponse")

#Fonction validant la tricoloration ou non (Mode multijoueur)
def validateb():
    global winmulti
    init = []
    global bliste,verif
    for el in bliste:
        for j in range(0,3):
            if ((el[j][0],el[j][1]),getColor(el[j])) not in init :
                init.append(((el[j][0],el[j][1]),getColor(el[j])))
    coloration()
    if verif == init:
        winmulti = True
        print("-> WIN")
        if messagebox.askyesno("C'est gagné !","Rejouer ?"):
            main.fen.destroy()
            os.system('python jeu.py')
            report.print()
        else:
            main.fen.destroy()
            os.system('python menu.py')
    else :
        messagebox.showinfo("Perdu", "Hum, il me semble que cela ne soit pas la bonne réponse")

#-----Triangulation-----#

#Fonction renvoyant le point le plus à gauche du polygone
def gauche(points):
    n = len(points)
    x = points[0][0]
    j = 0
    for i in range(1,n):
        if points[i][0] < x :
            x = points[i][0]
            j = i
    return j

#Fonction permettant de savoir de quel coté d'une droite le point se situe
def cotedroite(p0,p1,M):
    return (p1[0]-p0[0])*(M[1]-p0[1])-(p1[1]-p0[1])*(M[0]-p0[0])

#Fonction renvoyant l'index suivant d'un point selon l'écart selectionné
def voisin_sommet(n,i,di):
    return (i+di)%n

#Fonction permettant de savoir si un point est dans un triangle
def danstriangle(triangle,M):
    p1 = triangle[0]
    p2 = triangle[1]
    p3 = triangle[2]
    return cotedroite(p1,p2,M) > 0 and cotedroite(p2,p3,M) > 0 and cotedroite(p3,p1,M) > 0

#Fonction renvoyant l'indice du point étant le plus éloigné de p1 et p2 et étant dans le triangle
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

#Fonction générant un polygon à partir des indices fournis
def poly(points,start,finish):
    n = len(points)
    p= []
    i = start
    while i!=finish:
        p.append(points[i])
        i = voisin_sommet(n,i,1)
    p.append(points[finish])
    return p

#Fonction récursive permettant le calcul de la triangulation
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

#Fonction renvoyant la liste des triangles issus de la triangulation
def triangulerbis(points):
    liste = []
    triangulationb(points,liste)
    return liste

#Fonction permettant de tracer les triangles issus de la triangulation
def drawT(liste):
    for triangle in liste:
        main.canvas.create_line(triangle[0][0],triangle[0][1],triangle[1][0],triangle[1][1], tags="triangl", width= 1)
        main.canvas.create_line(triangle[0][0],triangle[0][1],triangle[2][0],triangle[2][1], tags="triangl", width= 1)
        main.canvas.create_line(triangle[1][0],triangle[1][1],triangle[2][0],triangle[2][1], tags="triangl", width= 1)

def clock(polygon):
    s = 0
    n = len(polygon)
    for i in range(n):
        point = polygon[i]
        point2 = polygon[(i + 1) % n]
        s += (point2[0] - point[0]) * (point2[1] + point[1])
    return s > 0

#Fonction principale gérant la triangulation
def trianguler():
    if clock(points):
        points.reverse()
    global triliste
    if len(points)>=4:
        start = perf_counter()
        triliste = triangulerbis(points)
        drawT(triliste)
        dt = perf_counter() - start
        print("Performance triangulation:",round(dt * 10**3, 2), " ms pour ", len(points), "points")


#-----Tri-Coloration-----#

#Fonction permettant de savoir si un point d'un triangle est lié à un autre triangle
#Afin de savoir si un triangle est collé au premier
def segmentation(t1,t2):
    success = False
    if((t1[0] in t2 and t1[1] in t2)  or (t1[2] in t2 and t1[1] in t2) or (t1[0] in t2 and t1[2] in t2)):
        success = True

    return (success)


global bliste

#Fonction principale pour la tri-coloration
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

#Fonction renvoyant la couleur et les coordonnées du point qui n'est pas encore coloré sur les deux triangles
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

#Fonction renvoyant la couleur d'un point
def getColor(pt):
    return (main.canvas.itemcget(main.canvas.find_withtag(str(pt[0])+","+str(pt[1])), "fill"))

#Fonction renvoyant la couleur d'un point sur le deuxieme canvas
def getColorb(pt):
    return (main.canvas2.itemcget(main.canvas2.find_withtag(str(pt[0])+","+str(pt[1])), "fill"))

#Sous-fonction récursive permettant la tricoloration à partir d'un index de triangle et du triangle précédent
#permettant ainsi d'empecher la recoloration du triangle précédent
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
