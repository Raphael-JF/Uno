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
        alt_names:list[list[str]] = [],
        degrees:float = 0,
        alpha:int = 255,
        layer: int = 0, 
        living: bool = True,
    ):

        super().__init__(name, winsize, scale_axis, loc, parent_groups, alt_names, degrees, alpha, layer, living)


        self.cur_translate_frames:Transition = None
        self.translate_iter_nb = 0
        self.translate_frames_list:list[tuple[Transition,int]] = []
        self.inf_translate_frames:Transition = None

        self.cur_resize_frames:Transition = None
        self.resize_iter_nb = 0
        self.resize_frames_list:list[tuple[Transition,int]] = []
        self.inf_resize_frames:Transition = None
        
        self.cur_alpha_frames:Transition = None
        self.alpha_iter_nb = 0
        self.alpha_frames_list:list[tuple[Transition,int]] = []
        self.inf_alpha_frames:Transition = None

        self.cur_degrees_frames:Transition = None
        self.degrees_iter_nb = 0
        self.degrees_frames_list:list[tuple[Transition,int]] = []
        self.inf_degrees_frames:Transition = None



    def update(self,new_winsize,dt,fps,cursor):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)

        self.manage_states(dt)


    def manage_states(self,dt):

        calc_both1,calc_both2,calc_image1,calc_rect1 = [False]*4
        if self.translate_iter_nb > 0:
            self.pos, calc_rect1, finish = self.cur_translate_frames.change_index(dt,self.pos)
            if finish:
                if self.translate_iter_nb == math.inf and len(self.translate_frames_list) > 0:
                    
                    self.cur_translate_frames, self.translate_iter_nb = self.translate_frames_list.pop(0)
                self.translate_iter_nb -= 1
                if self.translate_iter_nb > 0:
                    self.cur_translate_frames.reset_index()
                elif len(self.translate_frames_list) > 0:
                    self.cur_translate_frames, self.translate_iter_nb = self.translate_frames_list.pop(0)
                elif self.inf_translate_frames:
                        self.cur_translate_frames = self.inf_translate_frames
                        self.translate_iter_nb = math.inf

        if self.resize_iter_nb > 0:
            self.resize_ratio, calc_both1, finish = self.cur_resize_frames.change_index(dt,self.pos)
            if finish:
                if self.resize_iter_nb == math.inf and len(self.resize_frames_list) > 0:
                    self.cur_resize_frames, self.resize_iter_nb = self.resize_frames_list.pop(0)
                self.resize_iter_nb -= 1
                if self.resize_iter_nb > 0:
                    self.cur_resize_frames.reset_index()
                elif len(self.resize_frames_list) > 0:
                    self.cur_resize_frames, self.resize_iter_nb = self.resize_frames_list.pop(0)
                elif self.inf_resize_frames:
                        self.cur_resize_frames = self.inf_resize_frames
                        self.resize_iter_nb = math.inf

        if self.degrees_iter_nb > 0:
            self.degrees, calc_both2, finish = self.cur_degrees_frames.change_index(dt,self.pos)
            if finish:
                self.degrees_iter_nb -= 1
                if self.degrees_iter_nb == math.inf and len(self.degrees_frames_list) > 0:
                    self.cur_degrees_frames, self.degrees_iter_nb = self.degrees_frames_list.pop(0)
                
                if self.degrees_iter_nb > 0:
                    self.cur_degrees_frames.reset_index()
                elif len(self.degrees_frames_list) > 0:
                    self.cur_degrees_frames, self.degrees_iter_nb = self.degrees_frames_list.pop(0)
                elif self.inf_degrees_frames:
                        self.cur_degrees_frames = self.inf_degrees_frames
                        self.degrees_iter_nb = math.inf

        if self.alpha_iter_nb > 0:
            self.alpha, calc_image1, finish = self.cur_alpha_frames.change_index(dt,self.pos)
            if finish:
                if self.alpha_iter_nb == math.inf and len(self.alpha_frames_list) > 0:
                    self.cur_alpha_frames, self.alpha_iter_nb = self.alpha_frames_list.pop(0)
                self.alpha_iter_nb -= 1
                if self.alpha_iter_nb > 0:
                    self.cur_alpha_frames.reset_index()
                elif len(self.alpha_frames_list) > 0:
                    self.cur_alpha_frames, self.alpha_iter_nb = self.alpha_frames_list.pop(0)
                elif self.inf_alpha_frames:
                        self.cur_alpha_frames = self.inf_alpha_frames
                        self.alpha_iter_nb = math.inf

        if self.alpha == 0 and self.alpha_iter_nb == 0:
            self.kill()

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
        if self.cur_translate_frames:
            self.cur_translate_frames.resize_extremums(self.ratio)
        if self.inf_translate_frames and self.inf_translate_frames is not self.cur_translate_frames:
            self.inf_translate_frames.resize_extremums(self.ratio)
        if len(self.translate_frames_list) > 0:
            for transition,_ in self.translate_frames_list:
                transition.resize_extremums(self.ratio)

    def translate(self,values:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):
        
        if iter_nb == math.inf:
            self.inf_translate_frames = Transition(values,ease_seconds,ease_modes)
            if self.cur_translate_frames is None or self.translate_iter_nb == 0:
                self.cur_translate_frames = self.inf_translate_frames
                self.translate_iter_nb = math.inf
        else:
            if self.cur_translate_frames is None or self.translate_iter_nb == 0:
                self.cur_translate_frames = Transition(values,ease_seconds,ease_modes)
                self.translate_iter_nb = iter_nb
            elif self.translate_iter_nb == math.inf:
                self.cur_translate_frames = Transition(values,ease_seconds,ease_modes)
                self.translate_iter_nb = iter_nb
            else:
                self.translate_frames_list.append((Transition(values,ease_seconds,ease_modes),iter_nb))
    

    def resize(self,values:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):
        
        if iter_nb == math.inf:
            self.inf_resize_frames = Transition(values,ease_seconds,ease_modes)
            if self.cur_resize_frames is None or self.resize_iter_nb == 0:
                self.cur_resize_frames = self.inf_resize_frames
                self.resize_iter_nb = math.inf
        else:
            if self.cur_resize_frames is None or self.resize_iter_nb == 0:
                self.cur_resize_frames = Transition(values,ease_seconds,ease_modes)
                self.resize_iter_nb = iter_nb
            elif self.resize_iter_nb == math.inf:
                self.cur_resize_frames = Transition(values,ease_seconds,ease_modes)
                self.resize_iter_nb = iter_nb
            else:
                self.resize_frames_list.append((Transition(values,ease_seconds,ease_modes),iter_nb))
        

    def rotate(self,values:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        if iter_nb == math.inf:
            self.inf_degrees_frames = Transition(values,ease_seconds,ease_modes)
            if self.cur_degrees_frames is None or self.degrees_iter_nb == 0:
                self.cur_degrees_frames = self.inf_degrees_frames
                self.degrees_iter_nb = math.inf
        else:
            if self.cur_degrees_frames is None or self.degrees_iter_nb == 0:
                self.cur_degrees_frames = Transition(values,ease_seconds,ease_modes)
                self.degrees_iter_nb = iter_nb
            elif self.degrees_iter_nb == math.inf:
                self.cur_degrees_frames = Transition(values,ease_seconds,ease_modes)
                self.degrees_iter_nb = iter_nb
            else:
                self.degrees_frames_list.append((Transition(values,ease_seconds,ease_modes),iter_nb))


    def change_alpha(self,values:list,ease_seconds:list,ease_modes:list,iter_nb:int = math.inf):

        if not self.alive():
            self.liven()

        if iter_nb == math.inf:
            self.inf_alpha_frames = Transition(values,ease_seconds,ease_modes)
            if self.cur_alpha_frames is None or self.alpha_iter_nb == 0:
                self.cur_alpha_frames = self.inf_alpha_frames
                self.alpha_iter_nb = math.inf
        else:
            if self.cur_alpha_frames is None or self.alpha_iter_nb == 0:
                self.cur_alpha_frames = Transition(values,ease_seconds,ease_modes)
                self.alpha_iter_nb = iter_nb
            elif self.alpha_iter_nb == math.inf:
                self.cur_alpha_frames = Transition(values,ease_seconds,ease_modes)
                self.alpha_iter_nb = iter_nb
            else:
                self.alpha_frames_list.append((Transition(values,ease_seconds,ease_modes),iter_nb))
