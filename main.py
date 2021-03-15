# main.py - chess board project
import tkinter as tk
import random
from PIL import Image, ImageTk
import numpy as np
import pygame
import random
import datetime


# on prépare pygame pour jouer les sons :
# on crée un mixeur pygame et on l'initialise
pygame.mixer.init(44100, -16, 2, 512)
pygame.mixer.init()
# et on charge les sons
sound1 = pygame.mixer.Sound("sounds/move6.ogg")
sound2 = pygame.mixer.Sound("sounds/move7.ogg")

# TODO
# pour vérifier un échec : /!\ doit être lancé avant tous les mouvements pour vérifier
# qu'on se met pas en échec
# et si on est en échec à cause d'un coup adverse on doit vérifier que le coup permet de nous sortir de l'échec
# -> tu prends toutes les pièces
# -> tu demandes leurs arbres de déplacement
# -> tu regardes si dans toutes ces cases y'a la position du roi adverse
# -> si oui y'a échec
# pour l'échec et mat :
# on regarde TOUS les mouvements possibles de TOUTES les pièces
# on sauvegarde toutes ces possibilités dans un nouveau plateau
# et on fait le test d'échec sur chacun de ces plateaux
# si y'a aucun plateau qui n'est pas en échec alors c'est échec et mat.


