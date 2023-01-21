from classes.button import Button
from assets import INPUT_FIELD_DASH_DELAY as DASH_DELAY,KEYPRESS_SPAM_DELAY,CHARS_SPAM_DELAY
import pygame

class Input_field(Button):
    """
    Héritant de l'objet Button, Input_field implémente la possibilité pour l'utilisateur de taper du texte dans un champ, de le supprimer et de pouvoir spammer les caractères en restant appuyé (commmmmmmmmmme ça)
    """

    def __init__(
        self,
        winsize:list,
        loc:list,
        font_size:int,
        font_family:str = "Arial",
        font_clr:tuple = (0,0,0),
        background_clr:tuple = (255,255,255),
        border:list = [0,(0,0,0),0,"inset"],
        size:list = [None,None],
        text:str = "",
        text_align = [0,'center'],
        layer:int = 0,
        hov_background_clr:tuple = None,
        hov_border:tuple = None,
        active_background_clr:tuple = None,
        active_border:tuple = None,
        ease_seconds:float = 0,
        ease_mode:str = "inout"
    ):
        """
        Pour des informations sur les  attributs, se référer à la docu de Button.__init__()
        """
        
    
        if len(text.split("\n")) > 1:
            raise ValueError("text must be 1 line only (no \\n)")

        super().__init__(
            winsize = winsize,
            loc = loc,
            background_clr = background_clr,
            border = border,
            font_clrs = [font_clr],
            font_size = font_size,
            size = size,
            ease_seconds = ease_seconds,
            ease_mode = ease_mode,
            text = text,
            text_align = text_align,
            font_family = font_family,
            hov_background_clr = hov_background_clr,
            hov_border = hov_border,
            layer = layer
        )

        if active_background_clr == None:
            self.active_background_clr = self.base_background_clr[:]
        else:
            self.active_background_clr = active_background_clr

        if active_border == None:
            self.active_border_width = self.base_border_width
            self.active_border_clr = self.base_border_clr[:]
            self.active_border_padding = self.base_border_padding
        else:
            self.active_border_width = active_border[0]
            self.active_border_clr = active_border[1]
            self.active_border_padding = active_border[2]
        
        if len(self.active_background_clr) != 4:
            self.active_background_clr = list(self.active_background_clr)
            self.active_background_clr.append(255)
        
        if len(self.active_border_clr) != 4:
            self.active_border_clr = list(self.active_border_clr)
            self.active_border_clr.append(255)

        self.dash_delay = DASH_DELAY
        self.dash = False
        self.focus = False
        self.base_text = text
        self.cur_keypress = None
        self.keypress_spam_delay = KEYPRESS_SPAM_DELAY
        self.char_spam_delay = CHARS_SPAM_DELAY
        self.text_max_size = False
    

    def update(self,new_winsize,dt,fps,cursor):
        if self.winsize != new_winsize:
            self.rescale(new_winsize = new_winsize)

        if self.focus:
            self.dash_update(dt)

        self.text_gestion(dt)
        self.state_changing(cursor)

        recalc_needed = self.frame_managing(dt)
        
        if recalc_needed:
            self.calc_title()
        
        
    def rescale(self, new_winsize):
        super().rescale(new_winsize)

    
    def state_changing(self, cursor):
        if self.rect.collidepoint(cursor):
            self.state = "hover"
        else:
            self.state = "base"

        if self.clicking or self.focus:
            self.state = "active"
        

    def frame_managing(self, dt):

        if self.state == "active":
            if self.last_frame_state != "active":
                self.last_frame_state = "active"
                self.background_clr_frames.set_step_values([self.cur_background_clr,self.active_background_clr])
                self.border_clr_frames.set_step_values([self.cur_border_clr,self.active_border_clr])
                self.border_padding_frames.set_step_values([self.cur_border_padding,self.active_border_padding])
                self.border_width_frames.set_step_values([self.cur_border_width,self.active_border_width])

        if self.state == "hover":
            if self.last_frame_state != "hover":
                self.last_frame_state = "hover"
                self.background_clr_frames.set_step_values([self.cur_background_clr,self.hov_background_clr])
                self.border_clr_frames.set_step_values([self.cur_border_clr,self.hov_border_clr])
                self.border_padding_frames.set_step_values([self.cur_border_padding,self.hov_border_padding])
                self.border_width_frames.set_step_values([self.cur_border_width,self.hov_border_width])
        
        if self.state == "base":
            if self.last_frame_state != "base":
                self.last_frame_state = "base"
                self.background_clr_frames.set_step_values([self.cur_background_clr,self.base_background_clr])
                self.border_clr_frames.set_step_values([self.cur_border_clr,self.base_border_clr])
                self.border_padding_frames.set_step_values([self.cur_border_padding,self.base_border_padding])
                self.border_width_frames.set_step_values([self.cur_border_width,self.base_border_width])


        if self.last_state != self.state or not self.animation_finish:

            recalc_needed = False
            self.animation_finish = True

            self.cur_background_clr,rec_need,finish = self.background_clr_frames.change_index(dt,self.cur_background_clr)
            recalc_needed = recalc_needed or rec_need
            self.animation_finish = self.animation_finish and finish

            self.cur_border_clr,rec_need,finish = self.border_clr_frames.change_index(dt,self.cur_border_clr)
            recalc_needed = recalc_needed or rec_need
            self.animation_finish = self.animation_finish and finish

            self.cur_border_padding,rec_need,finish = self.border_padding_frames.change_index(dt,self.cur_border_padding)
            recalc_needed = recalc_needed or rec_need
            self.animation_finish = self.animation_finish and finish

            self.cur_border_width,rec_need,finish = self.border_width_frames.change_index(dt,self.cur_border_width)
            recalc_needed = recalc_needed or rec_need
            self.animation_finish = self.animation_finish and finish

            if self.animation_finish:
                self.last_state = self.state
        
            return recalc_needed
        return False


    def clicked(self):

        self.focus = True
        self.dash = True
        self.dash_delay = DASH_DELAY
    

    def blured(self):

        self.focus = False
        self.dash = False
        self.dash_delay = DASH_DELAY
        self.char_spam_delay = CHARS_SPAM_DELAY
        self.cur_keypress = None
        self.text_max_size = False


    def reset_attributes(self):

        super().reset_attributes()
        self.blured()
        self.texte = self.base_text


    def dash_update(self,dt):

        self.dash_delay -= dt

        if self.dash_delay<0:
            self.dash_delay = DASH_DELAY
            self.dash = not(self.dash)

    
    def text_gestion(self,dt = None):

        if dt != None and self.cur_keypress != None:
            self.keypress_spam_delay -= dt
        
        if self.keypress_spam_delay < 0 and self.cur_keypress != None:
            self.char_spam_delay -= dt

            if self.char_spam_delay < 0:
                self.char_spam_delay = CHARS_SPAM_DELAY

                if self.cur_keypress.key == pygame.K_BACKSPACE:
                    self.texte = self.texte[:-1]
                    self.text_max_size = False

                else:
                    self.texte += self.cur_keypress.unicode
                    
                    if self.calc_title(self.texte + '    ') == "text is too wide":
                        self.text_max_size = True

                    if self.calc_title(self.texte + '   ') == "text is too wide":
                        self.texte = self.texte[:-1]
                        self.text_max_size = True



        if not self.dash or self.text_max_size:
            self.calc_title(self.texte)
        else:
            self.calc_title(self.texte+'_')


    def get_focus(self):

        return self.focus


    def receive_keydown(self,event):

        if event.key in (pygame.K_KP_ENTER,pygame.K_RETURN):
            self.blured()

        elif event.key == pygame.K_ESCAPE:
            self.texte = ""

        elif event.key == pygame.K_BACKSPACE:
            self.texte = self.texte[:-1]
            self.cur_keypress = event
            self.calc_title()
            self.text_max_size = False
            
            if self.cur_keypress == None:
                self.cur_keypress = event

        else:
            self.texte += event.unicode
            
            if self.calc_title(self.texte+'    ') == "text is too wide" :
                self.text_max_size = True

            if self.calc_title(self.texte+'   ') == "text is too wide" :
                self.texte = self.texte[:-1]

            if self.cur_keypress == None:
                self.cur_keypress = event
                


    def receive_keyup(self,event):

        if self.cur_keypress != None:

            if event.key == self.cur_keypress.key:
                self.cur_keypress = None
                self.keypress_spam_delay = KEYPRESS_SPAM_DELAY
        

    def get_text(self):
        return self.texte