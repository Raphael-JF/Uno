from classes.card import Card
from classes.timer import Timer
import assets,pygame,random

class Deck():

    def __init__(self,winsize:list,deck_degrees:int|float,deck_midtop:list,deck_width:int,sprites_groups:list[pygame.sprite.LayeredUpdates],showed:bool,game):
        """
        self.card_size -> la taille souhaitée pour une carte, à l'échelle de winsize.
        deck_degrees -> l'angle prit par la carte centrale du deck.
        deck_midtop -> coordonnées du milieu du dessus de la zone du paquet.
        deck_width -> largeur de la zone du paquet. aucune carte ne fera dépasser au paquet cette largeur.
        discard_pile_midtop -> coordonnées du milieu du dessus de la pioche.
        sprites_groups -> groupes dans lesquels chaque carte sera ajoutée.
        """

        
        self.cartes = []
        self.deck_degrees = deck_degrees
        self.deck_width = deck_width
        self.deck_midtop = deck_midtop
        self.sprites_group = sprites_groups
        self.cards_to_add = []
        self.timers = []
        self.winsize = winsize
        self.showed = showed
        self.suggested_cards = []
        self.hovered_card_elevation = assets.HOVERED_CARD_ELEVATION_PX
        self.suggested_card_elevation = assets.SUGGESTED_CARD_ELEVATION_PX
        self.hovered_deck_elevation = assets.HOVERED_DECK_ELEVATION_PX
        self.card_size = assets.CARD_SIZE
        self.hovered_card = None
        self.played_card = None
        self.elevated = False
        self.resize_ratio = 1
        self.pile_color = None
        self.pile_value = None
        self.interactable = True
        self.game = game

    def set_infos(self,mode,name):

        self.player_mode = mode
        self.player_name = name


    def get_infos(self):

        return self.player_mode,self.player_name


    def update(self,new_winsize,dt,fps,cursor,hovered_card):

        if new_winsize != self.winsize:
            self.rescale(new_winsize)

        if self.showed and not self.get_clicking_card():
            last_hovered_card = self.get_hovered_card()
            for carte in self.cartes:
                if carte == hovered_card:
                    carte.set_hover(True)
                else:
                    carte.set_hover(False)

            if last_hovered_card != self.get_hovered_card():
                self.shift_cards(assets.CARDS_HOVER_SHIFT_ANIMATION_SECONDS,'out')

        
        for timer in self.timers:
            res,infos = timer.pass_time(dt)
            if res:
                self.timers.remove(timer)
                self.timer_handling(res,infos)

    

    def rescale(self,new_winsize):

        old_winsize = self.winsize[:]
        self.winsize = new_winsize
        self.ratio = self.winsize[0] / old_winsize[0]

        self.deck_midtop = [i*self.ratio for i in self.deck_midtop]
        self.deck_width *= self.ratio
        self.suggested_card_elevation *= self.ratio
        self.hovered_card_elevation *= self.ratio
        self.hovered_deck_elevation *= self.ratio
        self.card_size = [i*self.ratio for i in self.card_size]

        for carte in self.cartes:
            carte.rescale(new_winsize)


    def timer_handling(self,id,infos):

        if id == "draw_card":
            instant_sort = infos[0]
            carte = self.cards_to_add.pop(-1)
            self.timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS/2,"change_layers"))
            if self.showed:
                carte.add_timer(Timer(assets.CARDS_DRAWING_DELAY_BEFORE_FLIP,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
            self.cartes.append(carte)
            if instant_sort:
                self.arrange()
            self.rotate_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'out')
            self.shift_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'out')

        if id == "arrange":
            self.arrange()
            self.rotate_cards(assets.DECK_ROTATION_ANIMATION_SECONDS,'out')
            self.shift_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,'inout')

        if id == "change_layers":
            self.change_layers()


    def draw_cards(self,number_of_cards:int=1,instant_sort:bool=False):

        if number_of_cards<1:
            raise ValueError("number_of_cards must be => 1")

        x,y = assets.DRAW_PILE_CENTER
        w,h = assets.CARD_SIZE

        if self.deck_degrees == 0:
            placement_mode = "midtop"
            pos = [x, y - h/2]
        elif self.deck_degrees == 90:
            placement_mode = "midleft"
            pos = [x - w/2, y]
        elif self.deck_degrees == 180:
            placement_mode = "midbottom"
            pos = [x, y + h/2]
        elif self.deck_degrees == 270:
            placement_mode = "midright"
            pos = [x + w/2, y]

        layer = 10
        for i in range(number_of_cards):
            valeur = self.game.draw_card()
            carte = Card([pos,placement_mode],valeur,layer,self,self.resize_ratio)
            carte.rescale(self.winsize)
            for group in self.sprites_group:
                group.add(carte)
            layer += 1
            self.cards_to_add.append(carte)
            self.timers.append(Timer(i*assets.CARDS_DRAWING_DELAY_SECONDS,"draw_card",[instant_sort]))

        if not instant_sort:
            duree_avant_tri = number_of_cards*assets.CARDS_DRAWING_DELAY_SECONDS + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS
            self.timers.append(Timer(duree_avant_tri,'arrange'))


    def flip_cards(self):

        self.showed = not self.showed
        hovered_card = self.get_hovered_card()
        if hovered_card:
            hovered_card.set_hover(False)
        self.shift_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,'inout')
        for carte in self.cartes:
            carte.flip(assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out'])


    def arrange(self):

        self.cartes.sort(key = lambda card:card.get_value_priority())
        self.cartes.sort(key = lambda card:card.get_color_priority())
        self.timers.append(Timer(assets.CARDS_SORTING_ANIMATION_SECONDS/2,'change_layers'))
        

    
    def resize_cards(self,new_ratio:int|float,ease_seconds:int|float,ease_mode:str):

        if self.deck_degrees != 0:
            return
        
        self.resize_ratio = new_ratio
        self.shift_cards(ease_seconds,ease_mode)
        for carte in self.cartes:
            carte.resize(new_ratio,ease_seconds,ease_mode)
    

    def rotate_cards(self,ease_seconds:int|float,ease_mode:str):
        
        nb_cartes = len(self.cartes)
        if nb_cartes == 0:
            return

        part1 = []
        part2 = []
        for i in range(nb_cartes//2):
            part1.append(nb_cartes/2 - i)
            part2.append(-nb_cartes/2 + i)

        part2.reverse()

        if nb_cartes%2 == 0:
            cards_degrees = part1 + part2
        elif nb_cartes%2 == 1:
            cards_degrees = part1 + [0] + part2

        
        for i,(carte,degrees) in enumerate(zip(self.cartes,cards_degrees)):
            carte.rotate(self.deck_degrees + degrees, ease_seconds, ease_mode)
        
    
    def shift_cards(self,ease_seconds,ease_mode):

        nb_cartes = len(self.cartes)
        if nb_cartes == 0:
            return
        card_size = [i*self.resize_ratio for i in self.card_size]
        intervalle = self.deck_width*self.resize_ratio  - self.card_size[0]
        step = intervalle/nb_cartes
        if step > card_size[0]/4:
            step = card_size[0]/4

        if self.deck_degrees in [0,180]:
            if nb_cartes % 2 == 0:
                start = round(self.deck_midtop[0] - ((nb_cartes-1)/2)*step)
            else:
                start = round(self.deck_midtop[0] - (nb_cartes//2)*step)

            if self.deck_degrees == 0 and self.get_hovered_card():
                start -= round(card_size[0]/4)

            x=[]
            for i,carte in enumerate(self.cartes):
                x.append(round(start+step*i))
                if carte == self.get_hovered_card() and self.deck_degrees == 0:
                    start += round(card_size[0]/2)

            if self.deck_degrees == 180:
                y = [round(self.deck_midtop[1])]*nb_cartes
                x.reverse() 
            elif self.deck_degrees == 0:
                y = []
                for carte in self.cartes:

                    cur_y = self.deck_midtop[1]
                    if self.elevated:
                        cur_y -= self.hovered_deck_elevation
                        if carte in self.suggested_cards and not carte.get_hover():
                            cur_y -= self.suggested_card_elevation
                        elif carte.get_hover():
                            cur_y -= self.hovered_card_elevation

                    y.append(round(cur_y))

        else:
            if nb_cartes % 2 == 0:
                start = round(self.deck_midtop[1] - ((nb_cartes-1)/2)*step)
            else:
                start = round(self.deck_midtop[1] - (nb_cartes//2)*step)
            y=[]
            x = [round(self.deck_midtop[0])]*nb_cartes
            for i in range(nb_cartes):
                y.append(round(start+step*i))

            if self.deck_degrees == 90:
                y.reverse()  

        locs = list(zip(x,y))
        for card,loc in zip(self.cartes,locs):
            card.move_to(loc,ease_seconds,ease_mode)
            
    
    def change_layers(self):
        for i,carte in enumerate(self.cartes):
            # if carte.clicking:
            #     carte.set_clicking(False)
            carte.set_layer(10+i)
            for group in self.sprites_group:
                if type(group) is pygame.sprite.LayeredUpdates:
                    group.change_layer(carte,carte.get_layer())


    def get_hovered_card(self):

        for carte in self.cartes:
            if carte.get_hover():
                return carte
    

    def get_clicking_card(self):
        
        for carte in self.cartes:
            if carte.clicking:
                return carte


    def get_played_card(self):

        if self.played_card:
            played_card = self.played_card
            played_card.parent_deck = None
            self.played_card = None
            return played_card
        return None
        

    def get_cards(self):

        return self.cartes
    

    def set_cards(self,cards):

        self.cartes = cards[:]

        if self.deck_degrees == 0:
            for carte in self.cartes:
                carte.hover = False
                carte.clicking = False
                carte.set_parent_deck(self)
                carte.set_placement_mode("midtop")

        elif self.deck_degrees == 90:
            for carte in self.cartes:
                carte.hover = False
                carte.clicking = False
                carte.set_parent_deck(self)
                carte.set_placement_mode("midleft")

        elif self.deck_degrees == 180:
            for carte in self.cartes:
                carte.hover = False
                carte.clicking = False
                carte.set_parent_deck(self)
                carte.set_placement_mode("midbottom")

        elif self.deck_degrees == 270:
            for carte in self.cartes:
                carte.hover = False
                carte.clicking = False
                carte.set_parent_deck(self)
                carte.set_placement_mode("midright")

        self.set_pile_clrval(self.pile_color,self.pile_value)
        self.hovered_card = None
        self.played_card = None
        self.elevated = False
        self.change_layers()

    
    def play_card(self,card:Card):

        if card not in self.suggested_cards:
            return
        self.cartes.remove(card)
        self.shift_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,"inout")
        self.played_card = card


    def play_random_card(self):
        
        if len(self.suggested_cards) == 0:
            self.draw_cards(1,True)
        else:
            card = random.choice(self.suggested_cards)
            self.cartes.remove(card)
            self.played_card = card


    def elevate(self):

        self.elevated = True
        self.resize_cards(assets.CARDS_ELEVATION_SIZE_RATIO,assets.DECK_ELEVATION_ANIMATION_SECONDS,'out')


    def lower(self):
        
        self.elevated = False
        self.resize_cards(1,assets.DECK_ELEVATION_ANIMATION_SECONDS,'out')
        

    def add_card(self,card:Card):

        for group in self.sprites_group:
            if not group.has(card):
                group.add(card)
        self.cartes.append(card)
        card.set_parent_deck(self)


    def set_pile_clrval(self,color,value):

        self.pile_color = color
        self.pile_value = value
        self.suggested_cards = []
        for carte in self.cartes + self.cards_to_add:
            if carte.get_color() == color or carte.get_value() in ["wild", "4wild"] or carte.get_value() == value:
                self.suggested_cards.append(carte)
        self.shift_cards(assets.CARDS_HOVER_SHIFT_ANIMATION_SECONDS,'out')


    def set_interactable(self,state:bool):
        
        self.interactable = state