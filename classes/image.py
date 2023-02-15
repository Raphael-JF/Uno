import pygame
import os
from itertools import cycle
class Image(pygame.sprite.Sprite):
    def __init__(
        self,
        name:list[str],
        winsize:list,
        scale_axis:list,
        loc:list,
        parent_groups:list,
        alt_names:list[list[str]] = [],
        degrees:float = 0,
        alpha:int = 255,
        layer:int = 0,
        living:bool = True,
    ):
        """
        winsize = [base_width:int,base_height:int] -> taille fenetre pygame
        name = str -> chemin absolu vers l'image en partant du dossier 'images'. Aucune extension n'est concaténée.
        scale_axis = [x_or_y:str,value:int] -> taille voulue pour l'axe x ou y
        loc = [[x:int,y:int],mode:str] -> coordonnées et mode de placement ('center', 'topleft', 'topright', 'bottomleft','bottomright','midtop', midright', 'midbottom','midleft')
        degrees -> angle d'affichage de l'image
        border = [bd_base_width:int,bd_clr:tuple] -> bd_base_width est l'épaisseur de la bordure : pour ne pas en avoir, insérer une valeur négative. bd_clr est la couleur de la bordure. 
        layer -> couche sur laquelle afficher le sprite en partant de 1. Plus layer est élevée, plus la surface sera mise en avant.

        """

        super().__init__()
        
        self.winsize = winsize
        self._layer = layer
        self.pos = loc[0]
        self.placement_mode = loc[1]
        self.parent_groups = parent_groups
        self.resize_ratio = 1
        self.degrees = degrees
        self.alpha = alpha
        self.contenu = pygame.image.load(os.path.join(os.getcwd(),'images',*name))

        self.contenus_list = []
        for i in alt_names + [name]:
            self.contenus_list.append(pygame.image.load(os.path.join(os.getcwd(),'images',*i)))
        self.contenus_cycle = cycle(self.contenus_list)
        
        if scale_axis[0] == "x":
            self.base_height = (scale_axis[1]*self.contenu.get_height()) / self.contenu.get_width()
            self.base_width = scale_axis[1]
            
        elif scale_axis[0] == "y":
            self.base_width = (scale_axis[1]*self.contenu.get_width()) / self.contenu.get_height()
            self.base_height = scale_axis[1]

        else:
            raise ValueError("scale_axis[0] doit être 'x' ou 'y'")

        if living:
            self.liven()

        self.calc_image()
        self.calc_rect()


    def liven(self):

        for group in self.parent_groups:
            group.add(self)


    def calc_image(self):
        """
        Recalcul de la surface du sprite (sa taille).
        """
        self.image = pygame.transform.smoothscale(self.contenu,(round(self.base_width*self.resize_ratio),round(self.base_height*self.resize_ratio)))
        if self.degrees != 0:
            self.image = pygame.transform.rotate(self.image,round(self.degrees,2))

        if self.alpha != 255:
            self.image.set_alpha(self.alpha)
    

    def calc_rect(self):
        """
        Recalcul du rectangle du sprite (ses coordonnées).
        """

        pos = [round(i) for i in self.pos]
        if self.placement_mode == "topleft":
            self.rect = self.image.get_rect(topleft=pos)
        elif self.placement_mode == "topright":
            self.rect = self.image.get_rect(topright=pos)
        elif self.placement_mode == "bottomleft":
            self.rect = self.image.get_rect(bottomleft=pos)
        elif self.placement_mode == "bottomright":
            self.rect = self.image.get_rect(bottomright=pos)
        elif self.placement_mode == "midtop":
            self.rect = self.image.get_rect(midtop=pos)
        elif self.placement_mode == "midleft":
            self.rect = self.image.get_rect(midleft=pos)
        elif self.placement_mode == "midbottom":
            self.rect = self.image.get_rect(midbottom=pos)
        elif self.placement_mode == "midright":
            self.rect = self.image.get_rect(midright=pos)
        elif self.placement_mode == "center":
            self.rect = self.image.get_rect(center=pos)


    def update(self,new_winsize,*args):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)


    def rescale(self,new_winsize):
        """actualisation des valeurs en cas de changement de résolution"""

        self.old_winsize = self.winsize
        self.winsize = new_winsize

        self.ratio = self.winsize[0] / self.old_winsize[0]
        self.base_width = self.base_width*self.ratio
        self.base_height = self.base_height*self.ratio
        self.pos = [i*self.ratio for i in self.pos]
        
        self.calc_image()
        self.calc_rect()


    def switch_image(self,index:int=None):

        if index is None:
            self.contenu = next(self.contenus_cycle)
        else:
            self.contenu = self.contenus_list[index]
        self.calc_image()
        self.calc_rect()