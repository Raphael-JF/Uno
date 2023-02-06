
from classes.transition import Transition
from classes.timer import Timer
import assets,os,pygame


class Card(pygame.sprite.Sprite):
    """
    L'objet Card gère la surface d'une carte, sa taille, ses animations (retournement, translation, rotation, homothétie)
    """

    def __init__(self,loc:list,id:str,layer:int,parent_deck,resize_ratio:float=1):
        """
        loc : [[x:int,y:int],mode:str] -> coordonnées et mode de placement ('center', 'topleft', 'topright', 'bottomleft','bottomright','midtop', midright', 'midbottom','midleft')
        winsize -> taille fenêtre pygame
        size = [width:int,height:int] -> taille de la carte
        id -> un code représentant la couleur et la valeur de la carte (voir assets.ALL_CARDS)
        layer -> couche sur laquelle afficher le sprite en partant de 1. Plus layer est élevée, plus la surface sera mise en avant.
        parent_deck -> l'objet Deck qui contient la carte
        """
        
        super().__init__()

        if len(id) == 2:
            self.color = id[0]
            self.value = id[1]

        elif id.endswith("+2"):
            self.color = id[0]
            self.value = "+2"
        
        elif id.endswith("skip"):
            self.color = id[0]
            self.value = "skip"

        elif id.endswith("reverse"):
            self.color = id[0]
            self.value = "reverse"

        elif id == "wild":
            self.color = None
            self.value = "wild"
        
        elif id == "4wild":
            self.color = None
            self.value = "4wild"
        
        else:
            raise ValueError(f"'{id}' n'est pas une valeur possible")

        self.id = id
        self.showed_face = pygame.image.load(os.path.join(os.getcwd(),'images','cartes',id+'.png'))
        self.hidden_face = pygame.image.load(os.path.join(os.getcwd(),'images','cartes','hidden.png'))
        self._layer = layer
        self.pos = loc[0]
        self.placement_mode = loc[1]
        self.winsize = assets.BASE_SIZE
        self.width,self.height = [i*resize_ratio for i in assets.CARD_SIZE]
        self.base_width,self.base_height = [i*resize_ratio for i in assets.CARD_SIZE]
        self.last_cursor_pos = []
        self.degrees = assets.DRAW_PILE_DEGREES
        self.resize_ratio = resize_ratio
        self.parent_deck = parent_deck

        self.center_pile_hitbox_center = assets.GAME_PILE_CENTER
        self.center_pile_hitbox_size = assets.GAME_PILE_HITBOX
        self.center_pile_hitbox_rect = pygame.Rect((0,0),self.center_pile_hitbox_size)
        self.center_pile_hitbox_rect.center = self.center_pile_hitbox_center

        self.face = "hidden"
        self.states = []
        self.resize_frames = None
        self.width_frames = None
        self.pos_frames = None
        self.degrees_frames = None
        self.timers = []
        self.hover = False
        self.clicking = False

        self.calc_card()
    

    def calc_card(self):
        """
        Recalcul de la surface du sprite, ainsi que son rectangle.
        """
        if self.face == "showed":
            self.image = pygame.transform.smoothscale(self.showed_face,(round(self.width*self.resize_ratio),round(self.height*self.resize_ratio)))
        else:
            self.image = pygame.transform.smoothscale(self.hidden_face,(round(self.width*self.resize_ratio),round(self.height*self.resize_ratio)))

        if self.degrees != 0:
            self.image = pygame.transform.rotate(self.image,round(self.degrees,1))

            
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
                


    def rescale(self,new_winsize):
        """actualisation des valeurs en cas de changement de résolution"""

        old_winsize = self.winsize[:]
        self.winsize = new_winsize
        self.ratio = self.winsize[0] / old_winsize[0]

        self.width = self.width*self.ratio
        self.height = self.height*self.ratio
        self.base_width = self.base_width*self.ratio
        self.base_height = self.base_height*self.ratio
        self.pos = [i*self.ratio for i in self.pos]

        self.center_pile_hitbox_center = [i*self.ratio for i in self.center_pile_hitbox_center]
        self.center_pile_hitbox_size = [i*self.ratio for i in self.center_pile_hitbox_size]
        self.center_pile_hitbox_rect = pygame.Rect((0,0),self.center_pile_hitbox_size)
        self.center_pile_hitbox_rect.center = self.center_pile_hitbox_center
        
        if self.width_frames:
            self.width_frames.resize_extremums(self.ratio)

        if self.pos_frames:
            self.pos_frames.resize_extremums(self.ratio)
        
        if self.degrees_frames:
            self.degrees_frames.resize_extremums(self.ratio)
        
        if self.resize_frames:
            self.resize_frames.resize_extremums(self.ratio)

        self.calc_card()



    def update(self,new_winsize,dt,fps,cursor):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if new_winsize != self.winsize:
            self.rescale(new_winsize)

        for timer in self.timers:
            res,infos = timer.pass_time(dt)
            if res:
                self.timers.remove(timer)
                self.timer_handling(res,infos)

        self.manage_states(dt,fps,cursor)

        if self.parent_deck is None:
            return
        if self.clicking and self.face == "showed" and self.parent_deck.interactable:
            self.pos = cursor[0], cursor[1] - self.height//2
            if self in self.parent_deck.suggested_cards:
                if self.center_pile_hitbox_rect.collidepoint(cursor) and not self.center_pile_hitbox_rect.collidepoint(self.last_cursor_pos):
                    self.resize(1,assets.CARD_RESIZE_ANIMATION_SECONDS,'inout')
                if not self.center_pile_hitbox_rect.collidepoint(cursor) and self.center_pile_hitbox_rect.collidepoint(self.last_cursor_pos):
                    self.resize(1.2,assets.CARD_RESIZE_ANIMATION_SECONDS,'inout')
            self.calc_card()


    def manage_states(self,dt,fps,cursor):

        if len(self.states) == 0:
            return

        if "flipping" in self.states:
            self.width, recalc_needed, finish = self.width_frames.change_index(dt,self.width)

            if recalc_needed:
                self.calc_card()
            
            if finish:
                self.states.remove("flipping")
        
        if "moving" in self.states:
            self.pos, recalc_needed ,finish = self.pos_frames.change_index(dt,self.pos)
            if recalc_needed:
                self.calc_card()
            
            if finish:
                self.states.remove("moving")

        if "rotating" in self.states:

            self.degrees, recalc_needed, finish = self.degrees_frames.change_index(dt,self.degrees)

            if recalc_needed:
                self.calc_card()
            
            if finish:
                self.states.remove("rotating")

        if "resizing" in self.states:
            
            self.resize_ratio, recalc_needed, finish = self.resize_frames.change_index(dt,self.resize_ratio)

            if recalc_needed:
                self.calc_card()
            
            if finish:
                if "resizing" in self.states:
                    self.states.remove("resizing")
        self.last_cursor_pos = cursor


    def resize(self,new_ratio:int|float,ease_seconds:int|float,ease_mode:str):
        """initialisation d'un changement progressif de taille selon un ratio"""

        if new_ratio <= 0:
            raise ValueError("ratio must be > 0")

        self.resize_frames = Transition([self.resize_ratio,new_ratio],[ease_seconds],[ease_mode])

        if "resizing" not in self.states:
            self.states.append("resizing")
        

    def timer_handling(self,id,infos):
        if id == "change_face":
            self.change_face()
        elif id == "flip":
            self.flip(*infos)


    def set_wild_color(self,color:str):

        if self.value in ["wild","4wild"]:
            self.color = color
            self.showed_face = pygame.image.load(os.path.join(os.getcwd(),'images','cartes',color+self.value+'.png'))
            self.calc_card()


    def change_face(self):

        if self.face == "showed":
            self.face = "hidden"

        else:
            self.face = "showed"


    def move_to(self,pos:list,ease_seconds:int|float,ease_mode:str):
        
        if ease_seconds == 0:
            self.pos = pos
            self.calc_card()
            if "moving" in self.states:
                self.states.remove("moving")
            return
        
        if "moving" not in self.states:
            self.states.append("moving")
        self.pos_frames = Transition([self.pos,pos],[ease_seconds],[ease_mode])


    def move_a_to_b(self,pos_a:list,pos_b:list,ease_seconds:int|float,ease_mode:str):

        if "moving" not in self.states:
            self.states.append("moving")
        self.pos_frames = Transition([pos_a,pos_b],[ease_seconds],[ease_mode])


    def flip(self,ease_seconds:list[int|float],ease_modes:list[str]):

        if len(ease_seconds) != 2 != len(ease_modes):
            raise ValueError("ease_seconds and ease_modes must contain 2 values to flip")
            
        self.states.append("flipping")
        self.width_frames = Transition([self.width,0,self.base_width],[i for i in ease_seconds], ease_modes)

        self.timers.append(Timer(ease_seconds[0],'change_face'))


    def rotate(self,degrees:int|float,ease_seconds:int|float,ease_mode:str):
        
        if ease_seconds == 0:
            self.degrees = degrees
            self.calc_card()
            if "rotating" in self.states:
                self.states.remove("rotating")
            return

        if "rotating" not in self.states:
            self.states.append("rotating")
        self.degrees_frames = Transition([self.degrees,degrees],[ease_seconds],[ease_mode])

    
    def add_timer(self,timer:Timer):
        self.timers.append(timer)


    def set_layer(self,layer):
        self._layer = layer

    
    def get_value(self):

        return self.value


    def get_color(self):

        return self.color
    

    def get_id(self):
        return self.id

    def get_layer(self):
        return self._layer


    def get_value_priority(self):

        if self.value == "4wild":
            return 0
        if self.value == "wild":
            return 1
        if self.value in [str(i) for i in range(10)]:
            return int(self.value)
        if self.value == "+2":
            return 10
        if self.value == "skip":
            return 11
        if self.value == "reverse":
            return 12

    def get_color_priority(self):

        if self.color == None:
            return 0
        if self.color == "r":
            return 1
        if self.color == "j":
            return 2
        if self.color == "b":
            return 3
        if self.color == "v":
            return 4

    def get_hover(self):

        return self.hover


    def set_hover(self,hover):

        self.hover = hover


    def set_placement_mode(self,new_mode):

        self.placement_mode = new_mode


    def set_parent_deck(self,new_deck):

        self.parent_deck = new_deck


    def get_clicking(self):

        return self.clicking


    def set_clicking(self,clicking):

        if self.face == "showed" and self.parent_deck and "flipping" not in self.states :
            self.clicking = clicking

        if self.clicking and "flipping" not in self.states:
            for group in self.groups():
                if type(group) is pygame.sprite.LayeredUpdates:
                    group.change_layer(self,100)
            self.states = []
            self.rotate(0,assets.DECK_ROTATION_ANIMATION_SECONDS,"inout")

        if not self.clicking and self.parent_deck:
            if self.center_pile_hitbox_rect.collidepoint(self.last_cursor_pos):
                self.parent_deck.play_card(self)
            self.hover = False
            self.parent_deck.change_layers()
            self.parent_deck.shift_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'out')
            self.parent_deck.rotate_cards(assets.DECK_ROTATION_ANIMATION_SECONDS,'out')

    
    def nullify(self):
        
        surf = self.image
        rect = self.rect
        self.kill()
        del(self)
        return surf,rect


    def get_face(self):
        return self.face

