"""des fonctions en tous genres"""

def transition(valdebut:float,valfin:float,duree:int,ease_mode:str,avancement:int=None) -> float or list:
    """Calcul de la fonction d'accélaration cubique d'une valeur à une autre.
    - valdebut est la valeur de début
    - valfin est la valeur de fin
    - duree est le nombre de cases du tableau renvoyé
    - ease_mode est le mode de transition ('in','out','inout','linear')
    - si avancement est renseigné, renvoie la valeur d'index avancement, sinon renvoie toutes les valeurs dans un tableau"""

    if duree == 0:
        return valfin if avancement==None else [valfin]

    if avancement == None:
        sortie = []
        for avancement in range(1,duree):
            evolution = avancement / duree
            if ease_mode == "in":
                valeur = evolution**3
                sortie.append(valfin*valeur + valdebut*(1-valeur))
            elif ease_mode == "out":
                valeur = (evolution - 1)**3 + 1
                sortie.append(valfin*valeur + valdebut*(1-valeur))
            elif ease_mode == "inout":
                if evolution < 0.5:
                    valeur = 4 * evolution**3
                    sortie.append(valfin*valeur + valdebut*(1-valeur))
                else:
                    valeur = 0.5*(2*evolution - 2)**3 + 1
                    sortie.append(valfin*valeur + valdebut*(1-valeur))
            elif ease_mode == "linear":
                valeur = (valfin-valdebut) / duree
                sortie.append(valdebut + valeur*avancement)
            else:
                raise ValueError("ease_mode doit être dans ['in','inout','out','linear']")
        return sortie + [valfin]
    else:
        avancement+=1
        if avancement > duree:
            raise ValueError("avancement ne peut être supérieur ou égal à duree")
        if avancement == duree : 
            return float(valfin)
        evolution = avancement / duree
        if ease_mode == "in":
            valeur = evolution**3
            return valfin*valeur + valdebut*(1-valeur)
        elif ease_mode == "out":
            valeur = (evolution - 1)**3 + 1
            return valfin*valeur + valdebut*(1-valeur)
        elif ease_mode == "inout":
            if evolution < 0.5:
                valeur = 4 * evolution**3
                return valfin*valeur + valdebut*(1-valeur)
            else:
                valeur = 0.5*(2*evolution - 2)**3 + 1
                return valfin*valeur + valdebut*(1-valeur)
        elif ease_mode == "linear":
                valeur = (valfin-valdebut) / duree
                return valdebut + valeur*avancement
        else:
            raise ValueError(f"ease_mode:{ease_mode} doit être dans ['in','inout','out','linear']")


def transition_many_values(values:list,durees:list,ease_modes:str,avancement:int=None):
    """
    values -> les valeurs que prendra la valeur à modifier
    durees -> les durées respectives à chaque transition
    ease_mode -> le mode de transformation : soit 'linear', soit 'inout' ('out' et 'in' autorisés pour 3 valeurs au plus)
    """
    
    if len(values) != len(durees)+1 != len(ease_modes)+1:
        raise ValueError("len(values), len(duree)+1 and len(ease_modes)+1 must be equal")

    if avancement == None:
        val_debut = values.pop(0)
        sortie = []

        for value,duree,ease_mode in zip(values,durees,ease_modes):
            sortie += transition(val_debut,value,duree,ease_mode)
            val_debut = value
        return sortie

    else:
        for i,duree in enumerate(durees):
            if avancement-duree > 0:
                avancement -= duree
            else:
                break
        return transition(values[i],values[i+1],duree,ease_modes[i],avancement-1)

        

