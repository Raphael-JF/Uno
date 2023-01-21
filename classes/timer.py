class Timer():
    """Timer est un objet assez simple permettant de renvoyer un signal quand une durée est écoulée"""


    def __init__(self,duree_seconds:int,id:str,infos=None):
        """
        duree_seconds -> la durée en seconde avant laquelle le timer renvoie l'id et les infos.
        id -> un identifiant déterminant le rôle du timer. Cet id est renvoyé lorsque le temps est écoulé.
        infos -> les informations à ajouter en cas d'appel de fonction à la fin du décompte.
        """

        if duree_seconds < 0:
            raise ValueError("Impossible d'attendre une durée négative")


        self.id = id
        self.infos = infos
        self.duree_seconds = duree_seconds
        self.elapsed = 0
        self.finished = False


    def pass_time(self,time):
        """Ajoute time au temps écoulé du Timer. si ce temps écoulé dépasse la durée initalement renseignée, alors cette méthode renvoie l'id et les infos du Timer."""


        self.elapsed += time

        if self.elapsed >= self.duree_seconds:
            self.finished = True
            return self.id,self.infos
            
        return None,None
