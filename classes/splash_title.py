from classes.timer import Timer
from classes.box import Box
from classes.transition import Transition
import pygame,os

class Splash_title(Box):

    def __init__(
        self, 
        winsize: list, 
        text_center:list,
        background_clr: tuple,
        font_clrs: list,
        font_size: int,
        start_y:int,
        parent_groups:list,
        text_alpha:int = 255,
        appearing_ease:list[int,str] = [0,'linear'],
        text: str = "",
        font_family: str = "Arial", 
        layer: int = 0, 
        underline: bool = False,
        dismiss_ease:list[int,str] = [0,'linear'],
        seconds_before_dismiss:int|float = 0,
        living:bool = True
    ):

        super().__init__(winsize=winsize,size=winsize,loc=[[0,0],"topleft"],background_clr=background_clr,layer=layer,parent_groups=parent_groups,living = living)

        self.appearing_seconds, self.appearing_mode = appearing_ease
        self.dismiss_seconds, self.dismiss_mode = dismiss_ease
        self.seconds_before_dismiss = seconds_before_dismiss
        self.start_y = start_y
        
        self.text_alpha = text_alpha
        self.start_text_alpha = text_alpha
        self.start_background_alpha = background_clr[-1]

        self.underline = underline
        self.font_family = font_family
        self.texte = text
        self.font_size = font_size
        self.font_clrs = font_clrs
        self.cur_text_center = text_center[:]
        self.base_text_center = text_center[:]

        self.state = "hidden"
        self.timers = []

        self.background_alpha_frames = Transition([0,self.start_background_alpha],[self.appearing_seconds],[self.appearing_mode])
        self.text_alpha_frames = Transition([0,self.start_text_alpha],[self.appearing_seconds],[self.appearing_mode])
        self.y_frames = Transition([self.start_y,self.rect.centery],[self.appearing_seconds],[self.appearing_mode])

        self.calc_text()
        

    def calc_pos(self):
        """
        Recalcul du rectangle du sprite
        """

        self.text_surface.set_alpha(round(self.text_alpha))
        super().calc_box()
        cur_text_center = [round(i) for i in self.cur_text_center]
        text_rect = self.text_surface.get_rect(center=cur_text_center)
        self.image.blit(self.text_surface,text_rect)
        


    def calc_text(self):
        """
        Recalcul de la surface du sprite
        """

        if self.font_family.endswith(".ttf"):
            font = pygame.font.SysFont(name=os.path.join(os.getcwd(),"fonts",self.font_family),size=round(self.font_size))
        else:
            font = pygame.font.SysFont(name=self.font_family,size=round(self.font_size))

        font.set_underline(self.underline)

        textes = self.texte.split("\n")
        
        texte_surfaces = []
        for i in range(len(textes)):
            font_clr = [round(j) for j in self.font_clrs[i]]
            texte_surfaces.append(font.render(textes[i],True,font_clr))

        self.text_height = sum([i.get_height() for i in texte_surfaces])
        self.text_width = max([i.get_width() for i in texte_surfaces])
        self.text_surface = pygame.Surface([
            self.text_width,self.text_height],pygame.SRCALPHA)

        count_height = 0
        for i in texte_surfaces:
            self.text_surface.blit(i,i.get_rect(midtop=(self.text_width//2,count_height)))
            count_height += i.get_height()


    def update(self,new_winsize, dt, fps, **args):

        if self.winsize != new_winsize:
            self.rescale(new_winsize)
            
        for timer in self.timers:
            res,infos = timer.pass_time(dt)
            if res:
                self.timers.remove(timer)
                self.timer_handling(res,infos)
        
        self.manage_states(dt,fps)
            
                
    def timer_handling(self,res,infos = None):

        if res == "dismiss":
            self.dismiss()


    def rescale(self, new_winsize):

        super().rescale(new_winsize) 

        self.font_size *= self.ratio
        self.cur_text_center = [i*self.ratio for i in self.cur_text_center]
        self.base_text_center = [i*self.ratio for i in self.base_text_center]
        self.start_y = self.start_y*self.ratio
        self.y_frames.resize_extremums(self.ratio)
        self.calc_pos()
        self.calc_text()
        
        

    def manage_states(self,dt,fps):

        if self.state == "appearing":

            self.cur_text_center[1], _, _ = self.y_frames.change_index(dt,self.cur_text_center[1])
            self.cur_background_clr[-1], _ , _ = self.background_alpha_frames.change_index(dt,self.cur_background_clr[-1])
            self.text_alpha, recalc_needed, finish = self.text_alpha_frames.change_index(dt,self.text_alpha)

            if recalc_needed:
                self.calc_pos()

            if finish:
                self.state = "showed"
                if self.seconds_before_dismiss > 0:
                    self.timers.append(Timer(self.seconds_before_dismiss,"dismiss"))
            
        elif self.state == "dismiss":

            self.cur_text_center[1], _ , _ = self.y_frames.change_index(dt,self.cur_text_center[1])
            self.cur_background_clr[-1], _ , _ = self.background_alpha_frames.change_index(dt,self.cur_background_clr[-1])
            self.text_alpha, recalc_needed, finish = self.text_alpha_frames.change_index(dt,self.text_alpha)

            if recalc_needed :
                self.calc_pos()

            if finish:
                self.state = "hidden"
                self.kill()

    def appear(self):

        if not self.alive():
            self.liven()

        self.state = "appearing"
        self.background_alpha_frames = Transition([0,self.start_background_alpha],[self.appearing_seconds],[self.appearing_mode])
        self.text_alpha_frames = Transition([0,self.start_text_alpha],[self.appearing_seconds],[self.appearing_mode])
        self.y_frames = Transition([self.start_y,self.base_text_center[1]],[self.appearing_seconds],[self.appearing_mode])
    

    def dismiss(self):

        self.state = "dismiss"
        self.background_alpha_frames = Transition([self.cur_background_clr[-1],0],[self.appearing_seconds],[self.appearing_mode])
        self.text_alpha_frames = Transition([self.text_alpha,0],[self.dismiss_seconds],[self.dismiss_mode])
        self.y_frames = Transition([self.cur_text_center[1],self.start_y],[self.dismiss_seconds],[self.dismiss_mode])
        

    def change_text(self,new_text):
        self.texte = new_text
        self.calc_pos()
        self.calc_text()

    
    def get_state(self):
        return self.state