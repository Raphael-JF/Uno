import assets
from classes.title import Title
from classes.transition import Transition

class Player_name(Title):
    def __init__(
        self,
        winsize:list,
        loc:list,
        background_clr:tuple,
        font_clrs:list,
        font_size:int,
        border:list = [-1,(0,0,0),0,"inset"],
        size:list = [None,None],
        text:str = "",
        font_family:str = "Arial",
        text_align:list = [0,"center"],
        layer:int = 0,
        underline:bool = False
    ):
        super().__init__(winsize,loc,background_clr,font_clrs,font_size,border,size,text,font_family,text_align,layer,underline)

        self.base_width = self.width
        self.base_height = self.height
        self.base_font_size = self.font_size
        self.state = "base"
        self.size_frames = None


    def update(self,new_winsize,dt,fps,cursor):

        if self.winsize != new_winsize:
            self.rescale(new_winsize)

        if self.state == "highlight":
            [self.width,self.height], recalc_needed1 , _ = self.size_frames.change_index(dt,[self.width,self.height])

            self.font_size, recalc_needed2, finish = self.font_size_frames.change_index(dt,self.font_size)

            if recalc_needed1 or recalc_needed2:
                self.calc_title()
            
            if finish:
                self.size_frames.reset_index()
                self.font_size_frames.reset_index()


    def rescale(self,new_winsize):

        super().rescale(new_winsize)
        print(self.ratio)
        self.base_width *= self.ratio
        self.base_height *= self.ratio
        self.base_font_size *= self.ratio


    def set_highlight(self,highlight:bool=None):

        if highlight is None:
            if self.state == "base":
                self.state = "highlight"
                highlight = True
            else:
                self.state = "base"
                highlight = False

        if highlight:
            self.state = "highlight"
            self.size_frames = Transition([[self.width,self.height],[self.width*1.4,self.height*1.4],[self.width,self.height]],[assets.PLAYER_NAME_RESIZING_ANIMATION_SECONDS]*2,['linear','linear'])   
            self.font_size_frames = Transition([self.font_size,self.font_size*1.4,self.font_size],[assets.PLAYER_NAME_RESIZING_ANIMATION_SECONDS]*2,['linear','linear'])


        else:
            self.state = "base"
            self.width = self.base_width
            self.height = self.base_height
            self.font_size = self.base_font_size
            self.calc_title()
