import Patern

class Deck(Patern.Patern):
    """ Classe regroupant les info et les methodes pour la gestion d'un deck """

    def shuffle(self):
        """ Melange le deck """
        for i in range(len(self._liste)):#On repete l'operation pour chaque carte du deck (mais pas dans l'ordre des cartes du deck) :
            #On prend 2 nb random
            rand1 = randint(0,len(self._liste)-1)
            rand2 = randint(0,len(self._liste)-1)
            #On prend 2 cartes de la liste aux index des 2 nb
            a = self._liste[rand1]
            b = self._liste[rand2]
            #On inverse leurs position
            self._liste[rand2] = a
            self._liste[rand1] = b
            #=> Melange classique mais pas parfait
            
