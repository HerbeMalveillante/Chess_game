# main.py - chess board project
import tkinter as tk
import random







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
        #self.plateau = [[None for i in range(8)] for i in range(8)]
        
        self.plateau = [
            [Pion('T','W'), Pion('C','W'), Pion('F','W'), Pion('Q','W'), Pion('R', 'W'), Pion('F','W'), Pion('C','W'), Pion('T','W')],
            [Pion('P','W') for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pion('P','B') for i in range(8)],
            [Pion('T','B'), Pion('C','B'), Pion('F','B'), Pion('Q','B'), Pion('R', 'B'), Pion('F','B'), Pion('C','B'), Pion('T','B')]
            ]
            
        self.coord = ['a','b','c','d','e','f','g','h']
        
        self.updateDisplay()
    
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
            
        #implémentation sous forme de boutons :
        for l,line in enumerate(self.plateau) : 
            for c,case in enumerate(line) :
                textButton = case.valeur if case is not None else " "
                button=tk.Button(text=textButton, width = "2", height = "2", bg=color) 
                button.grid(row = l, column = c)
                color = toggle(color)
            color = toggle(color)
        
        #implémentation sous forme de canvas
        canvas = tk.Canvas(bd=2, height=8, width=8)
                
        
        
        
    
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
        

p = Board()
p.mainloop()
#p.updateDisplay()

  
