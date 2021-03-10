# main.py - chess board project
import tkinter as tk
import random
from PIL import Image, ImageTk
import numpy as np
import pygame
import random
import datetime

pygame.mixer.init(44100, -16, 2, 512)
pygame.mixer.init()
sound1 = pygame.mixer.Sound("sounds/move6.ogg")
sound2 = pygame.mixer.Sound("sounds/move7.ogg")




class Board(tk.Tk):
    """
    La classe Board permet de représenter un plateau de jeu.
    un object Board contient un plateau sous la forme d'une matrice
    [
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x,x]
    ]
    
    chaque emplacement 'x' peut contenir un objet Pion ou un None
    """
    
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("NSICHESS XTREME 2 DELUXE PREMIUM [CRACK]")
        #self.plateau = [[None for i in range(8)] for i in range(8)]
        
        self.tour = "W"
        self.selectedCase = None
        
        
        self.plateau = [
            [Pion('T','B'), Pion('C','B'), Pion('F','B'), Pion('Q','B'), Pion('R', 'B'), Pion('F','B'), Pion('C','B'), Pion('T','B')],
            #[Pion('P','B') for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            #[Pion('P','W') for i in range(8)],
            [Pion('T','W'), Pion('C','W'), Pion('F','W'), Pion('Q','W'), Pion('R', 'W'), Pion('F','W'), Pion('C','W'), Pion('T','W')]
            ]
            
        self.plateau[5][5] = Pion('Q','B')
            
        self.coordLettre = ['a','b','c','d','e','f','g','h']
        self.coordChiffre =["8","7","6","5","4","3","2","1"]
        self.coupsJouables = []
        
        self.sprites = {
                        "TW" : ImageTk.PhotoImage(Image.open("sprites/WT.png").convert("RGBA").resize((75,75))),
                        "CW" : ImageTk.PhotoImage(Image.open("sprites/WKN.png").convert("RGBA").resize((75,75))),
                        "FW" : ImageTk.PhotoImage(Image.open("sprites/WB.png").convert("RGBA").resize((75,75))),
                        "RW" : ImageTk.PhotoImage(Image.open("sprites/WK.png").convert("RGBA").resize((75,75))),
                        "QW" : ImageTk.PhotoImage(Image.open("sprites/WQ.png").convert("RGBA").resize((75,75))),
                        "PW" : ImageTk.PhotoImage(Image.open("sprites/WP.png").convert("RGBA").resize((75,75))),

                        "TB" : ImageTk.PhotoImage(Image.open("sprites/BT.png").convert("RGBA").resize((75,75))),
                        "CB" : ImageTk.PhotoImage(Image.open("sprites/BKN.png").convert("RGBA").resize((75,75))),
                        "FB" : ImageTk.PhotoImage(Image.open("sprites/BB.png").convert("RGBA").resize((75,75))),
                        "RB" : ImageTk.PhotoImage(Image.open("sprites/BK.png").convert("RGBA").resize((75,75))),
                        "QB" : ImageTk.PhotoImage(Image.open("sprites/BQ.png").convert("RGBA").resize((75,75))),
                        "PB" : ImageTk.PhotoImage(Image.open("sprites/BP.png").convert("RGBA").resize((75,75)))
                        }
                        
        #Image.open('sprites/WT.png').show
                        
        self.canvas = tk.Canvas(bd=0, height=830, width=830, cursor='hand2')
        #b = ImageTk.PhotoImage(file="sprites/WK.png")
        #self.canvas.create_image((50,50), image=b) # wtf pourquoi elles s'affichent pas ?
        #self.canvas.image = b
        #self.canvas.pack()            
        
        
        self.updateDisplay()
    
    def transparent(self, path):
        handle = Image.open(path)
        
        handle.putalpha(30)
        return handle

    def toString(self):
        
        # on charge d'abord les deux listes d'indexs, lettre puis chiffre afin de communiquer
        # la rotation actuelle du plateau.
        
        # une pièce et sa position est sous la forme "a8TB" (lettreChiffreValeurCouleur)
        
        sE = ""
        
        for l in range(len(self.plateau)):
            for c in range(len(self.plateau[l])):
                if self.plateau[l][c] is not None :
                    sE += f"{self.coordLettre[c]}{self.coordChiffre[l]}{self.plateau[l][c].valeur}{self.plateau[l][c].couleur}" 
        return sE
    
    def loadFromString(self, string):
        piecesList = []
        
        for index, char in enumerate(string):
            if index%4 == 0 : # nouvelle pièce :
                piecesList.append("".join(string[index:index+4]))
        
        
        
        nouveauPlateau = [
        [None for i in range(8)] for j in range(8)
        ]
        
        for i in piecesList :
            lettreIndex = self.coordLettre.index(i[0])
            chiffreIndex = self.coordChiffre.index(i[1])
            pion = Pion(i[2], i[3])
            
            nouveauPlateau[chiffreIndex][lettreIndex] = pion
        
        self.plateau = nouveauPlateau
        self.updateDisplay()
        return nouveauPlateau


    def mouvePion(self, deplacement):
        pass
    
    def retournePlateau(self):
        self.plateau = np.flip(self.plateau, (0,1)).tolist()
        self.coordLettre = np.flip(self.coordLettre, 0).tolist()
        self.coordChiffre = np.flip(self.coordChiffre, 0).tolist()
        self.updateDisplay()
        print("flipped the board")
    
    
    def finPartie(self):
        pass
    
    def partie(self):
        pass
        
    def updateDisplay(self):
    
    
        
    
        self.canvas.delete("all")
    
        color = "beige"
        def toggle(color):
            return "beige" if color == "brown" else "brown"
        def playMoveSound():
            sounds = [sound1, sound2]
            return pygame.mixer.Sound.play(random.choice(sounds))
            
        def clickEvent(event):
            
            colonne = event.x//100
            ligne = event.y//100
            
            if colonne < 8 and ligne < 8 : # si une case est sélectionnée
            
                
                pionstr = f"{self.plateau[ligne][colonne].valeur}{self.plateau[ligne][colonne].couleur}" if self.plateau[ligne][colonne] is not None else "Empty"
                print(f"clicked at x={event.x} ; y={event.y} | case {self.coordLettre[colonne]}{self.coordChiffre[ligne]} | pion : {pionstr}")
                if self.plateau[ligne][colonne] is not None and self.plateau[ligne][colonne].couleur == self.tour and f"{self.coordLettre[colonne]}{self.coordChiffre[ligne]}".upper() != self.selectedCase: # si on sélectionne une pièce de notre couleur
                
                	# si un pion est sélectionné
                
                    playMoveSound()
                    arbreDeplacement = ArbreDeplacement(f'{self.coordLettre[colonne]}{self.coordChiffre[ligne]}'.upper(), f'{pionstr[0]}', self)
                    print(pionstr[0])
                    print(arbreDeplacement.DeplacementPion())
                    self.coupsJouables = arbreDeplacement.DeplacementPion()
                    self.updateDisplay()
                    self.selectedCase = f'{self.coordLettre[colonne]}{self.coordChiffre[ligne]}'.upper()

                
                elif f"{self.coordLettre[colonne]}{self.coordChiffre[ligne]}".upper() in self.coupsJouables : # on clique sur une case valide
                	
                	playMoveSound()
                	
                	self.plateau[ligne][colonne] = self.plateau[self.coordChiffre.index(self.selectedCase[1])][self.coordLettre.index(self.selectedCase[0].lower())]
                	self.plateau[self.coordChiffre.index(self.selectedCase[1])][self.coordLettre.index(self.selectedCase[0].lower())] = None 
                	print(f"Moved {self.selectedCase} to {self.coordLettre[colonne].upper()}{self.coordChiffre[ligne]}")
                	
                	self.coupsJouables = []
                	self.selectedCase = None
                	self.tour = "B" if self.tour == "W" else "W"
                	#self.retournePlateau()
                	self.updateDisplay()
                	
                else : # si on clique sur n'importe quel autre endroit
                	self.coupsJouables = []
                	self.selectedCase = None
                	self.updateDisplay()
                	
                	
        
            
                

                
            
                
            
            
        #implémentation sous forme de boutons :
        #for l,line in enumerate(self.plateau) : 
        #    for c,case in enumerate(line) :
        #        textButton = case.valeur if case is not None else " "
        #        button=tk.Button(text=textButton, width = "2", height = "2", bg=color) 
        #        button.grid(row = l, column = c)
        #        color = toggle(color)
        #    color = toggle(color)
        
        #implémentation sous forme de canvas
        label = tk.Label(self,text="ici on peut mettre du texte hihi")
        label.grid(row=0, column=0)
        label = tk.Label(self,text="Texte sur le côté")
        label.grid(row=0, column=1)
        labelFrame = tk.LabelFrame(self,text="Debug Buttons", width="50")
        labelFrame.grid(row=1, column=1)
        button1 = tk.Button(labelFrame, text="Flip the board", command = self.retournePlateau)
        button1.pack()
        button2 = tk.Button(labelFrame, text="Play sound", command = lambda : playMoveSound())
        button2.pack()
        
        #on doit ensuite créer 64 carrés d'une couleur différente, sous forme
        #de polygones avec la méthode canvas.create_rectangle(x0,y0,x1,y1, fill=color, outline="black")
        for l, line in enumerate(self.plateau):
            for c, case in enumerate(line) :
                # dessin du plateau
                self.canvas.create_rectangle(c*100,l*100,c*100+100,l*100+100, fill=color,width=3, outline="black")
                # dessin des pièces
                
                sprPiece = f"{case.valeur}{case.couleur}" if case is not None else None
                if sprPiece is not None :
                    self.canvas.create_image((c*100+50,l*100+50), image=self.sprites[sprPiece]) # wtf pourquoi elles s'affichent pas ?
                    self.canvas.image=self.sprites[sprPiece]
                    #print(self.sprites[sprPiece])
                    #print(sprPiece)
                
                color = toggle(color)
            color = toggle(color)
            
        for position in self.coupsJouables : # affichage d'un point bleu pour les points jouables
            lettre = position[0].lower()
            nombre = position[1].lower()
            
            x = self.coordLettre.index(lettre)
            y = self.coordChiffre.index(nombre)
            
            self.canvas.create_oval(x*100-10+50, y*100-10+50, x*100+10+50, y*100+10+50, fill='blue', stipple='gray50', outline = None)
            
            
            
            
            
            
            
        for i, coords in enumerate(self.coordLettre):
            self.canvas.create_text(i*100+9, 812 , text=coords,font="Times 15 italic bold")
        for i, coords in enumerate(self.coordChiffre):
            self.canvas.create_text(812,i*100+10, text=coords, font="Times 15 italic bold")
        
        self.canvas.bind("<Button-1>", clickEvent)
        self.canvas.grid(row=1, column=0)
        
        
        labelFrame = tk.LabelFrame(self, text="Board string representation")
        labelFrame.grid(row=2, column=0)
        label = tk.Label(labelFrame, text=self.toString(), width = 50, wraplength=500, padx=50, pady=10)
        label.pack()
        label = tk.Label(labelFrame, text=f"updated at {datetime.datetime.now()}")
        label.pack()
        label = tk.Label(labelFrame, text=f"{'White' if self.tour == 'W' else 'Black'} have to play.")
        label.pack()
        
        
                
        
        
        
    
    def __repr__(self):
    
        stringBoard = ""
        for ligne in self.plateau:
            for case in ligne :
                stringBoard += " " if case == None else case.valeur
                stringBoard += " "
            stringBoard += "\n"
        return stringBoard.strip()

