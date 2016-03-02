from tkinter import *
from PIL import *
from PIL.ImageTk import *
from Methodes_utiles import *
import sqlite3 as db
#La base de l'interface
fen = Tk()

can = Canvas(fen)
can2 = Canvas(fen)
can_line = Canvas(fen)
can_zoom = Canvas(fen)

can.grid(column=0,row=0)
can_line.grid(column=1,row=0)
can2.grid(column=2,row=0)
can_zoom.grid(column=0,row=1)
#Creation du Menu principal pour ouvrir les != decks
menu = Menu(fen)
fen['menu'] = menu
menu_deck = Menu(menu)
menu.add_cascade(label='Decks',menu=menu_deck)

#Var modifiables
taille_x_l = 10 #Nombre de cartes sur l'axe X du canvas gauche
taille_y_l = 5 #idem pour l'axe Y

taille_x_r = 6 #idem pour celui de droite
taille_y_r = 5 #la meme

global taille_x_l, taille_y_l
global taille_x_r, taille_y_r

no_page = 1 #numero actuel de la page du canvas gauche
deck = [] #liste des cartes du deck (int)
index_deck = 0 #Index du deck en edition
cartes = [] #Database des cartes
noms_decks = [] #Nom des decks disponibles (list de string)

global no_page,deck
#config de la ligne de séparation entre les 2 canvas principaux
can_line.configure(width=20,height=200)
can_line.create_line(10,10,10,190)

#db - DECKS
cnx = db.connect("decks.sq3")
curseur = cnx.cursor()
curseur.execute("SELECT * FROM deck")
names = []
decks = []
for i in curseur.fetchall():
    names.append(list(i)[0])
    decks.append(eval(list(i)[1]))
print(names,decks)

#db - CARDS
cnx2 = db.connect("cartes.sq3")
curseur2 = cnx2.cursor()
curseur2.execute("SELECT * FROM cartes")
cards = []
for i,v in enumerate(curseur2.fetchall()):
    cards.append(list(v))
    cards[i][4] = eval(cards[i][4])
    cards[i][5] = eval(cards[i][5])
    
cnx2.commit()
cnx2.close()
print(cards)

#gestion graphique
images = []
labels1 = []
labels2 = []
label_zoom = Label(can_zoom)
label_zoom.pack()
global labels1,labels2,label_zoom,images

""" Menu"""
def create_commands():
    global noms_decks
    for i in range(len(decks)):
        def relais(i=i,decks=decks):
            return load_deck(i,decks)
        menu_deck.add_command(label=names[i],command=relais)
#Commandes : 
def load_deck(index,datas):
    global deck, index_deck
    deck = decks[index]
    display_labels(taille_x_r,taille_y_r,can2,labels2)
    aff_deck()
""" Images """
def sprite(index):
    im1 = Image.open(cards[index][7])
    im2 = PhotoImage(image=im1)
    images.append(im2)
    return im2
                           
def sprite2():
    im1 = Image.open("Images/dos2.png")
    im2 = PhotoImage(image=im1)
    images.append(im2)
    return im2
""" CARTE DATABASE """
        
""" Clicks """
def left_click_coll(index_card):
    global deck
    if len(deck) < 30:
        deck.append(index_card)
        aff_deck()
        
def left_click_deck(index_card):
    global deck
    if index_card < len(deck):
        del deck[index_card]
        aff_deck()
    
def right_click(index_card):
    global label_zoom
    im1 = Image.open(cartes[index_card][6])
    im2 = PhotoImage(image=im1)
    images.append(im2)
    label_zoom.configure(image=im2)
    
""" Affichage """                         
def aff_page(width=taille_x_l,height=taille_y_l,canv=can):
    display_labels(width,height,canv,labels1)
    for j in range(height):
        for i in range(width):
            index = ((no_page-1)*width*height + j*width +i)
            print(index,len(cards))
            if len(cards) > index:
                labels1[i][j].configure(image=sprite(index))

def display_labels(width,height,canv,labels):
    for j in range(width):
        labels.append([])
        for i in range(height):
            def relais_l(evt,j=j,i=i):
                index_card = int(((no_page-1)*width*height + j*width +i)/10)
                if labels == labels1:
                    return left_click_coll(index_card)
                if labels == labels2:
                    return left_click_deck(index_card)
            def relais_r(evt,j=j,i=i):
                index_card = int(((no_page-1)*width*height + j*width +i)/10)
                return right_click(index_card)
            labels[j].append(Label(canv))
            labels[j][i].grid(column=j,row=i)
            labels[j][i].bind('<Button-1>',relais_l)
            labels[j][i].bind('<Button-3>',relais_r)

""" 2e Can """
def aff_deck():
    global deck
    for j in range(30):
        y = j%taille_y_r
        x = int(j/taille_y_r)
        if j >= len(deck):
            labels2[x][y].configure(image=sprite2())
        else:
            labels2[x][y].configure(image=sprite(deck[j]))

"""Boutons"""
def vider_deck():
    global deck
    deck = []
    aff_deck()

def save():
    decks[index_deck] = deck
    curseur.execute("DELETE FROM deck")
    for i in range(len(decks)):
        curseur.execute("INSERT INTO deck(name,cards) VALUES('"+names[i]+"','"+str(decks[i])+"')")
    cnx.commit()
    curseur.execute("SELECT * FROM deck")
    print("SAVED",len(deck),curseur.fetchall())

button_vider = Button(fen,text="Vider le deck",command=vider_deck)
button_vider.grid()
button_save = Button(fen,text="Sauvegarder le deck",command=save)
button_save.grid()
aff_page()
create_commands()
                   
