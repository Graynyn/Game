from tkinter import *
from PIL.ImageTk import *
from PIL import *
from Methodes_utiles import *
import sqlite3

cnx = sqlite3.connect("cartes.sq3")
curseur = cnx.cursor()

def save():
    global no_carte_edit,curseur
    print("entries",Entries)
    name = Entries[0].get()
    mana = int(Entries[1].get())
    attaque = int(Entries[2].get())
    vie = int(Entries[3].get())
    patern_atk = Entries[4]
    patern_depl = Entries[5]
    sprite_carte = Entries[6].get()
    sprite_jeton = Entries[7].get()
    sprite_dos = Entries[8].get()
    fichier_save = open("Cartes_version_txt/"+name+".txt","w")
    liste_donnees_cartes[no_carte_edit] = [name,mana,attaque,vie,patern_atk,patern_depl,sprite_carte,sprite_jeton,sprite_dos]
    curseur.execute("DELETE FROM cartes")
    for i in range(len(liste_donnees_cartes)):
        curseur.execute("INSERT INTO cartes VALUES"
                        "('"+liste_donnees_cartes[i][0]+"','"
                        ""+str(liste_donnees_cartes[i][1])+"','"
                        ""+str(liste_donnees_cartes[i][2])+"','"
                        ""+str(liste_donnees_cartes[i][3])+"','"
                        ""+str(liste_donnees_cartes[i][4])+"','"
                        ""+str(liste_donnees_cartes[i][5])+"','"
                        ""+liste_donnees_cartes[i][6]+"','"
                        ""+liste_donnees_cartes[i][7]+"','"
                        ""+liste_donnees_cartes[i][8]+"')")
    cnx.commit()
    
def see():
    """ Fonction permettant de visualiser les cartes déjà crées et de les modifier """
    global curseur
    #Creation du menu
    menu = Menu(fen)
    fen['menu'] = menu
    menu_cartes = Menu(menu)
    menu.add_cascade(label="Cartes",menu=menu_cartes)
    #Récupération des données des fichiers :
    """liste_cartes = liste_fichiers #Ouverture du fichier contenant le noms des cartes
    #Init de la phase de montage de la liste de données des cartes
    liste_fichiers_cartes = []
    liste_donnees_cartes = []
    liste_boutons = []"""
    curseur.execute("SELECT * FROM cartes")
    resultat = []
    for i in curseur.fetchall():
        print(i)
        resultat.append(list(i))
    for i in range(len(resultat)):
        resultat[i][4] = eval(resultat[i][4])
        resultat[i][5] = eval(resultat[i][5])
    liste_donnees_cartes = resultat
    for i in range(len(liste_donnees_cartes)):
        def info(i=i):
            print("GO",liste_donnees_cartes[i])
            return edit(i,liste_donnees_cartes[i][0],liste_donnees_cartes[i][1],liste_donnees_cartes[i][2],liste_donnees_cartes[i][3],liste_donnees_cartes[i][4],liste_donnees_cartes[i][5],liste_donnees_cartes[i][6],liste_donnees_cartes[i][7],liste_donnees_cartes[i][8])
        name = liste_donnees_cartes[i][0]
        menu_cartes.add_command(label=name,command=info)
    def new_card():
        return create_new_card(len(liste_donnees_cartes))
    menu_cartes.add_command(label="New",command=new_card)
    global liste_donnees_cartes

def reset_canvas():
    global can,can2,can3,can4,can5,can6,can7,can8
    can.destroy()
    can2.destroy()
    can3.destroy()
    can4.destroy()
    can5.destroy()
    can6.destroy()
    can7.destroy()
    can8.destroy()
    can = Canvas(fen)
    can2 = Canvas(fen)
    can3 = Canvas(fen)
    can4 = Canvas(fen)
    can5 = Canvas(fen)
    can6 = Canvas(fen)
    can7 = Canvas(fen)
    can8 = Canvas(fen)
    can.grid(column=0,row=0)
    can2.grid(column=1,row=0)
    can3.grid(column=2,row=0)
    can4.grid(column=3,row=0)
    can5.grid(column=4,row=0)
    can6.grid(column=5,row=0)
    can7.grid(column=6,row=0)
    can8.grid(column=7,row=0)
    im = []
    
