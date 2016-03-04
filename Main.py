import Patern
import tkinter as tk

class Main(Patern.Patern):
    """ Classe regroupant les info et les methodes nécessaires pour la gestion d'une main """
    #Attribut GAME
    _taille = 7
    #Attribut Graphics
    __labels = []
    __can = None
    __can_width = 20
    __can_height = 100

    def __init__(self,patern,root):
        """ l'argument patern est une liste de cartes """
        #Attributs GAME
        self._liste = patern
        #Racine
        self._root = root
        #Attributs Graphics
        self.__can = tk.Canvas(self._root._root._fen,bg='red')
        place = 2-(self._root._index - 1)*2 #Emplacement dans la grille du .grid du canvas
        self.__can.grid(column=1,row=place)
    def display(self): #Pour gregoire
        pass
    def refresh(self): #Pour gregoire
        pass
    def reverse(self): #Pour gregoire
        pass
      
