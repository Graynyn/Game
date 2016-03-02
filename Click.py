class Click:
    """ Classe gérant les entrées d'informations nottament par la souris """
    """ _creature est est une liste de 2 valeures : les 2 dernieres valeures du click """
    """ _creature_ref est l'origine du click : terrain ("T"), main ("M") """
    #Attributs GAME
    _creature = []
    _creature_ref = None
    _zoom = False
    #Attributs Graphics
    __zoom_can = None
    __zoom_label = None
    __zoom_label_width = 10
    __zoom_label_height = 10
    #Racine
    _root = None
    
    def __init__(self,root):
        """ Initialisateur de la classe Click """
        pass
        self._root = root
        self._creature = [None,None]
        self._creature_ref = "T"
        self.__zoom_can = Canvas(self._root._fen,width=self.__zoom_label_width,height=self.__zoom_label_height)
        self.__zoom_can.grid(column=3,row=1)
        self.__zoom_label = Label(self.__zoom_can)
