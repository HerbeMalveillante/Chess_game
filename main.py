# main.py - chess board project
import tkinter as tk
import random
from PIL import Image, ImageTk


sprites = {

"TW" : ImageTk.PhotoImage("sprites/WT.png"),
"CW" : ImageTk.PhotoImage("sprites/WKN.png"),
"FW" : ImageTk.PhotoImage("sprites/WB.png"),
"RW" : ImageTk.PhotoImage("sprites/WK.png"),
"QW" : ImageTk.PhotoImage("sprites/WQ.png")





}







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
        
        
        self.plateau = [
            [Pion('T','B'), Pion('C','B'), Pion('F','B'), Pion('R','B'), Pion('Q', 'B'), Pion('F','B'), Pion('C','B'), Pion('T','B')],
            [Pion('P','B') for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pion('P','W') for i in range(8)],
            [Pion('T','W'), Pion('C','W'), Pion('F','W'), Pion('R','W'), Pion('Q', 'W'), Pion('F','W'), Pion('C','W'), Pion('T','W')]
            
            ]
            
        self.coord = ['a','b','c','d','e','f','g','h']
        
        self.sprites = {
                        "TW" : ImageTk.PhotoImage(Image.open("sprites/WT.png").convert("RGBA").resize((80,80))),
                        "CW" : ImageTk.PhotoImage(Image.open("sprites/WKN.png").convert("RGBA").resize((80,80))),
                        "FW" : ImageTk.PhotoImage(Image.open("sprites/WB.png").convert("RGBA").resize((80,80))),
                        "RW" : ImageTk.PhotoImage(Image.open("sprites/WK.png").convert("RGBA").resize((80,80))),
                        "QW" : ImageTk.PhotoImage(Image.open("sprites/WQ.png").convert("RGBA").resize((80,80))),
                        "PW" : ImageTk.PhotoImage(Image.open("sprites/WP.png").convert("RGBA").resize((80,80))),

                        "TB" : ImageTk.PhotoImage(Image.open("sprites/BT.png").convert("RGBA").resize((80,80))),
                        "CB" : ImageTk.PhotoImage(Image.open("sprites/BKN.png").convert("RGBA").resize((80,80))),
                        "FB" : ImageTk.PhotoImage(Image.open("sprites/BB.png").convert("RGBA").resize((80,80))),
                        "RB" : ImageTk.PhotoImage(Image.open("sprites/BK.png").convert("RGBA").resize((80,80))),
                        "QB" : ImageTk.PhotoImage(Image.open("sprites/BQ.png").convert("RGBA").resize((80,80))),
                        "PB" : ImageTk.PhotoImage(Image.open("sprites/BP.png").convert("RGBA").resize((80,80)))
                        }
                        
        #Image.open('sprites/WT.png').show
                        
        self.canvas = tk.Canvas(bd=0, height=800, width=800)
        #b = ImageTk.PhotoImage(file="sprites/WK.png")
        #self.canvas.create_image((50,50), image=b) # wtf pourquoi elles s'affichent pas ?
        #self.canvas.image = b
        #self.canvas.pack()            
        
        
        self.updateDisplay()
    
    def transparent(self, path):
        handle = Image.open(path)
        
        handle.putalpha(30)
        return handle

    def mouvePion(self, deplacement):
        pass
    
    def retournePlateau(self):
        pass
    
    
    def finPartie(self):
        pass
    
    def partie(self):
        pass
        
    def updateDisplay(self):
        color = "beige"
        def toggle(color):
            return "beige" if color == "brown" else "brown"
            
        def clickEvent(event):
            print(f"clicked at x={event.x} ; y={event.y}")
            
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
        label = tk.Label(self,text="Texte sur le côté mais du côté du plateau cette fois ci\nOn peut mettre le score ici par exemple")
        label.grid(row=1, column=1)
        
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
        self.canvas.bind("<Button-1>", clickEvent)
        self.canvas.grid(row=1, column=0)
        
        
                
        
        
        
    
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
    def __init__(self, positionDuPion):
            self.valeur=positionDuPion
            self.branches=[]
            
    
class ArbreDeplacement():
    
    def __init__(self, positionPion, valeurPion):
        self.racine=Noeud(positionPion)
        self.position= positionPion
        self.valeurPion=valeurPion
    
    
    def constructionArbre(self):
        """
        P = Pion
        T = Tour
        C = Cavalier
        F = Fou
        Q = Reine
        K = Roi
        """
        
        if self.valeurPion == "P":
            if self.position[1] == "2": 
                self.racine.branches.append(
                    Noeud()
                    )
        
        if self.valeurPion == "T":
            pass
        
        if self.valeurPion == "C":
            pass
        
        if self.valeurPion == "F":
            pass
        
        if self.valeurPion == "Q":
            pass
        
        if self.valeurPion == "K":
            pass
        
        
    
    
    
    def searchCase(self):
        pass
        
        
        
        
        
        
        
        

p = Board()
p.mainloop()
#p.updateDisplay()

  