class Board(tk.Tk):
    """
    Initialise une fenêtre Tkinter, et définit
    des attributs publics utilisés et potentiellement
    modifiés par d'autres programmes : 

    l'attribut 'tour' contient la lettre de la couleur du joueur qui doit jouer ('W' ou 'B'), 'W' par défaut
    l'attribut 'selectedCase' contient la case actuellement sélectionnée ou un None, utile pour connaître
    l'état de l'action du joueur.
    l'attribut 'plateau' est une matrice de dimension 2 contenant des objets Pion ou des None.
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

    les attributs 'coordLettre' et 'coordChiffre' contiennent une légende sous forme de liste permettant de calculer
    une coordonnée dans la matrice à partir d'une dénomination de case (par exemple 'D6') et inversement.
    Ces liste sont retournées en même temps que le plateau afin de changer le point de vue du joueur
    (coté noir ou coté blanc) en gardant une cohérence dans les cases.

    l'attribut 'coupsJouables' contient une liste de coups jouables par le joueur, indiquant les cases sur
    lesquelles dessiner un point bleu.

    l'attribut sprite est un dictionnaire associant une dénomination de pion (par exemple 'TW' pour 'Tour White')
    à une image Tkinter pouvant être utilisée dans le canvas.

    l'attribut 'canvas' contient un objet canvas, sur lequel est dessiné la fenêtre de jeu. Cet attribut est notemment
    modifié par la méthode 'updateDisplay'.
    """

    def __init__(self, *args, **kwargs):
        """
        TODO
        """

        # initialisation de la fenêtre de jeu
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("NSICHESS XTREME 2 DELUXE PREMIUM [CRACK]")

        self.tour = "W"  # les blancs commencent
        self.selectedCase = None

        self.plateau = [
            [Pion('T', 'B'), Pion('C', 'B'), Pion('F', 'B'), Pion('Q', 'B'), Pion(
                'R', 'B'), Pion('F', 'B'), Pion('C', 'B'), Pion('T', 'B')],
            [Pion('P', 'B') for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pion('P', 'W') for i in range(8)],
            [Pion('T', 'W'), Pion('C', 'W'), Pion('F', 'W'), Pion('Q', 'W'), Pion(
                'R', 'W'), Pion('F', 'W'), Pion('C', 'W'), Pion('T', 'W')]
        ]

        self.coordLettre = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.coordChiffre = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.coupsJouables = []

        self.sprites = {
            "TW": ImageTk.PhotoImage(Image.open("sprites/WT.png").convert("RGBA").resize((75, 75))),
            "CW": ImageTk.PhotoImage(Image.open("sprites/WKN.png").convert("RGBA").resize((75, 75))),
            "FW": ImageTk.PhotoImage(Image.open("sprites/WB.png").convert("RGBA").resize((75, 75))),
            "RW": ImageTk.PhotoImage(Image.open("sprites/WK.png").convert("RGBA").resize((75, 75))),
            "QW": ImageTk.PhotoImage(Image.open("sprites/WQ.png").convert("RGBA").resize((75, 75))),
            "PW": ImageTk.PhotoImage(Image.open("sprites/WP.png").convert("RGBA").resize((75, 75))),

            "TB": ImageTk.PhotoImage(Image.open("sprites/BT.png").convert("RGBA").resize((75, 75))),
            "CB": ImageTk.PhotoImage(Image.open("sprites/BKN.png").convert("RGBA").resize((75, 75))),
            "FB": ImageTk.PhotoImage(Image.open("sprites/BB.png").convert("RGBA").resize((75, 75))),
            "RB": ImageTk.PhotoImage(Image.open("sprites/BK.png").convert("RGBA").resize((75, 75))),
            "QB": ImageTk.PhotoImage(Image.open("sprites/BQ.png").convert("RGBA").resize((75, 75))),
            "PB": ImageTk.PhotoImage(Image.open("sprites/BP.png").convert("RGBA").resize((75, 75)))
        }

        self.canvas = tk.Canvas(bd=0, height=830, width=830, cursor='hand2')

        # on met à jour l'affichage lors de l'initialisation.
        self.updateDisplay()

    def toString(self):
        """
        retourne une représentation sous forme de string du plateau de jeu
        afin de l'envoyer à une autre instance du programme pour une partie multijoueur.
        """

        # on charge d'abord les deux listes d'indexs, lettre puis chiffre afin de communiquer
        # la rotation actuelle du plateau.
        # une pièce et sa position est sous la forme "a8TB" (lettreChiffreValeurCouleur)
        # TODO ajouter la variable "tour" afin de communiquer la personne qui est censé jouer au prochain tour.

        sE = ""
        for l in range(len(self.plateau)):
            for c in range(len(self.plateau[l])):
                if self.plateau[l][c] is not None:
                    sE += f"{self.coordLettre[c]}{self.coordChiffre[l]}{self.plateau[l][c].valeur}{self.plateau[l][c].couleur}"
        return sE

    def loadFromString(self, string):
        """
        prend en argument un string généré par la méthode 'toString' et
        modifie le plateau de jeu en conséquence et le retourne
        """
        piecesList = []

        for index, char in enumerate(string):
            if index % 4 == 0:  # nouvelle pièce tous les quatre caractères.
                piecesList.append("".join(string[index:index + 4]))
        # création d'un plateau vide
        nouveauPlateau = [
            [None for i in range(8)] for j in range(8)
        ]

        for i in piecesList:
            # on récupère les coordonées matricielles de la pièce grâce à la dénomination de la case
            lettreIndex = self.coordLettre.index(i[0])
            chiffreIndex = self.coordChiffre.index(i[1])
            # on récupère la valeur de la pièce grâce aux deux autres caractères
            pion = Pion(i[2], i[3])

            # on ajoute la pièce dans le nouveau plateau
            nouveauPlateau[chiffreIndex][lettreIndex] = pion

        # on met à jour le plateau et on actualise l'affichage.
        self.plateau = nouveauPlateau
        self.updateDisplay()
        return nouveauPlateau

    def retournePlateau(self):
        """
        retourne le plateau. Attention : cette fonction ne modifie pas juste l'affichage,
        elle retourne littéralement toutes les matrices. De cette façon, on peut conserver
        une très bonne logique quand aux dénominations des cases.
        """

        self.plateau = np.flip(self.plateau, (0, 1)).tolist()
        self.coordLettre = np.flip(self.coordLettre, 0).tolist()
        self.coordChiffre = np.flip(self.coordChiffre, 0).tolist()
        self.updateDisplay()
        print("flipped the board")

    def finPartie(self):
        pass

    def partie(self):
        pass

    def updateDisplay(self):
        """
        Cette fonction met à jour l'affichage de la fenêtre Tkinter.
        C'est ici que toute la partie graphique s'effectue
        """

        self.canvas.delete("all")  # on supprime l'affichage actuel

        color = "beige"  # on définit la première couleur de la case

        def toggle(color):
            """
            prend un string "beige" ou "brown" en entrée, et l'inverse,
            permettant de dessiner le plateau avec des cases de couleurs
            différentes.
            """
            return "beige" if color == "brown" else "brown"

        def playMoveSound():
            """
            joue un son aléatoire parmi les sons définis au début du programme
            """
            sounds = [sound1, sound2]
            return pygame.mixer.Sound.play(random.choice(sounds))

        def clickEvent(event):
            """
            cette fonction est appelée à chaque fois qu'un clic est effectué
            sur le canvas. Il gère la sélection des pièces durant les différentes
            actions possibles (sélection/déselection d'une pièce, mouvement possible ou impossible,
            clic ailleurs que sur une case, etc)
            """

            colonne = event.x // 100  # comme le canvas fait 800 pixels, on récupère les
            ligne = event.y // 100   # coordonnées matricielles de la case de cette façon

            if colonne < 8 and ligne < 8:  # si une case est sélectionnée

                # calcule la pièce sur laquelle on a cliqué, ou "Empty" si la case est vide.
                pionstr = f"{self.plateau[ligne][colonne].valeur}{self.plateau[ligne][colonne].couleur}" if self.plateau[ligne][colonne] is not None else "Empty"
                # affiche un string de débuggage pour le clic.
                print(
                    f"clicked at x={event.x} ; y={event.y} | case {self.coordLettre[colonne]}{self.coordChiffre[ligne]} | pion : {pionstr}")

                # si on sélectionne une pièce de notre couleur
                if self.plateau[ligne][colonne] is not None and self.plateau[ligne][colonne].couleur == self.tour and f"{self.coordLettre[colonne]}{self.coordChiffre[ligne]}".upper() != self.selectedCase:

                    playMoveSound()  # on joue un son

                    # on récupère l'arbre de déplacement de la pièce sélectionnée.
                    arbreDeplacement = ArbreDeplacement(
                        f'{self.coordLettre[colonne]}{self.coordChiffre[ligne]}'.upper(), f'{pionstr[0]}', self)

                    # debug : on affiche dans la console toutes les cases sur lesquelles la pièce peut se déplacer
                    print(arbreDeplacement.DeplacementPion())
                    # on stocke toutes ces cases dans l'attribut de classe 'coupsJouables'
                    self.coupsJouables = arbreDeplacement.DeplacementPion()
                    self.updateDisplay()  # on met à jour l'affichage
                    # on stocke la pièce selectionnée dans l'attribut de classe 'selectedCase'
                    self.selectedCase = f'{self.coordLettre[colonne]}{self.coordChiffre[ligne]}'.upper(
                    )

                # si on clique sur une case valide pour le déplacement:
                # en effet, si la liste self.coupsJouables n'est pas vide c'est qu'une pièce est sélectionnée.
                elif f"{self.coordLettre[colonne]}{self.coordChiffre[ligne]}".upper() in self.coupsJouables:

                    playMoveSound()  # on joue un son

                    # on copie la pièce qui se déplace à sa nouvelle position, prenant potentiellement la place d'une pièce mangée.
                    self.plateau[ligne][colonne] = self.plateau[self.coordChiffre.index(
                        self.selectedCase[1])][self.coordLettre.index(self.selectedCase[0].lower())]
                    # l'ancienne position de la pièce doit forcément être vide, on met donc une case vide à cette position.
                    self.plateau[self.coordChiffre.index(self.selectedCase[1])][self.coordLettre.index(
                        self.selectedCase[0].lower())] = None
                    print(
                        f"Moved {self.selectedCase} to {self.coordLettre[colonne].upper()}{self.coordChiffre[ligne]}")

                    # le tour est terminé, on réinitialise les attributs de sélection
                    self.coupsJouables = []
                    self.selectedCase = None
                    # on change le tour : c'est au joueur adverse de jouer.
                    self.tour = "B" if self.tour == "W" else "W"

                    # ici, dilemne : soit on retourne le plateau, permettant à la personne qui joue
                    # d'avoir toujours ses pions vers le bas, mais c'est assez désagréable à regarder
                    # et on ne s'y retrouve pas, soit on actualise simplement l'affichage
                    # (l'affichage est automatiquement mis à jour quand on retourne le plateau)
                    # nous avons choisi de simplement mettre à jour l'affichage : c'est plus confortable,
                    # surtout sur mobile.

                    # self.retournePlateau()
                    self.updateDisplay()

                else:  # si on clique sur n'importe quel autre endroit

                    # on réinitialise les attributs de sélection et on met à jour l'affichage.
                    self.coupsJouables = []
                    self.selectedCase = None
                    self.updateDisplay()

        # implémentation du canvas
        label = tk.Label(
            self, text="ici on peut mettre du texte hihi")  # debug
        label.grid(row=0, column=0)
        label = tk.Label(self, text="Texte sur le côté")  # debug
        label.grid(row=0, column=1)
        labelFrame = tk.LabelFrame(
            self, text="Debug Buttons", width="50")  # debug
        labelFrame.grid(row=1, column=1)
        button1 = tk.Button(labelFrame, text="Flip the board",
                            command=self.retournePlateau)  # debug
        button1.pack()
        button2 = tk.Button(labelFrame, text="Play sound",
                            command=lambda: playMoveSound())  # debug
        button2.pack()

        # on doit ensuite créer 64 carrés d'une couleur différente, sous forme
        # de polygones avec la méthode canvas.create_rectangle(x0,y0,x1,y1, fill=color, outline="black")
        for l, line in enumerate(self.plateau):
            for c, case in enumerate(line):
                # dessin du plateau
                self.canvas.create_rectangle(
                    c * 100, l * 100, c * 100 + 100, l * 100 + 100, fill=color, width=3, outline="black")
                # dessin des pièces

                sprPiece = f"{case.valeur}{case.couleur}" if case is not None else None
                if sprPiece is not None:
                    # on affiche les sprites correspondant aux pions
                    self.canvas.create_image(
                        (c * 100 + 50, l * 100 + 50), image=self.sprites[sprPiece])
                    self.canvas.image = self.sprites[sprPiece]

                # et on inverse les couleurs pour avoir des carreaux dont les couleurs alternent
                color = toggle(color)
            color = toggle(color)

        for position in self.coupsJouables:  # affichage d'un point bleu pour les points jouables
            lettre = position[0].lower()
            nombre = position[1].lower()

            x = self.coordLettre.index(lettre)
            y = self.coordChiffre.index(nombre)

            self.canvas.create_oval(x * 100 - 10 + 50, y * 100 - 10 + 50, x * 100 +
                                    10 + 50, y * 100 + 10 + 50, fill='blue', stipple='gray50', outline=None)

        # affichage des légendes sur les côtés du plateau.
        for i, coords in enumerate(self.coordLettre):
            self.canvas.create_text(
                i * 100 + 9, 812, text=coords, font="Times 15 italic bold")
        for i, coords in enumerate(self.coordChiffre):
            self.canvas.create_text(
                812, i * 100 + 10, text=coords, font="Times 15 italic bold")

        # on associe le canvas à la fonction clickEvent quand on clique dessus en le traitant comme un bouton.
        self.canvas.bind("<Button-1>", clickEvent)
        # on attache le canvas à la fenêtre
        self.canvas.grid(row=1, column=0)

        # frame de débug
        labelFrame = tk.LabelFrame(self, text="Board string representation")
        labelFrame.grid(row=2, column=0)
        # affiche la représentation string du plateau actuel
        label = tk.Label(labelFrame, text=self.toString(),
                         width=50, wraplength=500, padx=50, pady=10)
        label.pack()
        # affiche la dernière actualisation du plateau
        label = tk.Label(
            labelFrame, text=f"updated at {datetime.datetime.now()}")
        label.pack()
        # affiche la couleur du joueur dont c'est le tour
        label = tk.Label(
            labelFrame, text=f"{'White' if self.tour == 'W' else 'Black'} have to play.")
        label.pack()

    def __repr__(self):
        """
        Cette fonction est utilisée UNIQUEMENT si tkinter n'est pas attaché.
        En effet, comme l'objet Board est un sous-objet d'une fenêtre Tkinter,
        il est impossible de le print.
        """

        stringBoard = ""
        for ligne in self.plateau:
            for case in ligne:
                stringBoard += " " if case is None else case.valeur
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


