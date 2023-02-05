import math
from classes.image import Image
from classes.transition import Transition

class Dynamic_image(Image):
    def __init__(
        self, 
        name: list[str], 
        winsize: list, 
        scale_axis: list, 
        loc: list, 
        parent_groups: list, 
        border: list = [-1,(0,0,0)], 
        layer: int = 0, 
        living: bool = True,
    ):

        super().__init__(name, winsize, scale_axis, loc, parent_groups, layer, living)

        self.resize_frames:Transition = None
        self.resize_iter_nb = 0

        self.translate_frames:Transition = None
        self.translate_iter_nb = 0


    def update(self,new_winsize,dt,fps,cursor):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)

        self.pos, recalc_needed, finish = self.translate_frames.change_index(dt,self.pos)
        if recalc_needed:
            self.calc_image()

        if finish:
            self.translate_frames.reset_index()


    def manage_states(self,dt):

        if self.resize_iter_nb > 0:
            self.resize_ratio, calc_image, finish = self.resize_frames.change_index(dt,self.resize_ratio)
            if calc_image:
                self.calc_image()
            if finish:
                self.resize_iter_nb -= 1
                if self.resize_iter_nb > 0:
                    self.resize_frames.reset_index()
                
        
        if self.translate_iter_nb > 0:
            self.pos, calc_rect, finish = self.translate_frames.change_index(dt,self.pos)
            if calc_rect and not calc_image:
                self.calc_rect()
            if finish:
                self.translate_iter_nb -= 1
                if self.translate_iter_nb > 0:
                    self.translate_frames.reset_index()


    def rescale(self, new_winsize):

        super().rescale(new_winsize)
        self.pos = [i*self.ratio for i in self.pos]
        if self.resize_frames:
            self.resize_frames.resize_extremums(self.ratio)


    def translate(self,positions:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        self.translate_iter_nb = iter_nb
        self.translate_frames = Transition(positions,ease_seconds,ease_modes)
    

    def resize(self,size_ratios:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        self.resize_iter_nb = iter_nb
        self.resize_frames = Transition(size_ratios,ease_seconds,ease_modes)
        


    