def edit(i,d0,d1,d2,d3,d4,d5,d6,d7,d8):
    global no_carte_edit
    no_carte_edit = i
    reset_canvas()
    Entries = [0,0,0,0,0,0,0,0,0]
    global Entries
    Entries[0] = make_entry("name",can,d0)
    Entries[1] = make_entry("mana",can,d1)
    Entries[2] = make_entry("atk",can,d2)
    Entries[3] = make_entry("vie",can,d3)
    Entries[4] = make_echiquier(can2,7,d4) #Patern atk
    label1 = Label(can3,text="<= Patern Attaque")
    label2 = Label(can3,text="Patern Mouvement =>")
    label1.pack()
    label2.pack()
    button1 = Button(can3,text="Save",command=save)
    button1.pack()
    Entries[5] = make_echiquier(can4,7,d5) #Patern Depl
    Entries[6] = make_image(can5,"Sprite Carte",d6)
    Entries[7] = make_image(can6,"Sprite Jeton",d7)
    Entries[8] = make_image(can7,"Sprite Dos",d8)

def create_new_card(i):
    global can
    reset_canvas()
    e = make_entry("Nom du fichier",can,"")
    def edit_new_card():
        edit(i,"nom","mana","atk","pv",None,None,"","","") #Note : 'i' est la valeur de l'index de la derniere carte du menu deroulant on y ajoute donc '1'
    button = Button(can,text="OK",command=edit_new_card)
    button.pack()
    
def make_entry(text,can,defaut):
    label = Label(can,text=text)
    label.pack()
    e = Entry(can)
    e.pack()
    e.focus_set()
    e.insert(0,defaut)
    return e
def make_choice(can,choix,defaut):
    num_choice = 0
    global num_choice
    def change():
        global num_choice
        num_choice += 1
        if num_choice >= len(choix):
            num_choice = 0
        button.configure(text=choix[num_choice])

    button = Button(can,text=choix[num_choice],command=change)
    button.pack()
    return num_choice
def make_echiquier(can,taille,defaut):
    echiquier = []
    labels = []
    
    def get_click(evt,x,y,echiquier,labels):
        if echiquier[y][x] == 1:
            echiquier[y][x] = 0
        else :
            if echiquier[y][x] == 0:
                echiquier[y][x] = 1
        draw(echiquier,labels)

    def draw(echiquier,labels):
        for i in range(taille):
            for j in range(taille):
                if echiquier[i][j] == 0:
                    txt = ""
                else:
                    if echiquier[i][j] == 1:
                        txt = "X"
                    else:
                        if echiquier[i][j] == 2:
                            txt = "O"
                        else:
                            txt = "?"
                labels[i][j].configure(text=txt)
    #On charge les données sauvegardées
    if defaut != None:
        echiquier = defaut
    else:
        for j in range(taille):
            echiquier.append([])
            for i in range(taille):
                echiquier[j].append(0)
        echiquier[int((taille-1)/2)][int((taille-1)/2)] = 2
    for j in range(taille):
        labels.append([])
        for i in range(taille):
            def click(evt,i=i,j=j,echiquier=echiquier,labels=labels):
                return get_click(evt,i,j,echiquier,labels)
            if (j+i)%2 == 0:
                label = Label(can,bg='white')
            else:
                label = Label(can,bg='light grey')
            label.grid(row = j, column = i)
            label.configure(width=7,height=3)
            label.bind('<Button-1>',click)
            labels[j].append(label)
    draw(echiquier, labels)
    print("ech",echiquier)
    return echiquier
        
def make_image(canv,text,defaut):
    label = Label(canv,text=text)
    label.pack(side=TOP)
    label2 = Label(canv)
    label2.pack(side=TOP)
    chemin = make_entry('',canv,defaut)
    def ab(chemin=chemin,label=label2):
        chemin.delete(0)
        file = tkinter.filedialog.askopenfilename()
        file = simplifier_chemin(file,"I:/Projet_ISN/Classes_du_jeu/Outils_pour_le_jeu/")
        im1 = Image.open(file)
        im2 = PhotoImage(image=im1)
        label.configure(image=im2)
        chemin.delete(0,END)
        chemin.insert(0,file)
        im.append(im2)
        return im2
    button1 = Button(canv,text="change",command=ab )
    button1.pack(side=TOP)
    return chemin
    
        
    
fen = Tk()
can = Canvas(fen)
can.grid(column=0,row=0)
can2 = Canvas(fen)
can2.grid(column=1,row=0)
can3 = Canvas(fen)
can3.grid(column=2,row=0)
can4 = Canvas(fen)
can4.grid(column=3,row=0)
can5 = Canvas(fen)
can5.grid(column=4,row=0)
can6 = Canvas(fen)
can6.grid(column=5,row=0)
can7 = Canvas(fen)
can7.grid(column=6,row=0)
can8 = Canvas(fen)
can8.grid(column=7,row=0)
global can,can2,can3,can4,can5
im = []
global im
see()


fen.mainloop()
