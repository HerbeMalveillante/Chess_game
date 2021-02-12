# main.py - chess board project
import tkinter as tk
import random
from PIL import Image, ImageTk
import numpy as np




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
			[Pion('T','B'), Pion('C','B'), Pion('F','B'), Pion('Q','B'), Pion('R', 'B'), Pion('F','B'), Pion('C','B'), Pion('T','B')],
			[Pion('P','B') for i in range(8)],
			[None for i in range(8)],
			[None for i in range(8)],
			[None for i in range(8)],
			[None for i in range(8)],
			[Pion('P','W') for i in range(8)],
			[Pion('T','W'), Pion('C','W'), Pion('F','W'), Pion('Q','W'), Pion('R', 'W'), Pion('F','W'), Pion('C','W'), Pion('T','W')]
			
			]
			
		self.coordLettre = ['a','b','c','d','e','f','g','h']
		self.coordChiffre =["8","7","6","5","4","3","2","1"]
		
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
						
		self.canvas = tk.Canvas(bd=0, height=830, width=830)
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
		self.plateau = np.flip(self.plateau, (0,1))
		self.coordLettre = np.flip(self.coordLettre, 0)
		self.coordChiffre = np.flip(self.coordChiffre, 0)
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
			
		def clickEvent(event):
			
			colonne = event.x//100
			ligne = event.y//100
			
			if colonne < 8 and ligne < 8 :
			
				pionstr = f"{self.plateau[ligne][colonne].valeur}{self.plateau[ligne][colonne].couleur}" if self.plateau[ligne][colonne] is not None else "Empty"
			  
				
				print(f"clicked at x={event.x} ; y={event.y} | case {self.coordLettre[colonne]}{self.coordChiffre[ligne]} | pion : {pionstr}")
				
			
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
		labelFrame = tk.LabelFrame(self,text="Actions", width="50")
		labelFrame.grid(row=1, column=1)
		button1 = tk.Button(labelFrame, text="Flip the board", command = self.retournePlateau)
		button1.pack()
		button2 = tk.Button(labelFrame, text="button2")
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
			
		for i, coords in enumerate(self.coordLettre):
			self.canvas.create_text(i*100+9, 812 , text=coords,font="Times 15 italic bold")
		for i, coords in enumerate(self.coordChiffre):
			self.canvas.create_text(812,i*100+10, text=coords, font="Times 15 italic bold")
		
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
            
            
            
    def nord(self,continuite=None):
        if int(self.positionPion[1]) <8:
            self.branches.append(
                Noeud(self.positionPion[0]+str(int(self.positionPion[1])+1))
                )
            self.branches[-1].nord()
        
    def sud(self, continuite=None):
        if int(self.positionPion[1]) > 0:
            self.branches.append(
                Noeud(self.positionPion[0]+str(int(self.positionPion[1])-1))
                )
            self.branches[-1].sud(continuite)
    
    
    def est(self, continuite=None):
        if ord(self.positionPion[0].lower()) < 104 :
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())+1).upper()+self.positionPion[1])
                                 )
            self.branches[-1].est(continuite)
    
    def ouest(self, continuite=None):
        if ord(self.positionPion[0].lower()) > 97:
            self.branches.append( 
                Noeud(chr(ord(self.positionPion[0].lower())-1).upper()+self.positionPion[1])
                )
            self.branches[-1].ouest(continuite)
            
    
    
    
    def nord_est(self, continuite=None):
        if int(self.positionPion[1]) <8 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())+1).upper()+str(int(self.positionPion[1])+1))
                )
            self.branches[-1].nord_est(continuite)
        
        
    def nord_ouest(self, continuite=None):
        if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())-1).upper()+str(int(self.positionPion[1])+1))
                )
            self.branches[-1].nord_ouest(continuite)
    
    def sud_est(self, continuite=None):
        if int(self.positionPion[1]) >0 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())+1).upper() + str(int(self.positionPion[1])-1))
                      )
            self.branches[-1].sud_est(continuite)
    
    def sud_ouest(self, continuite=None):
        if int(self.positionPion[1]) >0 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower())-1).upper()+str(int(self.positionPion[1])-1))
                )     
            self.branches[-1].sud_ouest(continuite)
    
    
    
            
    

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
            
        
        if self.valeurPion == "K":
            pass
        
#        def dot(self):
#            """
#            Renvoie un str contenant tous les noeuds et toutes les arètes de l'arbre.
#            Ce str est interprétable par la fonction graphviz.from_string du module graphviz
#            pour la visualisation graphique de l'arbre directement dans le notebook :
#            Par exemple pour un arbre a :
#            graphviz.from_string(a.dot())
#            """
#            def representation(noeud):
#                # construit une liste de string, noeud par noeud, récursivement
#                if noeud is not None:
#                    #ajoute le noeud
#                    txt = (str(id(noeud)) + "[label = " +  str(noeud.positionPion) + "]\n")
#                    # Appel récursif de la fonction representation
#                    
#                    for caseSuivante in noeud.branches:
#                        txt += representation(caseSuivante)
#                        #ajoute l'arete correspondantes au noeud droit
#                        txt += (str(id(noeud)) + " -> " + str(id(caseSuivante)) + '\n')
#                    return txt
#
#            return "digraph g {\n" + representation(self.racine) + '}'
        
    
    
    
    def searchCase(self):
        pass
        
        
        
        
        
        
        
        

p = Board()
p.mainloop()
#p.updateDisplay()

  
