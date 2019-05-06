
##Some old fashion functions that didn't make it


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


         
##def recur(index,mode,prec):
##    subliste = [-1]
##    print("---------")
##    print("RECURSION AVEC " + str(index))
##    global bliste
##    c = 0
##    for x in range(len(bliste)):
##        if (bliste[x] != "N" and bliste[index] != "N" and index != x):
##            if(segmentation(bliste[index],bliste[x])):
##                c= c +1
##                subliste.append(x)
##    print("Nb d'occurences : " + str(c) + ",liste : " + str(subliste))
##
##    
##    for x in range(len(bliste)):
##        if (bliste[x] != "N" and bliste[index] != "N" and index != x):
##            if(segmentation(bliste[index],bliste[x])):
##                print("Triangle n°" + str(x) + " collé à triangle n°" + str(index))
##                triangle = bliste[x]
##                colors = ["red","green","blue"]
##                ide = [0,1,2]
##                if mode ==1:
##                    print("")
##                    for i in range (len(triangle)):
##                        if (triangle[i] in bliste[prec]):
##                            try:
##                                colors.remove(main.canvas.itemcget(main.canvas.find_withtag(str(triangle[i][0])+","+str(triangle[i][1])), "fill"))
##                                ide.remove(i)
##                            except:
##                                print("--------")
##                                print("ERREUR")
##                                print("--------")
##                else :
##                    for i in range (len(triangle)):
##                        if (triangle[i] in bliste[index]):
##                            try:
##                                colors.remove(main.canvas.itemcget(main.canvas.find_withtag(str(triangle[i][0])+","+str(triangle[i][1])), "fill"))
##                                ide.remove(i)
##                            except:
##                                print("--------")
##                                print("ERREUR")
##                                print("--------")
##                y = ide[0]
##                main.canvas.create_oval( triangle[y][0]- 8, triangle[y][1] - 8, triangle[y][0]+8,triangle[y][1]+8, fill=colors[0],tags=str(triangle[y][0])+","+str(triangle[y][1]),width="2")
##                print("POINT : ", triangle[y],colors[0])
##                if c < 2:
##                    print("SET N TO ",index)
##                    bliste[index] = "N"
##                print("NEXT ->", str(x))
##                recur(x,0,0)
##    for i in range(1,len(subliste)):
##        if subliste[i] != -1:
##            recur(index,1,x)


