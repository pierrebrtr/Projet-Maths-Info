###################################################################
#Script	: Editeur de polygones + triangulation + tricoloration
#Auteurs : Paul Lefay et Pierre Bertier
###################################################################
    #Tableau des variables:
    #triliste,bliste -> Liste des triangles après la triangulation
    #canpoly-> Test pour savoir si le polygone peut être tracé
    #sommet1,2,3 -> Couleurs liées au fichier de personnalisation
    #cam -> Fichier image caméra
###################################################################
from tkinter import *
import tkinter.filedialog
import tkinter.colorchooser
from math import *
import math
from time import *
import time
import os
print("""


 ___  __  _  ___  _  _  _  _
| __||  \| ||_ _|| |/ \| \| |
| _| | o ) | | | | ( o ) \\ |
|___||__/|_| |_| |_|\_/|_|\_|


""")

points = []
global triliste,canpoly,slowmode,sommet1,sommet2,sommet3,cam

#-----Initialisation-----#

#Initialisation de l'application
def demarrer(w = 500, h = 500):
    global width
    global height
    global main
    global cam
    global triangulet
    triangulet = False
    width = w
    height = h
    main = Application()
    main.canvas.bind("<Button-1>", point)
    main.canvas.bind("<Button-3>", Application.clear)
    main.canvas.bind('<Motion>', move)
    main.canvas.old_coords = None
    cam=PhotoImage(file="camera.png")
    main.fen.mainloop()
    return

#-----Classe principale-----#

#Application principale
class Application:

    def __init__(self):
        getperso()
        global slowmode,canpoly
        canpoly = False
        slowmode = False

        self.fen = Tk()
        self.fen.title("Editeur de polygone")

        self.menubar = Frame(self.fen)
        self.menubar.pack(side="top",fill=X)

        self.fbutton = Menubutton(self.menubar,text="Fichier",underline = 0)
        self.fbutton.pack(side="left")

        self.fbutton2 = Menubutton(self.menubar,text="Personnaliser ",underline = 0)
        self.fbutton2.pack(side="left")

        self.filemenu = Menu(self.fbutton)
        self.filemenu.add_command(label="Enregistrer le polygone",command = export)
        self.filemenu.add_command(label="Ouvrir un polygone",command = openb)
        self.filemenu.add_command(label="Quit",command = self.fen.destroy)
        self.fbutton.config(menu=self.filemenu)

        self.filemenu2 = Menu(self.fbutton2)
        self.filemenu2.add_command(label="Couleur sommet tricoloration #1",command= lambda: perso(1))
        self.filemenu2.add_command(label="Couleur sommet tricoloration #2",command= lambda: perso(2))
        self.filemenu2.add_command(label="Couleur sommet tricoloration #3",command= lambda: perso(3))
        self.fbutton2.config(menu=self.filemenu2)

        self.canvas = Canvas(self.fen, bg="white", width=width, height= height)
        self.canvas.configure(cursor="crosshair")
        self.canvas.pack(side="left")

        self.frame = Frame(self.fen)
        self.frame.pack(side="right")

        self.textbox = Label(self.frame,text="Menu",font=("Helvetica", 16))
        self.textbox.grid(row=0,column=1)

        self.bouton_trianguler = Button(self.frame, text="Trianguler", bg = "grey",command=trianguler)
        self.bouton_trianguler.grid(row=2,column =1,pady=10)
        self.bouton_trianguler.config(state=DISABLED)

        self.bouton_coloration = Button(self.frame, text="Coloration", bg = "blue",command=coloration)
        self.bouton_coloration.grid(row=5,column =1,pady=10)
        self.bouton_coloration.config(state=DISABLED)

        self.bouton_clear = Button(self.frame, text="Effacer", bg = "grey",command=self.clear)
        self.bouton_clear.grid(row=6,column =1,pady=10)


        self.bouton_quitter = Button(self.frame, text="Menu", bg = "red",command=leave)
        self.bouton_quitter.grid(row=7,column =1,pady=10)


        self.bouton_camera = Button(self.frame, text="Chiffres", bg = "green",command=chiffre)
        self.bouton_camera.grid(row=4,column =1,pady=10)
        self.bouton_camera.config(state=DISABLED)

        self.bouton_chiffre = Button(self.frame, text="Cameras", bg = "green",command=camera)
        self.bouton_chiffre.grid(row=3,column =1,pady=10)
        self.bouton_chiffre.config(state=DISABLED)
        self.var = IntVar()
        self.bouton_slow = Checkbutton(self.frame, text="Ralentir", command=self.slow_mode, variable=self.var)
        self.bouton_slow.grid(row=8,column =1,pady=10)

    #Fonction permettant d'effacer l'écran et de réinitialiser tout le programme
    def clear(self):
        global canpoly,triangulet
        canpoly = False
        points.clear()
        main.canvas.delete("all")
        main.canvas.bind("<Motion>",move)
        main.canvas.bind("<Button-1>", point)
        main.bouton_trianguler.config(state=DISABLED)
        main.bouton_coloration.config(state=DISABLED)
        main.bouton_chiffre.config(state=DISABLED)
        main.bouton_camera.config(state=DISABLED)
        triangulet = False

    #Fonction permettant de ralentir les calculs afin d'observer plus facilement les calculs
    def slow_mode(event):
        global slowmode
        slowmode = event.var.get()
        print("Ralentissement ? :",event.var.get())

