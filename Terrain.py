class Terrain:
    """ Classe regroupant les informations relatives au Terrain de jeu """
    #Attributs GAME
    _tabl_cards = None
    _tabl_points = None
    _taille = None
    #Attributs Graphics
    _labels = None
    _can = None
    _can_width = 60
    _can_height = 60
    #Racine
    _root = None

    def __init__(self,width,height,tabl_points,root):
        """ initialisateur de la classe terrain"""
        #Attributs GAME
        self._taille = width
        self._tabl_cards = []
        for j in range(width):
            self._tabl_cards.append([])
            for i in range(height):
                self._tabl_cards[j].append(None)
        self._tabl_points = tabl_points
        #Racine
        self._root = root
        #Attributs Graphics
        self._can = Canvas(self._root._fen)
        self._can.grid(column=1,row=1)
        
    def add_card(self,x,y,card):
        """ Ajoute une carte aux coordonnées du tableau de cartes """
        self._tabl_cards[x][y] = card #On ajoute une carte a des coordonées /!\ ca ecrasera une autre carte aux meme coordonées s'il y en a deja une à cet emplacement
        # On met a jour les coords en attr des cartes
        card._x = x
        card._y = y
                
    def reset_action(self):
        """ On permet aux cartes d'attaquer et à se déplacer """
        #On parcours tout le terrain (x et y)
        for j in range(len(self._tabl_cards)):
            for i in range(len(self._tabl_cards[j])):
                if self._tabl_cards[j][i] != None: #Si il y une carte à cet emplacement :
                    if self._tabl_cards[j][i]._proprietaire == self._root._joueur_tour: #Si la carte est au joueur concerné, on lui permet de se deplacer
                        self._tabl_cards[j][i]._peut_attaquer = True
                        self._tabl_cards[j][i]._peut_deplacer = True
