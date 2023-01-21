import pygame
import os

class Image(pygame.sprite.Sprite):
    def __init__(
        self,
        name:list[str],
        winsize:list,
        scale_axis:list,
        loc:list,
        degrees:int = 0,
        border:list = [-1,(0,0,0)],
        layer:int = 0
    ):
        """
        winsize = [width:int,height:int] -> taille fenetre pygame
        name = str -> chemin absolu vers l'image en partant du dossier 'images'. Aucune extension n'est concaténée.
        scale_axis = [x_or_y:str,value:int] -> taille voulue pour l'axe x ou y
        loc = [[x:int,y:int],mode:str] -> coordonnées et mode de placement ('center', 'topleft', 'topright', 'bottomleft','bottomright','midtop', midright', 'midbottom','midleft')
        degrees -> angle d'affichage de l'image
        border = [bd_width:int,bd_clr:tuple] -> bd_width est l'épaisseur de la bordure : pour ne pas en avoir, insérer une valeur négative. bd_clr est la couleur de la bordure. 
        layer -> couche sur laquelle afficher le sprite en partant de 1. Plus layer est élevée, plus la surface sera mise en avant.

        """

        super().__init__()
        
        self.degrees = degrees
        self.name = name
        self.winsize = winsize
        self._layer = layer
        self.pos = loc[0]
        self.placement_mode = loc[1]
        
        if len(border[1]) != 4:
            border[1] = list(border[1])
            border[1].append(255)

        self.base_border_width = border[0]
        self.base_border_clr = border[1][:]

        self.cur_border_width = self.base_border_width
        self.cur_border_clr = self.base_border_clr[:]

        contenu = pygame.image.load(os.path.join(os.getcwd(),'images',*self.name))
        
        if scale_axis[0] == "x":
            self.height = (scale_axis[1]*contenu.get_height()) / contenu.get_width()
            self.width = scale_axis[1]
            
        elif scale_axis[0] == "y":
            self.width = (scale_axis[1]*contenu.get_width()) / contenu.get_height()
            self.height = scale_axis[1]

        else:
            raise ValueError("scale_axis[0] doit être 'x' ou 'y'")


    def calc_image(self):
        """
        Recalcul de la surface du sprite, ainsi que son rectangle.
        """

        self.image = pygame.Surface([
            round(self.width + self.cur_border_width*2),
            round(self.height + self.cur_border_width*2)
        ],pygame.SRCALPHA)

        border_rect = pygame.Rect(0,0, *self.image.get_size())
        border_rect.center = self.image.get_rect().center

        pygame.draw.rect(
            self.image,
            self.cur_border_clr,
            border_rect,
            round(self.cur_border_width)
        )

        contenu = pygame.image.load(os.path.join(os.getcwd(),'images',*self.name)).convert_alpha()
        contenu = pygame.transform.smoothscale(contenu,(round(self.width),round(self.height)))

        self.image.blit(contenu,contenu.get_rect(center=self.image.get_rect().center))
        
        if self.degrees != 0:
            self.image = pygame.transform.rotate(self.image,self.degrees)
        
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


    def update(self,new_winsize,**args):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)


    def rescale(self,new_winsize):
        """actualisation des valeurs en cas de changement de résolution"""

        self.old_winsize = self.winsize
        self.winsize = new_winsize

        self.ratio = self.winsize[0] / self.old_winsize[0]
        self.width = self.width*self.ratio
        self.height = self.height*self.ratio
        self.cur_border_width = self.cur_border_width*self.ratio
        self.pos = [i*self.ratio for i in self.pos]
        
        self.calc_image()