class Noeud():
    """
    Utiliser par l'objet ArbreDeplacement afin de creer son arbre

        Initialise un objet Noeud, qui permet de creer un arbre, avec 1 ou plusieurs enfants.
            -positionPion : recuperer la position sur le plateau du pion choisit
            -branches : definir ses enfants sous forme de liste de liste (vide au depart et rempli par les differentes methodes)

    """

    def __init__(self, positionDuPion):

        self.positionPion = positionDuPion
        self.branches = []

    def nord(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers le haut du plateau en fonction de la position de notre pion.
        """
        if int(self.positionPion[1]) < 8:
            self.branches.append(
                Noeud(self.positionPion[0] +
                      str(int(self.positionPion[1]) + 1))
            )
            self.branches[-1].nord()

    def sud(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers le bas du plateau en fonction de la position de notre pion.
        """
        if int(self.positionPion[1]) > 1:
            self.branches.append(
                Noeud(self.positionPion[0] +
                      str(int(self.positionPion[1]) - 1))
            )
            self.branches[-1].sud()

    def est(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers la doite du plateau en fonction de la position de notre pion.
        """
        if ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(
                    chr(ord(self.positionPion[0].lower()) + 1).upper() + self.positionPion[1])
            )
            self.branches[-1].est()

    def ouest(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers la gauche du plateau en fonction de la position de notre pion.
        """
        if ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(
                    chr(ord(self.positionPion[0].lower()) - 1).upper() + self.positionPion[1])
            )
            self.branches[-1].ouest()

    def nord_est(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers la diagonale haut-droite du plateau en fonction de la position de notre pion.
        """
        if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) + 1).upper() + str(int(self.positionPion[1]) + 1))
            )
            self.branches[-1].nord_est()

    def nord_ouest(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers la diagonale haut-gauche du plateau en fonction de la position de notre pion.
        """
        if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) - 1).upper() + str(int(self.positionPion[1]) + 1))
            )
            self.branches[-1].nord_ouest()

    def sud_est(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers la diagonale bas-droite du plateau en fonction de la position de notre pion.
        """
        if int(self.positionPion[1]) > 1 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) + 1).upper() + str(int(self.positionPion[1]) - 1))
            )
            self.branches[-1].sud_est()

    def sud_ouest(self):
        """
        Ajoute dans l'attribut branches, toute les position possible dans un plateau vide.

            Celle ci sert a creer des fils vers la diagonale bas-gauche du plateau en fonction de la position de notre pion.
        """

        if int(self.positionPion[1]) > 1 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) - 1).upper() + str(int(self.positionPion[1]) - 1))
            )
            self.branches[-1].sud_ouest()

    def roi(self):
        """
        Cette fonction sert a creer les deplacement d'un roi dans toute les directions possibles.

            Clairement different des autres fonctions nord(), sud()..., du au fait que le roi peut se deplacer d'une seul case autour de lui
        """
        # nord
        if int(self.positionPion[1]) < 8:
            self.branches.append(
                Noeud(self.positionPion[0] +
                      str(int(self.positionPion[1]) + 1))
            )
        # sud
        if int(self.positionPion[1]) > 1:
            self.branches.append(
                Noeud(self.positionPion[0] +
                      str(int(self.positionPion[1]) - 1))
            )
        # est
        if ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(
                    chr(ord(self.positionPion[0].lower()) + 1).upper() + self.positionPion[1])
            )
        # ouest
        if ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(
                    chr(ord(self.positionPion[0].lower()) - 1).upper() + self.positionPion[1])
            )
        # nord-est
        if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) + 1).upper() + str(int(self.positionPion[1]) + 1))
            )
        # nord-ouest
        if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) - 1).upper() + str(int(self.positionPion[1]) + 1))
            )
        # sud-est
        if int(self.positionPion[1]) > 1 and ord(self.positionPion[0].lower()) < 104:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) + 1).upper() + str(int(self.positionPion[1]) - 1))
            )
        # sud-ouest
        if int(self.positionPion[1]) > 1 and ord(self.positionPion[0].lower()) > 97:
            self.branches.append(
                Noeud(chr(ord(self.positionPion[0].lower(
                )) - 1).upper() + str(int(self.positionPion[1]) - 1))
            )

    def pion(self, couleur, deuxCase=False):
        """
        De meme que le roi, cette fonction creer le deplacement d'un pion.
            - La fonction prend en compte si le pion peut avancer de 2 case si il est dans la position initiale.

            - La fonction demande la couleur du pion, où la couleur est soit blanc ( type = int) remplace par un 1 ou 0 pour une couleur noir avec l'attribut: couleur (type = int)

            - La fonction demande egalement si le pion peut avancer de 2 cases avec l'attribut: deuxCase (type = bool, de base False)
        """
        if couleur == 1:

            if deuxCase:
                # nord
                if int(self.positionPion[1]) < 8:
                    self.branches.append(
                        Noeud(self.positionPion[0] +
                              str(int(self.positionPion[1]) + 1))
                    )
                    self.branches.append(
                        Noeud(self.positionPion[0] +
                              str(int(self.positionPion[1]) + 2))
                    )
            else:
                # nord
                if int(self.positionPion[1]) < 8:
                    self.branches.append(
                        Noeud(self.positionPion[0] +
                              str(int(self.positionPion[1]) + 1))
                    )
            # nord-est
            if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) < 104:
                self.branches.append(
                    Noeud(chr(ord(self.positionPion[0].lower(
                    )) + 1).upper() + str(int(self.positionPion[1]) + 1))
                )
            # nord-ouest
            if int(self.positionPion[1]) < 8 and ord(self.positionPion[0].lower()) > 97:
                self.branches.append(
                    Noeud(chr(ord(self.positionPion[0].lower(
                    )) - 1).upper() + str(int(self.positionPion[1]) + 1))
                )

        else:

            if deuxCase:
                # sud
                if int(self.positionPion[1]) > 0:
                    self.branches.append(
                        Noeud(self.positionPion[0] +
                              str(int(self.positionPion[1]) - 1))
                    )
                    self.branches.append(
                        Noeud(self.positionPion[0] +
                              str(int(self.positionPion[1]) - 2))
                    )
            else:
                # sud
                if int(self.positionPion[1]) > 0:
                    self.branches.append(
                        Noeud(self.positionPion[0] +
                              str(int(self.positionPion[1]) - 1))
                    )
            # sud-est
            if int(self.positionPion[1]) > 0 and ord(self.positionPion[0].lower()) < 104:
                self.branches.append(
                    Noeud(chr(ord(self.positionPion[0].lower(
                    )) + 1).upper() + str(int(self.positionPion[1]) - 1))
                )
            # sud-ouest
            if int(self.positionPion[1]) > 0 and ord(self.positionPion[0].lower()) > 97:
                self.branches.append(
                    Noeud(chr(ord(self.positionPion[0].lower(
                    )) - 1).upper() + str(int(self.positionPion[1]) - 1))
                )

    def cavalier(self):
        """
        Creer tout les deplacements d'un cavalier dans un plateau vide selon la position du pion
        """
        positionInitialeX = int(self.positionPion[1])
        positionInitialeY = ord(self.positionPion[0].lower())
        # haut haut droite et bas bas droite
        if positionInitialeY + 1 <= 104:
            if positionInitialeX + 2 < 8:
                self.branches.append(
                    Noeud(chr(positionInitialeY + 1).upper() +
                          str(positionInitialeX + 2))
                )
            if positionInitialeX - 2 > 0:
                self.branches.append(
                    Noeud(chr(positionInitialeY + 1).upper() +
                          str(positionInitialeX - 2))
                )
        # haut haut gauche et bas bas gauche
        if positionInitialeY - 1 >= 97:
            if positionInitialeX + 2 < 8:
                self.branches.append(
                    Noeud(chr(positionInitialeY - 1).upper() +
                          str(positionInitialeX + 2))
                )
            if positionInitialeX - 2 > 0:
                self.branches.append(
                    Noeud(chr(positionInitialeY - 1).upper() +
                          str(positionInitialeX - 2))
                )
        # haut droite droite et bas droite droite
        if positionInitialeX + 1 < 8:
            if positionInitialeY + 2 <= 104:
                self.branches.append(
                    Noeud(chr(positionInitialeY + 2).upper() +
                          str(positionInitialeX + 1))
                )
            if positionInitialeY - 2 >= 97:
                self.branches.append(
                    Noeud(chr(positionInitialeY - 2).upper() +
                          str(positionInitialeX + 1))
                )

        # haut gauche gauche et bas gauche gauche
        if positionInitialeX - 1 > 0:
            if positionInitialeY + 2 <= 104:
                self.branches.append(
                    Noeud(chr(positionInitialeY + 2).upper() +
                          str(positionInitialeX - 1))
                )
            if positionInitialeY - 2 >= 97:
                self.branches.append(
                    Noeud(chr(positionInitialeY - 2).upper() +
                          str(positionInitialeX - 1))
                )


class ArbreDeplacement():
    """
    la classe arbre creer un arbre de deplacement d'un pion, sans verifiquation au niveau du plateau
    pour obtenir l'arbre sous forme de liste:

        ->creer l'arbre : ArbreDeplacement('case', 'valeur pion', 'plateau')
            -->case : position du pion demander
                    valeurPion : de quel type est le pion
                        -Roi
                        -Reine
                        -Cavalier
                        -Fou
                        -Tour
                        -Pion
            -->plateau :  plateau actuel sous forme de liste

        ->demander via le pion dans le plateau,  => pion.DeplacementPion()

    =>Les attributs:

        -racine : creer un objet Noeud avec la position du pion

        -positionPion : prend la position du pion sur le plateau

        -valeurPion : prend la valeur du pion (Roi, Reine, ...)

        -plateau : prend la liste definisant le plateau (soit l'attribut plateau de la classe Board)

        -coordLettre : prend de l'objet Board, l'attribut coordLettre pour definir les coordonnées selon le sens du plateau

        -coordchiffre : prend de l'objet Board, l'attribut coordChiffre pour definir les coordonnées selon le sens du plateau


    """

    def __init__(self, positionPion, valeurPion, board=None):
        self.racine = Noeud(positionPion)
        self.position = positionPion
        self.valeurPion = valeurPion
        self.plateau = board.plateau
        self.coordLettre = board.coordLettre
        self.coordChiffre = board.coordChiffre

        # lance la methode constructionArbre() pour creer la liste des coups possibles
        self.constructionArbre()

    def constructionArbre(self):
        """
        Cette fonction permet de creer selon le type de pion ( Roi, Reine, ...) toute la liste des coups possibles
        """

        if self.valeurPion == "P":
            xPion = self.coordLettre.index(self.position[0].lower())
            yPion = self.coordChiffre.index(self.position[1])
            PionBase = self.plateau[yPion][xPion]
            if PionBase.couleur == 'W':

                if self.position[1] == "2":
                    self.racine.pion(1, True)
                else:
                    self.racine.pion(1)
            else:

                if self.position[1] == "7":
                    self.racine.pion(0, True)
                else:
                    self.racine.pion(0)

        if self.valeurPion == "T":

            self.racine.nord()
            self.racine.sud()
            self.racine.est()
            self.racine.ouest()

        if self.valeurPion == "C":

            self.racine.cavalier()

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
        Renvoi la liste de toute les case possible du pion
        Utilise parcours() pour les pion simples
        Utilise testPion
        """
        def parcours(noeud, lst, PionBase):
            """
            Permet de retourner les deplacements sous forme de liste simple des pions :
                -Roi

                -Reine

                -Fou

                -Cavalier

                -Tour
            """

            case = noeud.positionPion.lower()
            xPlateau = self.coordLettre.index(case[0])
            yPlateau = self.coordChiffre.index(case[1])

            coord = self.plateau[yPlateau][xPlateau]

            # for i in range(len(noeud.branches)):

            if coord is None:
                lst.append(noeud.positionPion)
                for fils in noeud.branches:
                    parcours(fils, lst, PionBase)

            elif coord is not None:
                if coord.couleur != PionBase.couleur:
                    # si la couleur du pion sur le plateau est differente de notre pion
                    lst.append(noeud.positionPion)

        def parcoursPion(lst, couleur, PionBase, plateau):
            """
            Permet, si le pion est un pion, de retourner sa propre liste
            """
            liste = []

            if couleur == 1:
                for i in range(len(lst)):
                    if i == 0:
                        if plateau[self.coordChiffre.index(lst[0][1])][self.coordLettre.index(lst[0][0].lower())] is None:
                            liste.append(lst[0])
                            if lst[0][1] == '3':
                                if plateau[self.coordChiffre.index(lst[1][1])][self.coordLettre.index(lst[1][0].lower())] is None:
                                    liste.append(lst[1])
                    else:
                        if lst[i] not in liste:

                            if plateau[self.coordChiffre.index(lst[i][1])][self.coordLettre.index(lst[i][0].lower())] is not None:
                                if plateau[self.coordChiffre.index(lst[i][1])][self.coordLettre.index(lst[i][0].lower())].couleur != PionBase.couleur:
                                    liste.append(lst[i])
                if len(liste) > 1:
                    if liste[0][0] == liste[1][0]:
                        if int(liste[0][1]) == int(liste[1][1]) - 1:
                            if plateau[self.coordChiffre.index(lst[1][1])][self.coordLettre.index(lst[1][0].lower())] is not None:
                                liste.pop(1)
                return liste

            else:

                for i in range(len(lst)):
                    if i == 0:
                        if plateau[self.coordChiffre.index(lst[0][1])][self.coordLettre.index(lst[0][0].lower())] is None:
                            liste.append(lst[0])
                            if lst[0][1] == '6':
                                if plateau[self.coordChiffre.index(lst[1][1])][self.coordLettre.index(lst[1][0].lower())] is None:
                                    liste.append(lst[1])
                    else:
                        if lst[i] not in liste:

                            if plateau[self.coordChiffre.index(lst[i][1])][self.coordLettre.index(lst[i][0].lower())] is not None:
                                if plateau[self.coordChiffre.index(lst[i][1])][self.coordLettre.index(lst[i][0].lower())].couleur != PionBase.couleur:
                                    liste.append(lst[i])

                if len(liste) > 1:
                    if liste[0][0] == liste[1][0]:

                        if int(liste[0][1]) == int(liste[1][1]) + 1:
                            if plateau[self.coordChiffre.index(lst[1][1])][self.coordLettre.index(lst[1][0].lower())] is not None:
                                liste.pop(1)
                return liste

        xPion = self.coordLettre.index(self.position[0].lower())
        yPion = self.coordChiffre.index(self.position[1])
        PionBase = self.plateau[yPion][xPion]
        lst = []

        for fils in self.racine.branches:
            parcours(fils, lst, PionBase)

        if self.valeurPion == "P":
            if PionBase.couleur == "W":
                lst = parcoursPion(lst, 1, PionBase, self.plateau)
            else:
                lst = parcoursPion(lst, 0, PionBase, self.plateau)

        return lst


p = Board()

arbrePiece = Noeud("d1")
print('--------------')

p.mainloop()
# p.updateDisplay()
