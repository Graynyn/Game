#J'ai pas pu le tester car ya pas python sur les ordi du cdi donc c'est pas sur que ca fonctionne n'oubliez pas de regarder le readme que j'ai mis dans la branch 1.0 sinon yaura forcement des erreures
import tkinter as tk
import Terrain
import Click
import Carte
import Main
import Deck
import Joueur
import sqlite3 as sq
import Methodes_utiles as mu

class Game:
    """Classe gérant toutes les actions qui ne se rapportent pas directement aux joueurs (messages,etc...)"""
    #Attributs GAME
    _terrain = None #Objet Tableau
    _joueurs = None #Objet Joueur
    _joueur_tour = None #Int tour du joueur en cours 1 : j1 // 2: j2
    _click = None #Objet Click
    _cards = None #DATABASE des cartes
    _roi_joueur = None #Objet Carte
    _roi_adverse = None
    _decks_names = None
    _decks_cards = None
    #Attributs Graphics
    _fen = None
    _bouton_fin_tour = None

    def __init__(self):
        """ Initialisateur de la classe Game """
        self.create_card_database() #Charge la db des cartes
        self.create_deck_database() #Charge la db des cartes
        self._bouton_fin_tour = tk.Button(self._fen,text="Fin du tour",command=self.switch_turn) #Crée le bouton fin de tour
        self._bouton_fin_tour.grid(column=1,row=3) #Le grid (pack)
        
    def start(self):
        """ Methode qui va etre appelée pour lancer une Game """
        #Creation du terrain
        taille_terrain = 8 #La taille du terrain (modulable)
        self._terrain = Terrain.Terrain(taille_terrain,taille_terrain,self.create_terrain_points(taille_terrain),self) #Creation de l'objet terrain
        #Creation es objets
        self._click = Click.Click(self) #Creation de l'objet click
        self._joueurs = [[],[],[]] #Initialisation des joueurs
        #Creation des decks
        self._decks = self.create_deck_database() #
        deck1 = self._decks_cards[0] #Crée le premier deck à partir de la db (celui d'index 0)
        deck2 = self._decks_cards[0] #Crée le second deck a partir de la db (celui d'index 0)
        #Attention ces decks sont chargés des index des cartes (1,2,3,4,5,...) et non des objets cartes
        d1 = []
        d2 = []
        for i in range(30): # Creation des objets cartes en fonction des index des cartes de chaque deck
            d1.append(self.create_card(deck1[i],1))
            d2.append(self.create_card(deck2[i],2))
        #Creation des zones de deploiement
        zones_deploiement1 = []
        zones_deploiement2 = []
        for i in range(taille_terrain):
            zones_deploiement2.append([i,0]) #Pour le joueur 2 : les lignes d'index 0 et 1
            zones_deploiement2.append([i,1])
            zones_deploiement1.append([i,taille_terrain-2]) #Pour le joueur 1 : les lignes d'index 6 et 7 (pour un terrain de taille 8)
            zones_deploiement1.append([i,taille_terrain-1])
        #Creation des joueurs
        self._joueurs[1] = Joueur.Joueur(1,"Joueur1",d1,[],zones_deploiement1,self)
        self._joueurs[2] = Joueur.Joueur(2,"Joueur2",d2,[],zones_deploiement2,self)
        #Creation des cartes es rois
        self._roi_joueur = self.create_card(0,1) #Index + proprietaire
        self._roi_adverse = self.create_card(0,2)
        #Mise en place des rois chez chaque joueur
        self._joueurs[1].focus_roi(self._roi_joueur)
        self._joueurs[2].focus_roi(self._roi_adverse)
        #Positionnement des rois sur le terrain
        milieu = int(self._terrain._taille/2)
        marge = (1 - self._terrain._taille%2)
        self._terrain.add_card(milieu,0,self._joueurs[2]._roi)
        self._terrain.add_card(milieu-marge,-1,self._joueurs[1]._roi)
        #Affichage graphique
        self._terrain.display()#Affiche la grille qui va gérer les evt avec les clicks
        self._joueurs[1]._main.display()#Affiche la main du joueur 1
        self._joueurs[2]._main.display()#Affiche la main du joueur 2
        self._joueurs[1]._deck.shuffle()#Melange le deck du joueur 1
        self._joueurs[2]._deck.shuffle()#Melange le deck du joueur 2
        # Cartes en main de base
        for i in range(2): #On fait piocher 2 carte a chaque joueur
            self._joueurs[1].pioche()
            self._joueurs[2].pioche()
        self._joueurs[2].pioche() #Le joueur 2  qui jouera en 2e commence avec une carte de plus
        # Tour du j1
        self.tour_joueur(1) # On passe au tour du joueur 1
        
    def create_deck_database(self):
        """ Charge la bdd dans les attributs _deck_names et _decks_cards """
        cnx = sq.connect("Outils_pour_le_jeu/decks.sq3") #On charge la db
        curseur = cnx.cursor() #On crée un curseur pour parcourir la db
        curseur.execute("SELECT * FROM deck") #On selectionne toute la db
        datas = curseur.fetchall()#On charge la db dans 'datas'
        self._decks_names = [] #On indique la nature des attributs pour pouvoir utiliser 'append'
        self._decks_cards = []
        for i in range(len(datas)): #On parcours les données de la db (chargée dans datas) et on ajoute deck par deck leurs nom et données aux attributs _deck_names et _deck_cards. Les decks de la db sont sous cette forme : deck = [nom,liste des cartes]
            self._decks_names.append(list(datas)[i][0]) #Le nom est au debut du deck quand il est crée (index 0)
            self._decks_cards.append(eval(list(datas)[i][1])) #Les cartes du deck sont dans une liste d'index 1. 
        print("DECK DATABASE LOADED",self._decks_names)#On informe que la db est chargée et on montre les noms des decks
        cnx.close() #On ferme la db (on en a plus besoin)
        
    def create_card_database(self):
        """ Creation du tableau contenant toutes les cartes """
        #Idem qu'avec les decks
        self._cards = []
        cnx = sq.connect("Outils_pour_le_jeu/cartes.sq3")
        curseur = cnx.cursor()
        curseur.execute("SELECT * FROM cartes")
        datas = curseur.fetchall()
        for i in range(len(datas)):
            self._cards.append(list(datas[i]))
            self._cards[i][4] = eval(self._cards[i][4])#Les paterns sont stockés sous forme de texte donc on le lance comme un script python pour qu'il se transforme en liste
            self._cards[i][5] = eval(self._cards[i][5])#idem
        print("CARD DATABASE LOADED",self._cards)

    def create_card(self,index,proprietaire):
        """ Creation d'un objets cartes """
        #On charge les données de la carte en fonction de l'index donné depuis la db
        nom = self._cards[index][0]
        mana = self._cards[index][1]
        attaque = self._cards[index][2]
        vie = self._cards[index][3]
        patern_atk = self._cards[index][4]
        patern_mvt = self._cards[index][5]
        sprite = self._cards[index][6]
        jeton = self._cards[index][7]
        sprite_dos = self._cards[index][8]
        return Carte.Carte(self,nom,mana,attaque,vie,patern_atk,patern_mvt,jeton,sprite,sprite_dos,proprietaire) #On retourne la carte avec tous les attributs conformes à la db (on pourrait ainsi créer une nouvelle carte depuis ici dans qu'elle ne figure dans la db si on modifiait le code)

    def create_terrain_points(self,taille_terrain):
        """ Creer automatiquement un terrain de points de mana conventionnel """
        tabl1 = mu.array(taille_terrain,taille_terrain,1) #Methode dans Methodes_utiles (importé au debut du prog) qui crée un tableau de taille 'taille_terrain'*'taille_terrain' de valeur pour chaque case : 1
        tabl2 = mu.array(taille_terrain/2,taille_terrain/2,1)#meme genre
        tabl3 = mu.array(2-taille_terrain%2,2-taille_terrain%2,1)#meme genre
        a = 0
        b = 0
        for j in range(int(taille_terrain/4),int(3*taille_terrain/4)):#On additione le 2e tableau au 1er de facon a ce qu'il soit centré
            for i in range(int(taille_terrain/4),int(3*taille_terrain/4)):
                tabl1[j][i] += tabl2[a][b]
                a += 1
            b += 1
            a = 0
        a = 0
        b = 0
        for j in range(int(taille_terrain/2-len(tabl3)/2),int(taille_terrain/2+len(tabl3)/2)): #on additionne le 3e tableau a la somme des 2 1ers de facon a ce qu'il soit centré aussi
            for i in range(int(taille_terrain/2-len(tabl3)/2),int(taille_terrain/2+len(tabl3)/2)):
                tabl1[j][i] += tabl3[a][b]
                a += 1
            b += 1
            a = 0
        return tabl1 #On retourne la somme des 3 tableaux. On pourrait aussi en faire un personnalisé
    
    def tour_joueur(self,index):
        """ Change de tour des joueurs """
        if index == 1: #Commenc le tour du j1
            self._joueur_tour = 1 #L'indique dans l'attribut
            self._joueurs[1].begin_tour() #Commence le tour du j1
            self._joueurs[2].end_tour() #Termine le tour du j2
        else: #Meme logique ci dessous
            self._joueur_tour = 2
            self._joueurs[2].begin_tour()
            self._joueurs[1].end_tour()
            
    def switch_turn(self): #On inverse les tours
        """ Inverse les tours """
        if self._joueurs[1]._tour == True: #Si c'est le tour du j1, on passe a celui du j2 avec la methodes precedente
            self.tour_joueur(2)
        else:# Sinon, on fait l'inverse
            self.tour_joueur(1)
            
game = Game()
game.start()
