        
class Patern:
    """ Classe regroupant les info et les methodes pour la gestion d'un groupe de cartes """
    #Attribut GAME
    _liste = []
    #Racine
    _root = None
    
    def __init__(self,patern,root):
        """ Initialisateur de la classe Patern """
        self._liste = patern
        self._root = root
        
    def add_card(self,index,card):
        """ Ajoute une carte spécifique (card = pointeur)a un endroit déterminé (index = int) """
        self._liste.insert(index,card) #On insert une carte à un emplacement de la main annoncé
        
    def remove_card(self,index):
        """ Retire une carte de la liste à partir d'un index donné """
        del self._liste[index] #On supprime une carte à un index donné
        
