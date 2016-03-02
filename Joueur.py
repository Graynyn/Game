import Deck
import Main
import tkinter as tk


class Joueur:
    """ Classe regroupant toutes les informations et les fonctions nécessaires au jeu pour chaque joueur"""
    #Attributs GAME
    _nom = ""
    _index = None
    _deck = None
    _main = None
    _roi = None
    _tour = None
    _mana_max = None
    _mana = None
    _mvt_creature_possible = None
    _mvt_roi_possible = None
    _zones_deploiement = None
    #Attributs Graphics
    __can_mana = None
    __label_mana = None
    #Racine
    _root = None
    def __init__(self,index,nom,deck,main,zones_deploiement,root):
        """ Initialisateur de la classe Joueur """
        #Racine
        self._root = root
        #Attributs Game
        self._index = index
        self._deck = Deck.Deck(deck,self)
        self._main = Main.Main(main,self)
        self._nom = nom
        self._mana_max = 0
        self._mana = self._mana_max
        #Attributs Graphics
        self.__can_mana = tk.Canvas(self._root._fen,bg='red')
        place = (self._index - 1)*2
        self.__can_mana.grid(column=place,row=0)
        self.__label_mana = tk.Label(self.__can_mana)
        self.__label_mana.grid(column=self._index,row=0)
        self._zones_deploiement = zones_deploiement
    
    def pioche(self):
        """ Fonction permettant au joueur de prendre une carte de son deck et de l'ajouter a sa main """
        if len(self._deck._liste) != 0:
            if len(self._main._liste) >= 6: #Max de cartes dans la main
                #Il faudra mettre un message ou une animation
                print("main_pleine")
            else:
                print("pioche")
                carte_pioche = self._deck._liste[len(self._deck._liste)-1] #On prend la derniere carte du deck
                self._deck.remove_card(-1) #Vidage de l'emlacement du deck où on a pris la carte
                self._main.add_card(len(self._main._liste),carte_pioche) #Ajout de la carte dans la main 
            self._main.refresh() #Refresh graphique
        else:
            print("plus de cartes dans le deck") #Animation ou message dans une boite de dialogue
            
    def focus_roi(self,roi):
        """Change le focus sur fu roi du joueur """
        if self._roi != None: #Si il n'y a pas encore de roi pour ce joueur on peut se passer de cette phase (optimisation)
            self._roi._roi = False #On met a jour l'indicateur dans l'objet carte de l'ancienne carte roi
        self._roi = roi
        self._roi._roi = True #On met a jour l'attribut GAME de la carte de roi
        
    def get_mana(self):
        """ Met a jour la mana max en fonction de l'emplacement du roi sur le terrain """
        self._mana_max = self._root._terrain._tabl_points[self._roi._x][self._roi._y] #On met la mana du joueur à la valeur du tableau de points de mana du terrain sur la case sur laquelle se trouve le roi de ce joueur
        
    def reset_mana(self):
        """ rend tous les pts de mana """
        self._mana = self._mana_max #On remet la mana à la mana max
        
    def begin_tour(self):
        """ On commence le tour """
        self.pioche() #On pioche
        self._tour = True #On met a jour la variable de tour (c'est le tour de ce joueur maintenant)
        self._root._terrain.reset_action() #On permet aux cartes de ce joueur de bouger/attaquer
        self._mvt_creature_possible = True
        self._mvt_roi_possible = True
        self.get_mana() #Met à jour le mana max
        self.reset_mana() #Remet la mana a son max
        self.refresh_can_mana() #On met a jour les labels de mana
        self.__label_mana.configure(bg="green") #On met le label de mana en vert pour montrer que c'est le tour de ce joueur
        self._root._terrain.display() #On met à jour le terrain (graphique)

    def end_tour(self):
        """ fini le tour """
        self._tour = False
        self._main.reverse() #On retourne les cartes de la main (il ne s'ajirait pas de tricher en regardant les cartes de la main adverse tout de meme !
        self.__label_mana.configure(bg="grey") #On met le label mana en gris pour montrer que ce n'est plus le tour de ce joueur