class Pion(object):
    """
    La classe Pion permet de représenter un pion
    Un objet pion contient une valeur montrant la valeur du pion
    et sa couleur sous la forme 'WP' -> white pawn
    'BB' -> Black bishop
    """
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur
    def promote(self, NouvelleValeur):
        if NouvelleValeur.upper() in ["P","T","C","F","Q"]:
            pass



class Noeud():
    """
    P = Pion
    T = Tour
    C = Cavalier
    F = Fou
    Q = Reine
    K = Roi
    """
    def __init__(self, positionDuPion):
            self.positionPion=positionDuPion
            self.branches=[]
            
            
            
    def nord(self):  
        if int(self.positionPion[1]) <8:
            self.branches.append(
                Noeud(self.positionPion[0]+str(int(self.positionPion[1])+1))
                )
            self.branches[-1].nord()
        
    def sud(self):

       if int(self.positionPion[1]) > 1:
            self.branches.append(
                Noeud(self.positionPion[0]+str(int(self.positionPion[1])-1))
                )
            self.branches[-1].sud()
    
    
    def est(self):

        if ord(self.positionPion[0].lower()) < 104 :
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())+1).upper()+self.positionPion[1])
                                 )
            self.branches[-1].est()
    
    def ouest(self):

        if ord(self.positionPion[0].lower()) > 97:
            self.branches.append( 
                Noeud(chr(ord(self.positionPion[0].lower())-1).upper()+self.positionPion[1])
                )
            self.branches[-1].ouest()
            
    
    def nord_est(self):
        if int(self.positionPion[1]) <8 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())+1).upper()+str(int(self.positionPion[1])+1))
                )
            self.branches[-1].nord_est()
        
        
    def nord_ouest(self):
        if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())-1).upper()+str(int(self.positionPion[1])+1))
                )
            self.branches[-1].nord_ouest()
    
    def sud_est(self):
        if int(self.positionPion[1]) >1 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())+1).upper() + str(int(self.positionPion[1])-1))
                      )
            self.branches[-1].sud_est()
    
    def sud_ouest(self):
        if int(self.positionPion[1]) >1 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())-1).upper()+str(int(self.positionPion[1])-1))
                )     
            self.branches[-1].sud_ouest()
    
    def roi(self):
        pass
        
            
    

