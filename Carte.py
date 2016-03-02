class Carte:
    #Attributs
    _nom = "" #0
    _mana = None #1
    _attaque = None #2
    _vie = None #3
    _patern_atk = None #4
    _patern_depl = None #5
    _effet = Effet #6
    _jeton = None#Sprite du jeton #6
    _sprite = None#Sprite de la carte #7
    _dos = None#Sprite du dos de la carte #8
    _proprietaire = None #Ref a un joueur
    _root = None
    _peut_attaquer = None
    _peut_deplacer = None
    _x = None
    _y = None
    _roi = None
    _face = None #Face recto => True // Face verso => False
    _effect_evt = None
    _effect_name = None

    def __init__(self,root,nom,mana,attaque,vie,patern_atk,patern_depl,jeton,sprite,sprite_dos,proprietaire):
        """ Initialisateur de la classe carte """
        self._root = root
        self._nom = nom #0
        self._mana = mana #1
        self._attaque = attaque #2
        self._vie = vie #3
        self._patern_atk = patern_atk #4
        self._patern_depl = patern_depl #5
        self._jeton = "Outils_pour_le_jeu/"+jeton # On oublie pas que c'est un chemin relatif (pas a partir de la racine mais du premier dossier ancetre commun (comme en svt))
        self._sprite = "Outils_pour_le_jeu/"+sprite
        self._dos = "Outils_pour_le_jeu/"+sprite_dos
        self._proprietaire = proprietaire
        self._peut_attaquer = False
        self._peut_deplacer = False
        self._roi = False
        self.face = True 
