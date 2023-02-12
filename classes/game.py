import pygame,assets,random
from classes.card import Card
from classes.timer import Timer

class Game(pygame.sprite.Sprite):


    def __init__(self):

        super().__init__()

        self.winsize = assets.BASE_SIZE
        self.pos = assets.GAME_PILE_CENTER
        self.width = assets.GAME_PILE_SIZE[0]
        self.height = assets.GAME_PILE_SIZE[1]
        self.timers:list[Timer] = []
        self._layer = 2
        self.color = None
        self.value = None
        self.clockwise_direction = True
        self.draw_pile = assets.ALL_CARDS[:]

        self.calc_surf()


    def calc_surf(self):

        self.image = pygame.Surface([round(self.width),round(self.height)],pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = [round(i) for i in self.pos])


    def card_played(self,card:Card,ease_seconds,ease_mode):

        if card.value == "reverse":
            self.clockwise_direction = not self.clockwise_direction
    
        self.color = card.get_color()
        self.value = card.get_value()
        card.resize(1,ease_seconds,ease_mode)
        dest_midtop_x_extremums = [round(self.pos[0]*29/30),round(self.pos[0]*31/30)]
        dest_midtop_y_extremums = [round(self.pos[1]*29/30),round(self.pos[1]*31/30)]
        dest_midtop = [random.randint(*dest_midtop_x_extremums),random.randint(*dest_midtop_y_extremums)-card.height//2]
        degrees = round(random.uniform(-7.5,7.5),2)
        
        card.move_to(dest_midtop,ease_seconds,ease_mode)
        card.rotate(degrees,ease_seconds,ease_mode)
        self.timers.append(Timer(ease_seconds,'nullify',[card]))


    def card_centered(self,card:Card,ease_seconds,ease_mode):

        card.resize(1.2,ease_seconds,ease_mode)
        pos = self.pos[:]
        pos[1] -= card.height//2
        card.move_to(pos,ease_seconds,ease_mode)


    def update(self,new_winsize,dt,fps,cursor):

        if new_winsize != self.winsize:
            self.rescale(new_winsize)

        for timer in self.timers:
            res,infos = timer.pass_time(dt)
            if res:
                self.timers.remove(timer)
                self.timer_handling(res,infos)


    def rescale(self,new_winsize):

        old_winsize = self.winsize[:]
        self.winsize = new_winsize
        self.ratio = self.winsize[0] / old_winsize[0]

        self.pos = [i*self.ratio for i in self.pos]
        self.width *= self.ratio
        self.height *= self.ratio
        
        self.calc_surf()


    def timer_handling(self,id,infos = None):
        
        if id == "nullify":
            card_midtop = infos[0].pos
            surface, _ = infos[0].nullify()
            new_origin = self.rect.topleft
            relative_midtop = [card_midtop[0] - new_origin[0], card_midtop[1] - new_origin[1]]
            self.image.blit(surface,surface.get_rect(midtop=relative_midtop))
        
    
    def draw_card(self):

        res = self.draw_pile.pop(random.randint(0,len(self.draw_pile)-1))
        if len(self.draw_pile) == 0:
            self.draw_pile = assets.ALL_CARDS[:]
        return res


    def get_color(self):

        return self.color


    def get_value(self):

        return self.value


    def playable(self,card:Card):

        return card.value == self.value or card.color == self.color or card.value in ["wild", "4wild"]

    def pop_value(self):
        res = self.value
        self.value = None
        return res
