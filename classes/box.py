

import pygame

class Box(pygame.sprite.Sprite):
    """
L'objet Box est le widget le plus bas niveau (il n'hérite de rien d'autre que pygame.sprite.Sprite) : il permet l'implémentation très simple sous forme d'un sprite d'une boite statique d'une couleur donnée (alpha permis) et d'une bordure entourant cette boite définie par l'utilisateur
"""
    
    def __init__(
        self,
        winsize:list,
        size:list,
        loc:list,
        background_clr:tuple,
        parent_groups:list,
        border:list = [-1,(0,0,0),0,"inset"],
        living:bool = True,
        layer:int = 0
    ) -> None:
        """
        winsize = [width:int,height:int] -> taille de la fenetre pygame
        size = [width:int,height:int] -> taille de la box
        loc = [[x:int,y:int],mode:str] -> coordonnées et mode de placement ('center', 'topleft', 'topright', 'bottomleft','bottomright','midtop', midright', 'midbottom','midleft')
        background_clr = [r:int,g:int,b:int,alpha:int|None] -> couleur de fond de la boîte
        parent_groups -> liste des groupes auxquels le sprite est rattaché
        border = [bd_width:int,bd_clr:tuple,bd_padding:int,border_mode:str] -> bd_width est l'épaisseur de la bordure : pour ne pas en avoir, insérer une valeur négative. bd_clr est la couleur de la bordure. bd_padding est l'espacement entre le bout de la surface et la bordure. border_mode ('inset' ou 'outset') définit si la bordure est intérieur ou extérieur à la surface (comme en html-css).
        living -> booléen indiquant si à sa création le sprite doit exister dans ses groupes ('living' car selon pygame, un sprite mort est un sprite qui n'appartient à aucun groupe)
        layer -> couche sur laquelle afficher le sprite en partant de 0. Plus layer est élevée, plus la surface sera mise en avant.
        """

        super().__init__()

        self.winsize = winsize
        self.width = size[0]
        self.height = size[1]

        self._layer = layer
        self.parent_groups = parent_groups

        self.pos = loc[0]
        self.placement_mode = loc[1]

        self.base_background_clr = list(background_clr[:])
        self.base_border_width = border[0]
        self.base_border_clr = list(border[1][:])
        self.base_border_padding = border[2]

        self.cur_background_clr = list(background_clr[:])
        self.cur_border_width = border[0]
        self.cur_border_clr = list(border[1][:])
        self.cur_border_padding = border[2]

        self.border_position = border[3]

        if len(self.base_background_clr) != 4:
            self.base_background_clr.append(255)
            self.cur_background_clr.append(255)

        if len(self.cur_border_clr) != 4:
            self.base_border_clr.append(255)
            self.cur_border_clr.append(255)

        self.calc_box()

        if living:
            self.liven()


    def liven(self):
        """
        A l'inverse de kill() (méthode de pygame.sprite.Sprite permettant de suppprimer le sprite de tous les groupes dans lesquels il se trouve), ajoute le sprite à tous ses groupes parents.
        """

        for group in self.parent_groups:
            group.add(self)

        
    def calc_box(self) -> None:
        """
        Recalcul de la surface du sprite, ainsi que son rectangle.
        """

        if self.border_position == "inset":

            self.image = pygame.Surface([
                round(self.width),
                round(self.height)
                ],pygame.SRCALPHA)
            self.image.fill(self.cur_background_clr)

            border_rect = pygame.Rect(0,0, round(self.width - self.cur_border_padding*2), round(self.height - self.cur_border_padding*2))
            border_rect.center = self.image.get_rect().center

            pygame.draw.rect(
            self.image,
            self.cur_border_clr,
            border_rect,
            round(self.cur_border_width)
            )


        elif self.border_position == "outset":

            self.image = pygame.Surface([
                round(self.width + self.cur_border_width*2 + self.cur_border_padding*2),
                round(self.height + self.cur_border_width*2 + self.cur_border_padding*2)
                ],pygame.SRCALPHA)
            self.image.fill(self.cur_background_clr)

            border_rect = pygame.Rect(0,0, round(self.width + self.cur_border_width*2) , round(self.height + self.cur_border_width*2) )
            border_rect.center = self.image.get_rect().center

            pygame.draw.rect(
            self.image,
            self.cur_border_clr,
            border_rect,
            round(self.cur_border_width)
            )

        else:
            raise ValueError ("border_position must be 'inset' or 'outset'")

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

    def update(self,new_winsize,**args) -> None:
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)


    def rescale(self,new_winsize) -> None:
        """actualisation des valeurs en cas de changement de résolution"""

        old_winsize = self.winsize[:]
        self.winsize = new_winsize

        self.ratio = self.winsize[0] / old_winsize[0]

        self.width = self.width*self.ratio
        self.height = self.height*self.ratio
        self.cur_border_width = self.cur_border_width*self.ratio
        self.cur_border_padding = self.cur_border_padding*self.ratio
        self.pos = [i*self.ratio for i in self.pos]
        
        self.calc_box()
    