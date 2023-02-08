elif self.alpha_iter_nb == math.inf:
                self.cur_alpha_frames = Transition(positions,ease_seconds,ease_modes)
                self.alpha_iter_nb = iter_nb