import pygame,assets,math,random
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

        self.calc_surf()


    def calc_surf(self):

        self.image = pygame.Surface([round(self.width),round(self.height)],pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = [round(i) for i in self.pos])


    def card_played(self,card:Card,ease_seconds,ease_mode):

        dest_midtop_x_extremums = [round(self.pos[0]*29/30),round(self.pos[0]*31/30)]
        dest_midtop_y_extremums = [round(self.pos[1]*29/30),round(self.pos[1]*31/30)]
        dest_midtop = [random.randint(*dest_midtop_x_extremums),random.randint(*dest_midtop_y_extremums)-card.height//2]
        degrees = round(random.uniform(-7.5,7.5),2)
        dep_midtop = list(card.pos)
        dep_midtop[1] -= card.height//2
        
        card.move_a_to_b(dep_midtop,dest_midtop,ease_seconds,ease_mode)
        card.rotate(degrees,ease_seconds,ease_mode)
        self.timers.append(Timer(ease_seconds,'nullify',[card]))

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
            surface, rect = infos[0].nullify()
            new_origin = self.rect.topleft
            
            relative_midtop = [card_midtop[0] - new_origin[0], card_midtop[1] - new_origin[1]]
            self.image.blit(surface,surface.get_rect(midtop=relative_midtop))
        
        