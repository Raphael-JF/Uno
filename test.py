def instant_change_alpha(self,values:list,ease_seconds:list,ease_modes:list):

        self.cur_alpha_frames = Transition(values,ease_seconds,ease_modes)
        self.alpha_iter_nb = 1