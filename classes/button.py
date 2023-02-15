import pygame
from classes.title import Title
from classes.transition import Transition

from assets import TIME_TICKING

class Button(Title):
    """
    Héritant de l'objet Title, Button implémente la possibilité de réagir à une action utilisateur et de changer certains de ses paramètres en fonction des états du sprite (clické, survolé...)
    """

    def __init__(
        self,
        winsize:list,
        loc:list,
        background_clr:tuple,
        font_clrs:list,
        parent_groups:list,
        font_size:int = 0,
        border:list = [0,(0,0,0),0,"inset"],
        size:list = [None,None],
        ease_seconds:int = 0,
        ease_mode:str = "inout",
        text:str = "",
        font_family:str = "Arial",
        text_align:list = [0,'center'],
        hov_background_clr:tuple = None,
        hov_border:list = None,
        active_background_clr:tuple = None,
        active_border:tuple = None,
        layer:int = 0,
        living:bool = True
    ):
        """
        ease_seconds = temps d'animation en secondes
        ease_mode = 'in','out','inout' -> mode d'animation
        hov_background_clr -> couleur en survol (hover)
        hov_border =  [bd_width:int,bd_clr:tuple,bd_padding:int] -> bordure en survol
        active_background_clr -> couleur que prend le fond du sprite quand il est cliqué (quand le clic et maintenu)
        active_border -> [bd_width:int,bd_clr:tuple,bd_padding:int], 

        Pour des informations sur d'autres attributs, se référer à la docu de Title.__init__()

        """
        super().__init__(
            winsize = winsize,
            loc = loc,
            background_clr = background_clr,
            size = size,
            border = border,
            font_clrs = font_clrs,
            font_size = font_size,
            text = text,
            font_family = font_family,
            text_align = text_align,
            layer = layer,
            living = living,
            parent_groups = parent_groups
        )
        self.ease_seconds = ease_seconds
        self.ease_mode = ease_mode
        self.clicking = False
        self.hoverable = True
        self.state = "base"

        self.reset_style(background_clr,border,hov_background_clr,hov_border,active_background_clr,active_border)
        

    def reset_style(
        self,
        background_clr = None,
        border = None,
        hov_background_clr = None,
        hov_border = None,
        active_background_clr = None,
        active_border = None,
        instant_change = True,
    ):
        """
        Redéfinition des attributs constants du bouton. N'affecte pas l'état actuel du bouton. Cette méthode est à utiliser pour changer le style que le bouton prend en fonction de ses états : 'base' est l'état que prend le bouton quand il ne reçoit aucune interaction. 'hover' est l'état que prend le bouton au survol. 'active' est l'état que prend le bouton quand il est cliqué (il écrase donc 'hover')
        """

        if background_clr != None:
            self.base_background_clr = background_clr[:]

        if border != None:
            self.base_border_width = border[0]
            self.base_border_clr = border[1][:]
            self.base_border_padding = border[2]
    
        if hov_background_clr != None:
            self.hov_background_clr = hov_background_clr[:]
        else:
            self.hov_background_clr = background_clr[:]

        if hov_border != None:
            self.hov_border_width = hov_border[0]
            self.hov_border_clr = hov_border[1][:]
            self.hov_border_padding = hov_border[2]
        else:
            self.hov_border_width = border[0]
            self.hov_border_clr = border[1][:]
            self.hov_border_padding = border[2] 


        if active_background_clr != None:
            self.active_background_clr = active_background_clr[:]
        else:
            self.active_background_clr = self.hov_background_clr[:]

        if active_border != None:
            self.active_border_width = active_border[0]
            self.active_border_clr = active_border[1][:]
            self.active_border_padding = active_border[2]
        else:
            self.active_border_width = self.hov_border_width
            self.active_border_clr = self.hov_border_clr
            self.active_border_padding = self.hov_border_padding

        if len(self.base_background_clr) != 4:
            self.base_background_clr = list(self.base_background_clr)
            self.base_background_clr.append(255)

        if len(self.base_border_clr) != 4:
            self.base_border_clr = list(self.base_border_clr)
            self.base_border_clr.append(255)

        if len(self.hov_background_clr) != 4:
            self.hov_background_clr = list(self.hov_background_clr)
            self.hov_background_clr.append(255)
        
        if len(self.hov_border_clr) != 4:
            self.hov_border_clr = list(self.hov_border_clr)
            self.hov_border_clr.append(255)
              
        if len(self.active_background_clr) != 4:
            self.active_background_clr = list(self.active_background_clr)
            self.active_background_clr.append(255)
        
        if len(self.active_border_clr) != 4:
            self.active_border_clr = list(self.active_border_clr)
            self.active_border_clr.append(255)

        if instant_change:
            self.background_clr = self.base_background_clr[:]
            self.border_width = self.base_border_width
            self.border_clr = self.base_border_clr[:]
            self.border_padding = self.base_border_padding
            self.calc_image()
            self.calc_rect()
        else:
            self.instant_change_background_clr([self.background_clr,self.base_background_clr],[self.ease_seconds],[self.ease_mode])
            self.instant_change_border_width([self.border_width,self.base_border_width],[self.ease_seconds],[self.ease_mode])
            self.instant_change_border_clr([self.border_clr,self.base_border_clr],[self.ease_seconds],[self.ease_mode])
            self.instant_change_border_padding([self.border_padding,self.base_border_padding],[self.ease_seconds],[self.ease_mode])
            
    
    def update(self,new_winsize,dt,fps,cursor):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize)

        self.state_changing(cursor)
        self.manage_frames(dt)


    def rescale(self,new_winsize):
        """actualisation des valeurs en cas de changement de résolution"""
        
        super().rescale(new_winsize)

        self.active_border_width = self.active_border_width * self.ratio
        self.active_border_padding = self.active_border_padding * self.ratio
        self.hov_border_padding = self.hov_border_padding * self.ratio
        self.hov_border_width = self.hov_border_width * self.ratio
        self.base_border_width *= self.ratio
        self.base_border_padding *= self.ratio


    def state_changing(self,cursor):
        """
        actualisation de l'état du sprite.
        """

        if self.rect.collidepoint(cursor) and self.hoverable:
            new_state = "hover"
        else:
            new_state = "base"
        if self.clicking:
            new_state = "active"

        if self.state != new_state:
            
            self.state = new_state
            if self.state == "hover":
                self.cur_background_clr_frames = Transition([self.background_clr,self.hov_background_clr],[self.ease_seconds],[self.ease_mode])
                self.background_clr_iter_nb = 1

                self.cur_border_width_frames = Transition([self.border_width,self.hov_border_width],[self.ease_seconds],[self.ease_mode])
                self.border_width_iter_nb = 1

                self.cur_border_clr_frames = Transition([self.border_clr,self.hov_border_clr],[self.ease_seconds],[self.ease_mode])
                self.border_clr_iter_nb = 1

                self.cur_border_padding_frames = Transition([self.border_padding,self.hov_border_padding],[self.ease_seconds],[self.ease_mode])
                self.border_padding_iter_nb = 1

            elif self.state == "base":
                self.cur_background_clr_frames = Transition([self.background_clr,self.base_background_clr],[self.ease_seconds],[self.ease_mode])
                self.background_clr_iter_nb = 1

                self.cur_border_width_frames = Transition([self.border_width,self.base_border_width],[self.ease_seconds],[self.ease_mode])
                self.border_width_iter_nb = 1

                self.cur_border_clr_frames = Transition([self.border_clr,self.base_border_clr],[self.ease_seconds],[self.ease_mode])
                self.border_clr_iter_nb = 1

                self.cur_border_padding_frames = Transition([self.border_padding,self.base_border_padding],[self.ease_seconds],[self.ease_mode])
                self.border_padding_iter_nb = 1

            elif self.state == "active":
                self.cur_background_clr_frames = Transition([self.background_clr,self.active_background_clr],[self.ease_seconds],[self.ease_mode])
                self.background_clr_iter_nb = 1

                self.cur_border_width_frames = Transition([self.border_width,self.active_border_width],[self.ease_seconds],[self.ease_mode])
                self.border_width_iter_nb = 1

                self.cur_border_clr_frames = Transition([self.border_clr,self.active_border_clr],[self.ease_seconds],[self.ease_mode])
                self.border_clr_iter_nb = 1

                self.cur_border_padding_frames = Transition([self.border_padding,self.active_border_padding],[self.ease_seconds],[self.ease_mode])
                self.border_padding_iter_nb = 1
        
    
    def set_clicking(self,state:bool):
        """
        méthode d'écriture de l'attribut 'clicking'
        """
        if self.hoverable:
            self.clicking = state

    
    def set_hoverable(self,state:bool):

        self.hoverable = state

