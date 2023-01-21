from classes.button import Button

class Button_family():
    """
    L'objet Button_family implémente la possibilité de créer des groupes d'objets Button dans l'optique de leur assigner des états. Cet objet est destiné à gérer des boutons à interactions mutuelles (ex: paire de boutons Oui/Non)
    """

    def __init__(self,*states):
        """
        Prend en argument les états que les boutons pourront avoir.
        
        ATTENTION ! Les états que l'on manipule ici n'ont aucun lien avec les états de l'objet Button :
        - dans Button, les états possibles sont "hov", "active" et "base", et cet état change dynamiquement en fonction de l'action utilisateur
        - dans cette classe, les états ne représentent que de simples attributs qui permettent de marquer un bouton dans la famille de boutons.
        """
        
        self.states = states
        self.buttons_state = {}
        self.buttons_start_states = {}
        self.style_rules = {}
        

    def get_buttons(self):
        """
        Méthode d'obtention d'un tableau
        """
        return list(self.buttons_state.keys())


    def add_button(self,button:Button,start_state:str):
        """
        Prend en argument un bouton (objet Button) et l'état de départ qui lui sera assigné.
        """
        
        if start_state not in self.states:
            raise ValueError("state specified doesn't match with any existing state")

        self.buttons_state[button] = start_state
        self.buttons_start_states[button] = start_state

    def reset_states(self):
        """
        Réassigne à chaque bouton son état de départ.
        """

        for button in self.buttons_state.keys():
            self.set_state(button,self.buttons_start_states[button])
        
    
    def add_style_rule(self,state,**styles):
        """Attribution du style à donner aux boutons quand ils ont l'état renseigné.
        styles doit contenir des valeurs pour : 
        base_background_clr, base_border, 
        hov_background_clr, hov_border, 
        active_background_clr, active_border
        
        Il n'est pas nécessaire de tous les renseigner : seul les attribut contenant 'base' dans leur nom sont obligatoires.
        """
        
        self.style_rules[state] = styles

        for button,b_state in self.buttons_state.items():
            if b_state == state:
                button.reset_style(**self.style_rules[state])
                button.reset_attributes()
        

    def get_state(self,button:Button):
        """
        Méthode de lecture de l'état d'un bouton
        """

        if button not in self.buttons_state.keys():
            raise KeyError("button gived not recognized in this Button_family")

        return self.buttons_state[button]


    def set_state(self,button,state):
        """
        Méthode d'écriture d'un état pour un bouton
        """

        if state not in self.states:
            raise KeyError("button gived not recognized in this Button_family")
        
        self.buttons_state[button] = state
        button.reset_style(**self.style_rules[state])


    def __contains__(self,button):
        """
        Méthode permettant d'utiliser l'instruction 'in' sur un objet Button_family
        """

        return button in self.buttons_state.keys()

    