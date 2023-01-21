from utils import transition_many_values
import assets

class Transition():
    """Cette classe implémente la gestion de l'animation. Pour n'importe quelles valeurs étapes, seront calculées les valeurs intermédiaires, pour une durée donnée, pour allonger l'évolution d'une variable.
    exemple : pour passer de 0 à 500 avec une durée de 10 et un mode de transition 'in' (lent au début et croît de plus en plus vite): 
    [0.5, 4, 13.5, 32, 62.5, 108, 171.5, 256, 364.5, 500]"""


    def __init__(self,values:list[int|float|list[int|float]],ease_seconds:list[int],ease_modes:list[str]):
        """
        values -> les valeurs étapes (taille n). valeurs peut contenir des tableaux à une dimension (pratique pour les transitions de couleurs entre autres).
        nb_frames -> les durées de transition entre chaque paire de valeurs (taille n-1 par conséquent)
        ease_modes -> les modes de transition entre chaque paire de valeurs (taille n-1 par conséquent)

        """

        self.nb_frames = []
        for ease_second in ease_seconds:
            self.nb_frames.append(round(ease_second*assets.TIME_TICKING))
        self.ease_modes = ease_modes
        self.values = values
        self.index = 0


    def generer_frame(self,index:int) -> float|list[float]:
        """
        génère la valeur d'index donné
        """

        for i,seconds in enumerate(self.nb_frames) :
                if seconds == 0:
                    return self.values[i+1]

        if type(self.values[0]) in [float,int]:

            return transition_many_values(self.values,self.nb_frames,self.ease_modes,index)
       
        else:
            sortie = []
            for value_steps in zip(*self.values):
                sortie.append(transition_many_values(value_steps,self.nb_frames,self.ease_modes,index))

            return sortie


    def set_step_values(self,values,ease_seconds=None,ease_modes=None):
        """
        Réaffectation des valeurs de l'instance Transition.
        """

        if ease_seconds:
            self.nb_frames = []
            for ease_second in ease_seconds:
                self.nb_frames.append(round(ease_second*assets.TIME_TICKING))

        if ease_modes:
            self.ease_modes = ease_modes 

        self.values = values
        self.index = 0


    def resize_extremums(self,ratio):
        """
        Actualisation des valeurs en cas de changement de résolution.
        """

        if type(self.values[0]) in [float,int]:
            for i,value in enumerate(self.values):
                self.values[i] = value*ratio
            
        else:

            for i,step_values in enumerate(self.values):
                self.values[i] = list(step_values)

                for j, value in enumerate(step_values):
                    self.values[i][j] = value*ratio
            


    def change_index(self,dt:float,cur_val:int|float|list[int|float]):
        """
        dt_x_fps -> le temps écoulé de puis la dernière image multiplié par le nombre d'image/seconde
        """

        self.index += dt * assets.TIME_TICKING
        
        if self.index < 0:
            self.index = 0
        if self.index > sum(self.nb_frames)-1:
            self.index = sum(self.nb_frames)-1

        frame = self.generer_frame(round(self.index))

        return frame,frame != cur_val,self.index == sum(self.nb_frames)-1
    
    def get_list_of_values(self):
        """
        Renvoie une liste de toutes les valeurs successives. Pratique pour tester.
        """
        sortie = []
        for i in range(sum(self.nb_frames)):
            temp = self.generer_frame(i)
            if type (temp) in [int,float]:
                sortie.append(round(temp))
            else:
                temp = [round(i) for i in temp]
                sortie.append(temp)
        return sortie

        