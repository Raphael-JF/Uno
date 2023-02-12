import importlib
import pygame
import sys
import itertools

import elements.start_menu as start_menu
import elements.new_game as new_game
import elements.game_elements as game_elements
import assets

class Manager():
    """L'objet Manager gère le comportement du jeu à chaque image. Il redirige vers les instructions à exécuter en fonction des actions utilisateur."""

    def __init__(self):
        pygame.init()
        #variables
        self.fps = assets.START_GAME_FPS
        self.last_time = pygame.time.get_ticks()/1000
        self.state = "start_menu"
        self.screen_size=itertools.cycle([
            [960,540],
            
            [800,450],
            
            [1600,900],
            [1920,1080],
            
            
            
            [480,270],
            
            ])
        
        #initialisation
        self.current_winsize = next(self.screen_size) 
        self.win = pygame.display.set_mode(self.current_winsize)
        self.first_start = True
        self.clock = pygame.time.Clock()
        self.first_looping = True

    
    def tick(self):
        """
        Gestion du temps. A chaque tour de boucle, l'attribut dt est affecté et contient la durée en ms depuis la dernière exécution de cete méthode.
        """

        self.dt = (pygame.time.get_ticks()/1000 - self.last_time)
        self.last_time = pygame.time.get_ticks()/1000
        self.clock.tick(self.fps)
        

    def manage_state(self):
        """
        Redirection vers des instructions spécifiques en fonction de l'état actuel du jeu.
        """

        self.tick()
        if self.state == "start_menu":
            self.loop_start_menu()
        elif self.state == "multijoueur_selection_menu":
            self.loop_nouvelle_partie()
        elif self.state == "game":
            self.loop_game()
        

    def loop_start_menu(self):
        """
        Instructions du menu de lancement du jeu. action désigne l'action utilisateur (sur quel bouton il a apppuyé et dans quel menu doit il se rendre par conséquent)
        """
        
        action = start_menu.loop(self.win,self.current_winsize,self.dt,self.fps)
        if action == 1:
            pass
        if action == 2:
            importlib.reload(start_menu)
            self.state = "multijoueur_selection_menu"
        if action == 3:
            pass
        if action == 4:
            pass
        if action == 5:
            pygame.quit()
            sys.exit()

    def loop_nouvelle_partie(self):
        """
        Instructions du menu de création de nouvelle partie. action désigne l'action utilisateur (sur quel bouton il a apppuyé et dans quel menu doit il se rendre par conséquent)
        """

        action = new_game.loop(self.win,self.current_winsize,self.dt,self.fps)
        if type(action) is dict:
            self.game_info = action
            importlib.reload(new_game)
            self.state = "game"
            self.first_looping = True
        if action == 1:
            importlib.reload(start_menu)
            self.state = "start_menu"

    def loop_game(self):

        """
        Instructions du menu jeu. action désigne l'action utilisateur (sur quel bouton il a apppuyé et dans quel menu doit il se rendre par conséquent)
        """
        if self.first_looping:
            self.first_looping = False
            action = game_elements.loop(self.win,self.current_winsize,self.dt,self.fps,self.game_info)
        else:
            action = game_elements.loop(self.win,self.current_winsize,self.dt,self.fps)

        if action == 0:
            importlib.reload(game_elements)
            self.state = "start_menu"

        