#Fonction permettant de retourner au menu principal
def leave():
    main.fen.destroy()
    os.system('python menu.py')
    exit()

#Fonction permettant de créer un point au click de la souris
def point(event):
    points.append((event.x,event.y))
    if(len(points) >= 2):
        main.canvas.create_line(points, tags="line", width= 1)
        main.canvas.tag_lower("line")
    main.canvas.create_oval(event.x - 8, event.y - 8, event.x+8, event.y+8, fill="red",tags=[('first' if len(points) == 1 else 'sec'),"pt",(event.x,event.y)],width="2",)
    main.canvas.create_line(event.x,event.y,event.x +1,event.y + 1,fill="blue", width= 1,tags="line2")
    main.canvas.tag_bind("first","<Button-1>",polygon)
    return points

#Fonction permettant de créer le polygone suite au click de fermeture avec le premier point créé
def polygon(event) :
    global canpoly
    canpoly = True
    main.canvas.create_polygon(*points, fill='red',width=1,outline="black",tags="polygone")
    main.canvas.delete("line")
    main.canvas.unbind("<Button 1>")
    main.canvas.unbind("<Motion>")
    main.canvas.delete("line2")
    main.canvas.tag_bind("first","<ButtonPress-1>",drag1)
    main.canvas.tag_bind("sec","<ButtonPress-1>",drag1)
    main.bouton_trianguler.config(state=NORMAL)
    main.canvas.tag_lower("polygone")

global dragged
global ib



def drag1(event):
    global dragged
    el = main.canvas.find_closest(event.x, event.y)
    cb = main.canvas.coords(el)
    xb = int(cb[0] + 8)
    yb = int(cb[1] + 8)
    global ib
    for i in range(len(points)):
        if (xb,yb) == points[i]:
            ib = i
    dragged = 1
    main.canvas.tag_bind(el,"<Motion>",drag2)
    main.canvas.tag_bind(el,"<ButtonRelease-1>",drag3)

def drag2(event):
    global ib
    global dragged
    global triangulet
    x = event.x
    y = event.y
    el = main.canvas.find_closest(x, y)
    if dragged != 0:
        main.canvas.coords(el, x - 8, y - 8, x + 8, y + 8)
        cb = main.canvas.coords(el)
        xb = int(cb[0] + 8)
        yb = int(cb[1] + 8)
        main.canvas.delete("polygone")
        points[ib] = (xb,yb)
        polygon(event)
        if triangulet:
            main.canvas.delete("triangl")
            trianguler()
            main.canvas.lower("triangl")
            main.canvas.lower("polygone")


def drag3(event):
    global dragged,ib
    dragged = 0



#Fonction liée au processus de prévisualisation d'un segement entre un point créé
#et un point encore inexistant
def move(event):
    x, y = event.x, event.y
    if len(points)>=1:
        if main.canvas.old_coords:
            x1, y1 = main.canvas.old_coords
            main.canvas.tag_lower("line2")
            main.canvas.coords("line2", points[len(points)-1][0], points[len(points)-1][1], x1, y1)
        main.canvas.old_coords = x, y

#-----Menu bis-----#

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

#Dialogue de demande de personnalisation de couleur
def perso(index):
    global sommet1,sommet2,sommet3
    color = tkinter.colorchooser.askcolor()[1]
    if color:
        if (index == 1):
            sommet1 = color
        elif (index ==2):
            sommet2 = color
        elif (index == 3):
            sommet3 = color
        with open("fav.txt","w") as f:
            f.write("Perso\n")
            f.write(sommet1+"\n")
            f.write(sommet2+"\n")
            f.write(sommet3+"\n")

#Exportation d'un polygone
def export():
    global canpoly
    if (canpoly) :
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            print("Annulation")
            return
        save = points
        for el in points:
            f.write(str(el[0])+ "," + str(el[1]) +"\n")
        f.close()
    print("export")

