from classes.image import Image
from classes.transition import Transition

class Moving_image(Image):
    def __init__(
        self, 
        name: list[str], 
        winsize: list, 
        scale_axis: list, 
        loc: list, 
        alt_pos:list,
        parent_groups: list, 
        ease_seconds:list[float],
        ease_modes:list[str],
        border: list = [-1,(0,0,0)], 
        layer: int = 0, 
        living: bool = True,
    ):

        super().__init__(name, winsize, scale_axis, loc, parent_groups, border, layer, living)
        self.ease_seconds = ease_seconds
        self.ease_modes = ease_modes
        self.base_pos = self.pos[:]
        self.alt_pos = alt_pos
        self.pos_frames = Transition([self.pos,self.alt_pos,self.pos],self.ease_seconds,self.ease_modes)

    def update(self,new_winsize,dt,fps,cursor):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)

        self.pos, recalc_needed, finish = self.pos_frames.change_index(dt,self.pos)
        if recalc_needed:
            self.calc_image()

        if finish:
            self.pos_frames.reset_index()



    def rescale(self, new_winsize):
        super().rescale(new_winsize)
        self.alt_pos = [i*self.ratio for i in self.alt_pos]
        self.base_pos = [i*self.ratio for i in self.base_pos]