class ArbreDeplacement():
    """
    la classe arbre creer un arbre de deplacement d'un pion, sans verifiquation au niveau du plateau
    pour obtenir l'arbre sous forme de liste:
        creer l'arbre => ArbreDeplacement('case', 'valeur pion')
        demander via le pion => pion.DeplacementPion()
    """
    def __init__(self, positionPion, valeurPion, board=None):
        self.racine=Noeud(positionPion)
        self.position= positionPion
        self.valeurPion=valeurPion
        self.constructionArbre()
        self.plateau=board.plateau
        self.coordLettre= board.coordLettre
        self.coordChiffre= board.coordChiffre
        
        
    def constructionArbre(self):
        """
        P = Pion
        T = Tour
        C = Cavalier
        F = Fou
        Q = Reine
        R = Roi
        """
        
        if self.valeurPion == "P":
            pass            
        
        if self.valeurPion == "T":
            self.racine.nord()
            self.racine.sud()
            self.racine.est()
            self.racine.ouest()
        
        if self.valeurPion == "C":
            pass
        
        if self.valeurPion == "F":
            self.racine.nord_est()
            self.racine.nord_ouest()
            self.racine.sud_est()
            self.racine.sud_ouest()
        
        if self.valeurPion == "Q":
            self.racine.nord()
            self.racine.sud()
            self.racine.est()
            self.racine.ouest()
            self.racine.nord_est()
            self.racine.nord_ouest()
            self.racine.sud_est()
            self.racine.sud_ouest()
            
        
        if self.valeurPion == "R":
            self.racine.roi()
        
        
    
               
    
    
        
 def DeplacementPion(self):
        """
        renvoi la liste de toute les case posible du pion
        """
        def parcours(noeud, lst, PionBase):
            
            case=noeud.positionPion.lower()
            print(case)
            xPlateau= self.coordLettre.index(case[0])
            yPlateau= self.coordChiffre.index(case[1])
           
            coord=self.plateau[yPlateau][xPlateau]
                    
            #for i in range(len(noeud.branches)):                
                
            if coord is None:
                print(" les coords ne corresponde pas a un pion")
                lst.append(noeud.positionPion)
                for fils in noeud.branches:
                    parcours(fils, lst, PionBase)
            
    
            elif coord is not None: 
                print('les coords montre un pion')
                if coord.couleur != PionBase.couleur:
                    print('la couleur est opposer')
                    #si la couleur du pion sur le plateau est differente de notre pion 
                    lst.append(noeud.positionPion)
                            
        xPion= self.coordLettre.index(self.position[0].lower())
        yPion= self.coordChiffre.index(self.position[1])
        PionBase= self.plateau[yPion][xPion]
        lst=[]
        for fils in self.racine.branches:
            parcours(fils, lst, PionBase)
        return lst
        
        
        
   
        
        
        
        
        
        
        
        

p = Board()

arbrePiece = Noeud("d1")
#p.loadFromString(p.toString())
print('--------------')

p.mainloop()
#p.updateDisplay()




#plateau = liste de liste

#coordChiffre = ['1','2',....,'8']
#coordLettre = ['a','b',....,'h']


#H1 -> 1

#index de 1 dans coordChiffre -> ici c'est zéro

#x = coordChiffre.index('1')
#y = coordLettre.index('H')

#x et y 

#pièce = plateau[x][y] -> objet Pion ou None