#Fonction permettant l'importation d'un polygone à partir d'un fichier texte
def openb():
    global canpoly
    canpoly = True
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
                main.canvas.create_line(x,y,x +1,y + 1,fill="blue", width= 1,tags="line2")
                main.canvas.tag_bind("first","<Button-1>",polygon)
                main.canvas.create_polygon(*points, fill='red',width=1,outline="black")
                main.canvas.tag_raise("line")
                main.canvas.unbind("<Button 1>")
                main.canvas.unbind("<Motion>")
                main.canvas.delete("line2")
                main.bouton_trianguler.config(state=NORMAL)
                main.canvas.lower("polygone")
                print("POINTS",points)

#-----Triangulation-----#

global cpt

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
    global cpt
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
        if slowmode:
            main.fen.update()
            time.sleep(1)



def clock(polygon):
    s = 0
    n = len(polygon)
    for i in range(n):
        point = polygon[i]
        point2 = polygon[(i + 1) % n]
        s += (point2[0] - point[0]) * (point2[1] + point[1])
    return s > 0


global triangulet

#Fonction principale gérant la triangulation
def trianguler():

    global triangulet
    triangulet = True
    if clock(points):
        points.reverse()
    global triliste
    if len(points)>=4:
        start = perf_counter()
        triliste = triangulerbis(points)
        drawT(triliste)
        dt = perf_counter() - start
        print("Performance triangulation:",round(dt * 10**3, 2), " ms pour ", len(points), "points")
        main.bouton_chiffre.config(state=NORMAL)
        main.bouton_camera.config(state=NORMAL)
        main.bouton_coloration.config(state=NORMAL)
    print("Il faut ", len(triliste), " gardes pour surveiller la zone")
    main.canvas.tag_raise("sec")
    main.canvas.tag_raise("first")

#Fonction affichant l'index du triangle sur le triangle
def chiffre():
    global triliste
    if (len(points)>=4):
        liste = triliste
        for i in range(len(liste)):
            x = (liste[i][0][0]+liste[i][1][0]+liste[i][2][0])/3
            y = (liste[i][0][1]+liste[i][1][1]+liste[i][2][1])/3
            main.canvas.create_text(x,y,text=i)

#Fonction affichant l'image caméra  sur le triangle
def camera():
    print("CAMERAS")
    global triliste,cam
    if (len(points)>=4):
        liste = triliste
        for i in range(len(liste)):
            x = (liste[i][0][0]+liste[i][1][0]+liste[i][2][0])/3
            y = (liste[i][0][1]+liste[i][1][1]+liste[i][2][1])/3

            main.canvas.create_image(x,y,image=cam)

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
    global sommet1,sommet2,sommet3
    start = perf_counter()
    colors = [sommet1,sommet2,sommet3]
    global bliste,triliste
    bliste = []
    for el in triliste:
        bliste.append(el)
    for j in range (0,3):
        main.canvas.create_oval(bliste[0][j][0] - 8, bliste[0][j][1] - 8, bliste[0][j][0]+8,bliste[0][j][1]+8, fill=colors[j],tags=str(bliste[0][j][0])+","+str(bliste[0][j][1]),width="2")
        if slowmode:
            main.fen.update()
            time.sleep(1)
    subliste = []
    for x in range(len(bliste)):
        if (0 != x and bliste[x] not in subliste):
            if(segmentation(bliste[0],bliste[x])):
                subliste.append(x)
    for el in subliste:
        recurTricolor(el,0)
    dt = perf_counter() - start
    print("Performance tri-coloration :",round(dt * 10**3, 2), " ms pour ", len(points), "points")

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

#Sous-fonction récursive permettant la tricoloration à partir d'un index de triangle et du triangle précédent
#permettant ainsi d'empecher la recoloration du triangle précédent
def recurTricolor(index,indexb):
    global slowmode
    global bliste
    point = getPoint(bliste[index],bliste[indexb])[0][0]
    couleur = getPoint(bliste[index],bliste[indexb])[1][1]
    main.canvas.create_oval(point[0]- 8,point[1] - 8,point[0]+8,point[1]+8, fill=couleur,tags=str(point[0])+","+str(point[1]),width="2")
    if slowmode:
        main.fen.update()
        time.sleep(1)
    subliste = []
    for x in range(len(bliste)):
        if (index != x and indexb != x and bliste[x] not in subliste):
            if(segmentation(bliste[index],bliste[x])):
                subliste.append(x)
    for el in subliste:
        recurTricolor(el,index)

#-----Initialisation-----#
demarrer()
