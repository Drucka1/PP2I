from flask import g
from random import sample
import sqlite3, hashlib, os

current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, '..', 'instance', 'site.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_path)
    return db

def hash(string):
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    return hash_object.hexdigest()

def get_toutes_recettes(cursor):  
    recettes = []
    
    for elt in list(cursor):
        dict_tmp = {}
        dict_tmp['id'] = elt[0]
        dict_tmp['nom'] = elt[1]
        dict_tmp['image'] = elt[4]
        recettes.append(dict_tmp)
        
    for elt in recettes:
        c = get_db().cursor()
        c.execute("SELECT name,amountdenom,unit FROM ingredient JOIN ingredients ON ingredients.id = ingredient.ingredientid WHERE recipeid='"+str(elt['id'])+"' ORDER BY line")
        elt['ingredient'] = list(c)
        d = get_db().cursor()
        d.execute("SELECT txt FROM instruction WHERE recipeid='"+str(elt['id'])+"' ORDER BY line")
        elt['instruction'] = [elt_[0] for elt_ in list(d) if elt_[0] != '']
                
    return recettes

def get_full_recette(cursor):  
    
    elt = list(cursor)[0]
    dict_tmp = {}
    dict_tmp['id'] = elt[0]
    dict_tmp['nom'] = elt[1]
    dict_tmp['image'] = elt[4]
    c = get_db().cursor()
    c.execute("SELECT name,amountdenom,unit FROM ingredient JOIN ingredients ON ingredients.id = ingredient.ingredientid WHERE recipeid='"+str(dict_tmp['id'])+"' ORDER BY line")
    dict_tmp['ingredient'] = list(c)
    d = get_db().cursor()
    d.execute("SELECT txt FROM instruction WHERE recipeid='"+str(dict_tmp['id'])+"' ORDER BY line")
    dict_tmp['instruction'] = [elt_[0] for elt_ in list(d) if elt_[0] != '']
                
    return dict_tmp

def get_min_recettes(cursor):  
    recettes = []
    
    for elt in list(cursor):
        dict_tmp = {}
        dict_tmp['id'] = elt[0]
        dict_tmp['nom'] = elt[1]
        dict_tmp['image'] = elt[4]
        recettes.append(dict_tmp)
               
    return recettes

def get_recette_realisable_user():
    def appartient_liste_liste(elt,liste_liste):
        for liste in liste_liste:
            for elt_ in liste:
                if type(elt_) != int and elt in elt_ :
                    return True
        return False
            
    c = get_db().cursor()
    c.execute("SELECT * FROM recipes LIMIT 300")
    
    recettes = get_toutes_recettes(c)
    
    for allergene in session['allergene']:
        for recette in recettes:
            if appartient_liste_liste(allergene,recette['ingredient']) or appartient_liste_liste(allergene,recette['instruction']) :
                recettes.remove(recette)

    for ustensile in get_ustensiles():
        for recette in recettes:
            if ustensile not in session['ustensile'] and appartient_liste_liste(ustensile,recette['instruction']):
                recettes.remove(recette)
                
    return [recette['id'] for recette in recettes]
        

def get_ustensiles():
    d = get_db().cursor()
    d.execute("SELECT nom FROM ustensiles")
    return [elt[0] for elt in list(d)]

def get_allergenes():
    c = get_db().cursor()
    c.execute("SELECT nom FROM allergenes")
    return [elt[0] for elt in list(c)]

def creation_menu(recettes,budget__max,nb_repas):
    recette_melange = sample(recettes,k=len(recettes))
    
    def retire_elt(l,elt):
        l_ = l.copy()
        l_.remove(elt)
        return l_

    def ajout_elt(l,elt):
        l_ = l.copy()
        l_.append(elt)
        return l_
    
    def rec(recette_utilise,budget_encours,recette_restante):
        if len(recette_utilise) == nb_repas :
            return recette_utilise
        
        for elt in recette_restante:
            if budget_encours + elt[1] <= budget__max:
               tmp = rec(ajout_elt(recette_utilise,elt[0]),budget_encours + elt[1],retire_elt(recette_restante,elt))
               if tmp != [] :
                   return tmp
        return []
    return rec([],0,recette_melange)

