import Carte

def array(w,h,val):
    """ Créée un tableau de 'w'*'h' avec 'val' comme seule valeur """
    liste = []
    for j in range(int(w)):
        liste.append([])
        for i in range(int(h)):
            liste[j].append(val)
    return liste

def copy_list(obj,dim):
    """ Copie simple d'une liste composée de int, et d'objet cartes """
    obj2 = []
    def copy_obj(ob):
        """ Copie un objet carte """
        nom = str(ob._nom)
        mana = int(ob._mana)
        attaque = int(ob._attaque)
        vie = int(ob._vie)
        pa = list(ob._patern_atk)
        pd = list(ob._patern_depl)
        je = ob._jeton
        sprite = ob._sprite
        dos = ob._dos
        prop = int(ob._proprietaire)
        root = ob._root
        pea =bool(ob._peut_attaquer)
        ped = bool(ob._peut_deplacer)
        if ob._x == None and ob._y == None:
            x = None
            y = None
        else:
            x = int(ob._x)
            y = int(ob._y)
        roi = bool(ob._roi)
        #face = obj[i]._face
        carte = Carte.Carte(root,nom,mana,attaque,vie,pa,pd,je,sprite,dos,prop)
        carte._peut_attaquer = pea
        carte._peut_deplacer = ped
        carte._x = x
        carte._y = y
        carte._roi = roi
        return carte
                
    print("OBJJJJJJ",obj)
    if dim == 1:
        for j in range(len(obj)):
            if str(type(obj[j])) == "<class 'NoneType'>":
                obj2.append(None)
            if str(type(obj[j])) == "<class 'int'>":
                obj2.append(int(obj[j]))
            if str(type(obj[j])) == "<class 'Carte.Carte'>":
                carte = copy_obj(obj[j])
                obj2.append(carte)
    if dim == 2:
        for i in range(len(obj)):
            obj2.append([])
            for j in range(len(obj[i])):
                if str(type(obj[i][j])) == "<class 'NoneType'>":
                    obj2[i].append(None)
                if str(type(obj[i][j])) == "<class 'int'>":
                    obj2[i].append(int(obj[i][j]))
                if str(type(obj[i][j])) == "<class 'Carte.Carte'>":
                    carte = copy_obj(obj[i][j])
                    obj2[i].append(carte)
    return obj2



            
            
