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
        degrees:float = 0,
        alpha:int = 255,
        layer: int = 0, 
        living: bool = True,
    ):

        super().__init__(name, winsize, scale_axis, loc, parent_groups, degrees, alpha, layer, living)

        self.resize_frames:Transition = None
        self.resize_iter_nb = 0

        self.translate_frames:Transition = None
        self.translate_iter_nb = 0

        self.alpha_frames:Transition = None
        self.alpha_iter_nb = 0

        self.degrees_frames:Transition = None
        self.degrees_iter_nb = 0



    def update(self,new_winsize,dt,fps,cursor):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)

        self.manage_states(dt)


    def manage_states(self,dt):

        calc_both1,calc_both2,calc_image1,calc_rect1 = [False]*4

        if self.resize_iter_nb > 0:
            self.resize_ratio, calc_both1, finish = self.resize_frames.change_index(dt,self.resize_ratio)
            if finish:
                self.resize_iter_nb -= 1
                if self.resize_iter_nb > 0:
                    self.resize_frames.reset_index()
        
        if self.translate_iter_nb > 0:
            self.pos, calc_rect1, finish = self.translate_frames.change_index(dt,self.pos)
            if finish:
                self.translate_iter_nb -= 1
                if self.translate_iter_nb > 0:
                    self.translate_frames.reset_index()

        if self.degrees_iter_nb > 0:
            self.degrees, calc_both2, finish = self.degrees_frames.change_index(dt,self.pos)
            if finish:
                self.degrees_iter_nb -= 1
                if self.degrees_iter_nb > 0:
                    self.degrees_frames.reset_index()

        if self.alpha_iter_nb > 0:
            self.alpha, calc_image1, finish = self.alpha_frames.change_index(dt,self.alpha)
            if finish:
                self.alpha_iter_nb -= 1
                if self.alpha_iter_nb > 0:
                    self.alpha_frames.reset_index()

        # calc requests handling

        if calc_both1 or calc_both2:
            self.calc_image()
            self.calc_rect()

        else:
            if calc_image1:
                self.calc_image()

            if calc_rect1:
                self.calc_rect()


    def rescale(self, new_winsize):

        super().rescale(new_winsize)
        if self.translate_frames:
            self.translate_frames.resize_extremums(self.ratio)


    def translate(self,positions:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        if positions[0] == "auto":
            positions[0] = self.pos[:]
        self.translate_iter_nb = iter_nb
        self.translate_frames = Transition(positions,ease_seconds,ease_modes)
    

    def resize(self,size_ratios:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        if size_ratios[0] == "auto":
            size_ratios[0] = self.resize_ratio
        self.resize_iter_nb = iter_nb
        self.resize_frames = Transition(size_ratios,ease_seconds,ease_modes)
        

    def rotate(self,degrees:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        if degrees[0] == "auto":
            degrees[0] = self.degrees
        self.degrees_iter_nb = iter_nb
        self.degrees_frames = Transition(degrees,ease_seconds,ease_modes)


    def change_alphas(self,alphas:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        if alphas[0] == "auto":
            alphas[0] = self.alpha
        self.alpha_iter_nb = iter_nb
        self.alpha_frames = Transition(alphas,ease_seconds,ease_modes)


    