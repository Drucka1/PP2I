from random import sample

def retire_elt(l,elt):
    l_ = l.copy()
    l_.remove(elt)
    return l_

def ajout_elt(l,elt):
    l_ = l.copy()
    l_.append(elt)
    return l_

def creation_liste_repas(recettes,budget__max,nb_repas):
    recette_melange = sample(recettes,k=len(recettes))
    
    menus_possible = []
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
    
print(creation_liste_repas([(1,4),(2,8),(3,3),(4,6),(5,7),(6,15)],13,3))