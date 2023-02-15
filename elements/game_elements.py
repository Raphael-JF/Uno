"""
Ce module contient les éléments et widgets du menu jeu. Il contient aussi le code de gestion utilisateur pour ce menu.
"""

import random
import pygame,assets,sys
from classes.timer import Timer
from classes.splash_title import Splash_title
from classes.box import Box
from classes.image import Image
from classes.player_name import Player_name
from classes.deck import Deck
from classes.card import Card
from classes.game import Game
from classes.button import Button
from classes.title import Title
from classes.dynamic_image import Dynamic_image
pygame.init()

all_group = pygame.sprite.Group()
buttons_group = pygame.sprite.LayeredUpdates()
to_draw_group = pygame.sprite.LayeredUpdates()
cards_group = pygame.sprite.LayeredUpdates()

pause_all_group = pygame.sprite.Group()
pause_buttons_group = pygame.sprite.LayeredUpdates()


background = Box(
    winsize = assets.BASE_SIZE,
    size = [802,452],
    loc = [[0,0],"topleft"],
    background_clr=(191, 23, 29),
    border = [-1,(0,0,0),0,"inset"],
    layer=1,
    parent_groups = [all_group,to_draw_group]
)

pause_background = Box(
    winsize = assets.BASE_SIZE,
    size = [800,450],
    loc = [[0,0],"topleft"],
    background_clr=(0, 0, 0, 175),
    border = [-1,(0,0,0),0,"inset"],
    layer=6000,
    parent_groups = [all_group,to_draw_group,pause_all_group],
    living = False
)

pause_button = Button(
    winsize=assets.BASE_SIZE,
    loc = [(795,5),"topright"],
    background_clr = (250,250,250),
    size = [75,34],
    border=[2,(25,25,25),2,"inset"],
    text = "Pause",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 6,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = True
)


pioche = Image(
    name=["cartes","hidden.png"],
    winsize=assets.BASE_SIZE,
    scale_axis=['y',assets.CARD_SIZE[1]],
    loc=[assets.DRAW_PILE_CENTER,"center"],
    layer=9,
    parent_groups = [all_group,to_draw_group]
)

pioche_button = Button(
    winsize = assets.BASE_SIZE,
    loc = [assets.DRAW_PILE_CENTER,"center"],
    size = assets.CARD_SIZE,
    border = [-1,(0,0,0,0),0,'inset'],
    background_clr = (0,0,0,0),
    font_clrs = [(25,25,25)],
    font_family = "RopaSans-Regular.ttf",
    layer = 5001,
    ease_mode = "inout",
    ease_seconds= 0.3,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

pioche_fleche = Dynamic_image(
    name=["arrow.png"],
    winsize=assets.BASE_SIZE,
    scale_axis=['x',44],
    loc=[[220,85],"midleft"],
    layer=9,
    parent_groups = [all_group,to_draw_group],
    living = False
)
pioche_fleche.translate([[161,assets.DRAW_PILE_CENTER[1]],[191,assets.DRAW_PILE_CENTER[1]],[161,assets.DRAW_PILE_CENTER[1]]],[assets.DRAW_PILE_ARROW_ANIMATION_SECONDS]*2,['linear','linear'])

fleche4 = Dynamic_image(
    name=["4arrows_clockwise.png"],
    alt_names = [["4arrows_not_clockwise.png"]],
    winsize=assets.BASE_SIZE,
    scale_axis=['x',73],
    loc=[[66,384],"center"],
    layer=10,
    parent_groups = [all_group,to_draw_group],
    living = True
)
fleche4.rotate([360,180,180,0,0],[2,0.5,2,0.5],["inout","linear","inout","linear","inout"])

dark_background100 = Box(
    winsize = assets.BASE_SIZE,
    size = [800,450],
    loc = [[0,0],"topleft"],
    background_clr=(0, 0, 0, 100),
    border = [-1,(0,0,0),0,"inset"],
    layer=5000,
    parent_groups = [all_group,to_draw_group],
    living = False
)

dark_background205 = Box(
    winsize = assets.BASE_SIZE,
    size = [800,450],
    loc = [[0,0],"topleft"],
    background_clr=(0, 0, 0, 205),
    border = [-1,(0,0,0),0,"inset"],
    layer=4999,
    parent_groups = [all_group,to_draw_group],
    living = False
)

dark_area = Dynamic_image(
    name=["dark_area.png"],
    winsize=assets.BASE_SIZE,
    scale_axis=['x',550],
    alpha = 255,
    loc=[assets.GAME_PILE_CENTER,"center"],
    layer=5000,
    parent_groups = [all_group,to_draw_group],
    living = False
)

skip_logo = Dynamic_image(
    name=["skip_logo.png"],
    winsize=assets.BASE_SIZE,
    scale_axis=['x',125],
    alpha = 255,
    loc=[assets.GAME_PILE_CENTER,"center"],
    layer=5001,
    parent_groups = [all_group,to_draw_group],
    living = False
)


splash_title1 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,175],"center"],
    background_clr = [0,0,0,0],
    font_clrs = [[250,250,250]],
    font_size = 64,
    size = [400,150],
    text = "Au tour de",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    living = False,
    parent_groups = [all_group,to_draw_group]
)

splash_title2 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,225],"center"],
    background_clr = [0,0,0,0],
    font_clrs = [[250,250,250]],
    font_size = 64,
    size = [400,150],
    text = "Joueur 1",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    living = False,
    parent_groups = [all_group,to_draw_group]
)

splash_title3 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,400],"center"],
    background_clr = [0,0,0,0],
    font_clrs = [[250,250,250]],
    font_size = 30,
    size = [500,100],
    text = "Appuyez sur [Espace] pour jouer",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    living = False,
    parent_groups = [all_group,to_draw_group]
)

pseudo1 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,310],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    size = [133,27],
    text = "Joueur 1",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    parent_groups = [all_group,to_draw_group]
)

pseudo2 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[570,200],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    size = [133,27],
    text = "Joueur 2",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    parent_groups = [all_group,to_draw_group]
)

pseudo3 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,90],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    size = [133,27],
    text = "Joueur 3",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    parent_groups = [all_group,to_draw_group]
)

pseudo4 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[230,200],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    size = [133,27],
    text = "Joueur 4",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    parent_groups = [all_group,to_draw_group]
)
pseudos = [pseudo1,pseudo2,pseudo3,pseudo4]

yellow_button = Button(
    winsize = assets.BASE_SIZE,
    loc = ((395,230),"topright"),
    size = (115,115),
    border = [-1,(255, 244, 2),0,'outset'],
    hov_border = [5, (217,210,2),0],
    background_clr = (255, 244, 2),
    hov_background_clr = (217,210,2),
    font_clrs = [(25,25,25)],
    font_family = "RopaSans-Regular.ttf",
    layer = 5001,
    ease_mode = "inout",
    ease_seconds= 0.3,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

red_button = Button(
    winsize = assets.BASE_SIZE,
    loc = ((395,220),"bottomright"),
    size = (115,115),
    border = [-1,(219, 16, 1),0,'outset'],
    hov_border = [5, (181, 12, 0),0],
    background_clr = (219, 16, 1),
    hov_background_clr = (181, 12, 0),
    font_clrs = [(25,25,25)],
    font_family = "RopaSans-Regular.ttf",
    layer = 5001,
    ease_mode = "inout",
    ease_seconds= 0.3,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

blue_button = Button(
    winsize = assets.BASE_SIZE,
    loc = ((405,220),"bottomleft"),
    size = (115,115),
    border = [-1,(8, 84, 191),0,'outset'],
    hov_border = [5, (6, 67, 153),0],
    background_clr = (8, 84, 191),
    hov_background_clr = (6, 67, 153),
    font_clrs = [(25,25,25)],
    font_family = "RopaSans-Regular.ttf",
    layer = 5001,
    ease_mode = "inout",
    ease_seconds= 0.3,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

green_button = Button(
    winsize = assets.BASE_SIZE,
    loc = ((405,230),"topleft"),
    size = (115,115),
    border = [-1,(53, 153, 17),0,'outset'],
    hov_border = [5, (42, 115, 13), 0],
    background_clr = (53, 153, 17),
    hov_background_clr = (42, 115, 13),
    font_clrs = [(25,25,25)],
    font_family = "RopaSans-Regular.ttf",
    layer = 5001,
    ease_mode = "inout",
    ease_seconds= 0.3,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

cancel_wild = Button(
    winsize=assets.BASE_SIZE,
    loc = [(400,400),"center"],
    background_clr = (250,250,250),
    size = [235,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Annuler",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 5001,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

playable_card_box = Box(
    winsize = assets.BASE_SIZE,
    size = [250,70],
    loc = [[400,350],"center"],
    background_clr = [240,240,240],
    parent_groups = [all_group,to_draw_group],
    border = [2,(20,20,20),2,"inset"],
    living = False,
    layer = 5001
)

play_card_button = Button(
    winsize=assets.BASE_SIZE,
    loc = [(342.5,350),"center"],
    background_clr = (250,250,250),
    size = [100,35],
    border=[1,(25,25,25),0,"inset"],
    text = "Jouer",
    font_clrs=[(25,25,25)],
    font_size=25,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[1,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[2,(25,25,25),0],
    layer = 5002,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

keep_card_button = Button(
    winsize=assets.BASE_SIZE,
    loc = [(457.5,350),"center"],
    background_clr = (250,250,250),
    size = [100,35],
    border=[1,(25,25,25),0,"inset"],
    text = "Garder",
    font_clrs=[(25,25,25)],
    font_size=25,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[1,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[2,(25,25,25),0],
    layer = 5002,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

keep_wild_card_button = Button(
    winsize=assets.BASE_SIZE,
    loc = [(400,400),"center"],
    background_clr = (250,250,250),
    size = [235,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Garder",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 5001,
    parent_groups = [all_group,to_draw_group,buttons_group],
    living = False
)

suivant_gauche = Title(
    winsize = assets.BASE_SIZE, 
    loc = [(230,225),"center"], 
    background_clr = (235,235,235),
    size = [60 ,18],
    border=[2,(25,25,25),0,"inset"],
    text = "Suivant",
    font_clrs = [(25,25,25)],
    font_size = 18,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    parent_groups = [all_group,to_draw_group]
)

suivant_droite = Title(
    winsize = assets.BASE_SIZE, 
    loc = [(570,225),"center"], 
    background_clr = (235,235,235),
    size = [60 ,18],
    border=[2,(25,25,25),0,"inset"],
    text = "Suivant",
    font_clrs = [(25,25,25)],
    font_size = 18,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    parent_groups = [all_group,to_draw_group],
    living = False
)

reprendre_button = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,157.5),"center"], 
    background_clr = (250,250,250),
    size = [275,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Retour au jeu",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 6001,
    parent_groups = [pause_all_group, to_draw_group, pause_buttons_group],
    living = False
)

sauvegarder_button = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,202.5),"center"], 
    background_clr = (250,250,250),
    size = [275,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Sauvegarder la partie",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 6001,
    parent_groups = [pause_all_group, to_draw_group, pause_buttons_group],
    living = False
)

parametres_button = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,247.5),"center"], 
    background_clr = (250,250,250),
    size = [275,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Paramètres",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 6001,
    parent_groups = [pause_all_group, to_draw_group, pause_buttons_group],
    living = False
)

quitter_button = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,292.5),"center"], 
    background_clr = (250,250,250),
    size = [275,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Quitter la partie",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 6001,
    parent_groups = [pause_all_group, to_draw_group, pause_buttons_group],
    living = False
)

texte_gagant = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,175],"center"],
    background_clr = [0,0,0,0],
    font_clrs = [[250,250,250]],
    font_size = 64,
    size = [400,150],
    text = "Victoire de",
    font_family = "RopaSans-Regular.ttf",
    layer = 6001,
    living = False,
    parent_groups = [all_group,to_draw_group]
)

pseudo_gagnant = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,225],"center"],
    background_clr = [0,0,0,0],
    font_clrs = [[250,250,250]],
    font_size = 64,
    size = [400,150],
    text = "",
    font_family = "RopaSans-Regular.ttf",
    layer = 6001,
    living = False,
    parent_groups = [all_group,to_draw_group]
)


game = Game()
all_group.add(game)
to_draw_group.add(game)

deck1 = Deck(assets.BASE_SIZE,0,assets.DECK1_MIDTOP,400,[all_group,to_draw_group,cards_group],False,game)
deck2 = Deck(assets.BASE_SIZE,90,assets.DECK2_MIDTOP,225,[all_group,to_draw_group,cards_group],False,game)
deck3 = Deck(assets.BASE_SIZE,180,assets.DECK3_MIDTOP,400,[all_group,to_draw_group,cards_group],False,game)
deck4 = Deck(assets.BASE_SIZE,270,assets.DECK4_MIDTOP,225,[all_group,to_draw_group,cards_group],False,game)
decks = [deck1,deck2,deck3,deck4]




first_card = Card([assets.DRAW_PILE_CENTER,'midtop'],random.choice(assets.SIMPLE_CARDS),2,None)
cards_group.add(first_card)
all_group.add(first_card)
to_draw_group.add(first_card)


paused_game = False
a_qui_le_tour = 0
timers = []
last_played_card = None
splash_titles_state = ""


def loop(screen,new_winsize, dt,fps,game_infos = None):

    global timers,last_played_card,paused_game

    if game_infos != None:
        timers.append(Timer(assets.SECONDS_BEFORE_GAME_START,'appear_splash_titles'))
        temp_decks = random.sample(decks,4)
        for i,(name,mode) in enumerate(game_infos.items()):
            temp_decks[i].set_infos(mode,name)
            temp_decks[i].draw_cards(7,False)
        update_pseudos()

    cursor = pygame.mouse.get_pos()
    hovered_card:Card = (cards_group.get_sprites_at(cursor) or [None])[-1]

    if hovered_card:
        if hovered_card.get_face() == "hidden" or splash_title1.alive() or not deck1.interactable:
            hovered_card = None

    if paused_game:
        pause_all_group.update(new_winsize,dt,fps,cursor)
        hovered_button:Button = (pause_buttons_group.get_sprites_at(cursor) or [None])[-1]
    else:
        hovered_button:Button = (buttons_group.get_sprites_at(cursor) or [None])[-1]
        for deck in decks:
            deck.update(new_winsize,dt,fps,cursor,hovered_card)
        for timer in timers:
            res,infos = timer.pass_time(dt)
            if res:
                timers.remove(timer)
                timer_handling(res,infos)
        all_group.update(new_winsize,dt,fps,cursor)

    to_draw_group.draw(screen)
    pygame.display.flip()

    played_card = deck1.get_played_card()
    

    if played_card:
        if len(deck1.cartes) == 0:
            pseudo_gagnant.set_text(deck1.player_name)
            played_card.add_timer(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
            if deck1.player_mode == 1:
                played_card.add_timer(Timer(assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
                timers.append(Timer(assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS + 0.5,'game_end'))
                game.card_played(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
            else:
                played_card.add_timer(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
                timers.append(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS + 0.5,'game_end'))
                game.card_played(played_card,assets.BOT_PLAYING_CARD_ANIMATION_SECONDS,'out')
        else:
            last_played_card = played_card
            if deck1.player_mode == 1:
                if played_card.value in ["wild","4wild"]:
                    game.card_centered(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
                    timers.append(Timer(assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,"liven_wild_buttons"))
                elif played_card.value == "reverse":
                    game.card_played(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
                    apply_clrval_to_decks(game.color,game.value)
                    rotate_animation()
                    timers.append(Timer(2.6,'end_of_turn'))
                else:
                    game.card_played(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
                    apply_clrval_to_decks(game.color,game.value)
                    end_of_turn()
            else:
                if played_card.value in ["wild","4wild"]:
                    played_card.set_wild_color(random.choice(['r','v','b','j']))
                    played_card.add_timer(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
                    game.card_played(played_card,assets.BOT_PLAYING_CARD_ANIMATION_SECONDS,'out')
                    apply_clrval_to_decks(game.color,game.value)
                    timers.append(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS + 0.5,"appear_splash_titles"))
                elif played_card.value == "reverse":
                    played_card.add_timer(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
                    game.card_played(played_card,assets.BOT_PLAYING_CARD_ANIMATION_SECONDS,'out')
                    apply_clrval_to_decks(game.color,game.value)
                    rotate_animation()
                    timers.append(Timer(2.6 + 0.5,"appear_splash_titles"))
                else:
                    played_card.add_timer(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
                    game.card_played(played_card,assets.BOT_PLAYING_CARD_ANIMATION_SECONDS,'out')
                    apply_clrval_to_decks(game.color,game.value)
                    timers.append(Timer(assets.BOT_PLAYING_CARD_ANIMATION_SECONDS + 0.5,"appear_splash_titles"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_RIGHT) and not splash_title1.alive():
                if hovered_card:
                    hovered_card.set_clicking(True)
                if hovered_button:
                    hovered_button.set_clicking(True)

        if event.type == pygame.MOUSEBUTTONUP and not splash_title1.alive():
            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_LEFT):
                if hovered_card:
                    hovered_card.set_clicking(False)
                if hovered_button:
                    if hovered_button.clicking:
                        res = click_manage(hovered_button,new_winsize)
                        if res is not None:
                            return res
                        hovered_button.set_clicking(False)
                for button in buttons_group.sprites() + pause_buttons_group.sprites():
                    button.set_clicking(False)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if splash_titles_state == "appear" and paused_game == False:
                    disappear_splash_titles()
                    if deck1.player_mode == 1:
                        timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS,"flip_deck1"))
                    if deck1.player_mode == 1:
                        if game.value == "skip":
                            game.pop_value()
                            deck1.set_interactable(False)
                            skip_animation(0.75)
                            timers.append(Timer(1.75 + 0.75,'end_of_turn'))
                        elif game.value == "+2":
                            game.pop_value()
                            deck1.set_interactable(False)
                            skip_animation(assets.CARDS_DRAWING_DELAY_SECONDS + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS)
                            timers.append(Timer(1.75 + assets.CARDS_DRAWING_DELAY_SECONDS + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'end_of_turn'))
                            timers.append(Timer(0.625 + assets.DECK_ELEVATION_ANIMATION_SECONDS,'draw_cards',[2,True]))
                        elif game.value == "4wild":
                            game.pop_value()
                            deck1.set_interactable(False)
                            skip_animation(assets.CARDS_DRAWING_DELAY_SECONDS*3 + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS)
                            timers.append(Timer(1.75 + assets.CARDS_DRAWING_DELAY_SECONDS*3 + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'end_of_turn'))
                            timers.append(Timer(0.625 + assets.DECK_ELEVATION_ANIMATION_SECONDS,'draw_cards',[4,True]))
                        else:
                            fleche4.liven()
                            deck1.set_interactable(True)
                            deck1.elevate()
                            pioche_button.liven()
                            pioche_fleche.liven()
                    else:
                        if game.value == "skip":
                            game.pop_value()
                            skip_animation(0.75)
                            timers.append(Timer(1.75 + 0.75,'appear_splash_titles'))
                        elif game.value == "+2":
                            game.pop_value()
                            skip_animation(assets.CARDS_DRAWING_DELAY_SECONDS + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS)
                            timers.append(Timer(1.75 + assets.CARDS_DRAWING_DELAY_SECONDS + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'appear_splash_titles'))
                            timers.append(Timer(0.625 + assets.DECK_ELEVATION_ANIMATION_SECONDS,'draw_cards',[2,True]))
                        elif game.value == "4wild":
                            game.pop_value()
                            skip_animation(assets.CARDS_DRAWING_DELAY_SECONDS*3 + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS)
                            timers.append(Timer(1.75 + assets.CARDS_DRAWING_DELAY_SECONDS*3 + assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'appear_splash_titles'))
                            timers.append(Timer(0.625 + assets.DECK_ELEVATION_ANIMATION_SECONDS,'draw_cards',[4,True]))
                        else:
                            fleche4.liven()
                            timers.append(Timer(random.uniform(0.75,1.5),"play_random_card"))

            elif event.key == pygame.K_ESCAPE and not pseudo_gagnant.alive():
                paused_game = not paused_game
                pause_trigger(paused_game)
                
    if game_infos != None:
        first_card.add_timer(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
        game.card_played(first_card,assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'out') 
        apply_clrval_to_decks(game.color,game.value)



def apply_clrval_to_decks(color,value):
    for deck in decks:
        deck.set_pile_clrval(color,value)


def timer_handling(id,infos = None):

    if id == "appear_splash_titles":
        swap_decks()
        update_pseudos()
        appear_splash_titles()
        fleche4.kill()

    elif id == "flip_deck1":
        deck1.change_layers()
        deck1.flip_cards()

    elif id == "playable_card":
        playable_card_box.liven()
        keep_card_button.liven()
        play_card_button.liven()

    elif id == "end_of_turn":
        end_of_turn()

    elif id == "liven_wild_buttons":
        deck1.set_interactable(False)
        red_button.liven()
        yellow_button.liven()
        blue_button.liven()
        green_button.liven()
        dark_background100.liven()
        cancel_wild.liven()
        pioche_button.kill()
        pioche_fleche.kill()

    elif id == "switch_fleche4":
        if game.clockwise_direction:
            suivant_droite.kill()
            suivant_gauche.liven()
        else:
            suivant_gauche.kill()
            suivant_droite.liven()
        fleche4.switch_image()

    elif id == "draw_cards":
        deck1.draw_cards(*infos)
    
    elif id == "play_random_card":
        deck1.play_random_card()
        if len(deck1.suggested_cards) == 0:
            timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS + 0.5,"appear_splash_titles"))

    elif id == "game_end":
        global paused_game
        paused_game = True
        quitter_button.liven()
        pseudo_gagnant.liven()
        pause_background.liven()
        texte_gagant.liven()


def update_pseudos():

    if game.clockwise_direction:
        splash_title2.set_text(deck4.get_infos()[1])
        pseudo1.set_text(deck4.get_infos()[1])
        pseudo2.set_text(deck1.get_infos()[1])
        pseudo3.set_text(deck2.get_infos()[1])
        pseudo4.set_text(deck3.get_infos()[1])
    else:
        splash_title2.set_text(deck2.get_infos()[1])
        pseudo1.set_text(deck2.get_infos()[1])
        pseudo2.set_text(deck3.get_infos()[1])
        pseudo3.set_text(deck4.get_infos()[1])
        pseudo4.set_text(deck1.get_infos()[1])


def swap_decks():
    
    infos1 = deck1.get_infos()
    infos2 = deck2.get_infos()
    infos3 = deck3.get_infos()
    infos4 = deck4.get_infos()

    cartes1 = deck1.get_cards()
    cartes2 = deck2.get_cards()
    cartes3 = deck3.get_cards()
    cartes4 = deck4.get_cards()
    
    if game.clockwise_direction:
        deck1.set_cards(cartes4)
        deck2.set_cards(cartes1)
        deck3.set_cards(cartes2)
        deck4.set_cards(cartes3)

        deck1.set_infos(*infos4)
        deck2.set_infos(*infos1)
        deck3.set_infos(*infos2)
        deck4.set_infos(*infos3)
        
    else:
        deck1.set_cards(cartes2)
        deck2.set_cards(cartes3)
        deck3.set_cards(cartes4)
        deck4.set_cards(cartes1)

        deck1.set_infos(*infos2)
        deck2.set_infos(*infos3)
        deck3.set_infos(*infos4)
        deck4.set_infos(*infos1)
        pseudo1.set_text(infos2[1])
        pseudo2.set_text(infos3[1])
        pseudo3.set_text(infos4[1])
        pseudo4.set_text(infos1[1])

    deck1.shift_cards(0,"inout")
    deck2.shift_cards(0,"inout")
    deck3.shift_cards(0,"inout")
    deck4.shift_cards(0,"inout")
    deck1.rotate_cards(0,"inout")
    deck2.rotate_cards(0,"inout")
    deck3.rotate_cards(0,"inout")
    deck4.rotate_cards(0,"inout")


def click_manage(button:Button,new_winsize):

    global last_played_card, paused_game
    
    if button in [red_button,yellow_button,blue_button,green_button]:
        red_button.kill()
        yellow_button.kill()
        blue_button.kill()
        green_button.kill()
        dark_background100.kill()
        cancel_wild.kill()
        keep_wild_card_button.kill()
        pioche_button.liven()
        pioche_fleche.liven()
        if button is red_button:
            last_played_card.set_wild_color("r")
            apply_clrval_to_decks("r",None)
        elif button is yellow_button:
            last_played_card.set_wild_color("j")
            apply_clrval_to_decks("j",None)
        elif button is green_button:
            last_played_card.set_wild_color("v")
            apply_clrval_to_decks("v",None)
        elif button is blue_button:
            last_played_card.set_wild_color("b")
            apply_clrval_to_decks("b",None)
        game.card_played(last_played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
        end_of_turn()

    elif button is cancel_wild:
        deck1.set_interactable(True)
        red_button.kill()
        yellow_button.kill()
        blue_button.kill()
        green_button.kill()
        dark_background100.kill()
        cancel_wild.kill()
        pioche_button.liven()
        pioche_fleche.liven()
        deck1.add_card(last_played_card)
        last_played_card.resize(assets.CARDS_ELEVATION_SIZE_RATIO,assets.CARDS_SORTING_ANIMATION_SECONDS,"out")
        deck1.arrange()
        deck1.shift_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,"inout")
        deck1.rotate_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,"inout")

    elif button is pioche_button:
        deck1.set_interactable(False)
        pioche_button.kill()
        pioche_fleche.kill()

        x,y = assets.DRAW_PILE_CENTER
        h = assets.CARD_SIZE[1]

        pos = [x, y - h/2]
        valeur = game.draw_card()
        carte = Card([pos,'midtop'],valeur,10,deck1,1)
        all_group.add(carte)
        to_draw_group.add(carte)
        cards_group.add(carte)
        carte.rescale(new_winsize)
        if game.playable(carte): 
            last_played_card = carte
            carte.add_timer(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS/2,"flip",[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
            game.card_centered(carte,assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'out')
            timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS*0.75,"playable_card"))

        else:
            deck1.add_card(carte)
            carte.add_timer(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS/2,"flip",[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
            carte.resize(assets.CARDS_ELEVATION_SIZE_RATIO,assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS/2,'out')
            deck1.arrange()
            deck1.shift_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"out")
            deck1.rotate_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"inout")
            timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS*0.75,"end_of_turn"))
        
    elif button is play_card_button:

        playable_card_box.kill()
        keep_card_button.kill()
        play_card_button.kill()
        if last_played_card.value in ["wild","4wild"]:
            red_button.liven()
            yellow_button.liven()
            blue_button.liven()
            green_button.liven()
            keep_wild_card_button.liven()
            dark_background100.liven()
        elif last_played_card.value == "reverse":
            game.card_played(last_played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
            apply_clrval_to_decks(game.color,game.value)
            rotate_animation()
            timers.append(Timer(2.6,'end_of_turn'))
        else:
            game.card_played(last_played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
            apply_clrval_to_decks(last_played_card.color,last_played_card.value)
            end_of_turn()

    elif button is keep_card_button or button is keep_wild_card_button:

        red_button.kill()
        yellow_button.kill()
        green_button.kill()
        blue_button.kill()
        dark_background100.kill()
        playable_card_box.kill()
        keep_card_button.kill()
        keep_wild_card_button.kill()
        play_card_button.kill()
        deck1.add_card(last_played_card)
        last_played_card.resize(assets.CARDS_ELEVATION_SIZE_RATIO,assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"out")
        deck1.arrange()
        deck1.shift_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"out")
        deck1.rotate_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"inout")
        timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS*0.65,"end_of_turn"))

    elif button is pause_button:
        paused_game = True
        pause_trigger(paused_game)

    elif button is reprendre_button:
        paused_game = False
        pause_trigger(paused_game)
    
    elif button is sauvegarder_button:
        pass

    elif button is quitter_button:
        return 0
        
            
def appear_splash_titles():

    global splash_titles_state

    pause_button.set_hoverable(False)
    splash_titles_state = "appear"

    ratio = splash_title1.winsize[0] / assets.BASE_SIZE[0]

    splash_title1.instant_translate([[400*ratio,125*ratio],[400*ratio,175*ratio]],[0.75],['out'])
    splash_title1.instant_change_alpha([0,255],[0.75],['out'])

    splash_title2.instant_translate([[400*ratio,125*ratio],[400*ratio,225*ratio]],[0.75],['out'])
    splash_title2.instant_change_alpha([0,255],[0.75],['out'])

    splash_title3.instant_change_alpha([0,255],[0.75],['out'])
    dark_background205.instant_change_alpha([0,255],[0.75],['out'])
    

def disappear_splash_titles():

    global splash_titles_state

    pause_button.set_hoverable(True)
    splash_titles_state = "disappear"

    ratio = splash_title1.winsize[0] / assets.BASE_SIZE[0]

    splash_title1.instant_translate([splash_title1.pos,[400*ratio,125*ratio]],[0.5],['out'])
    splash_title1.instant_change_alpha([255,0],[0.5],['out'])

    splash_title2.instant_translate([splash_title2.pos,[400*ratio,125*ratio]],[0.5],['out'])
    splash_title2.instant_change_alpha([255,0],[0.5],['out'])

    splash_title3.instant_change_alpha([255,0],[0.5],['out'])
    dark_background205.instant_change_alpha([255,0],[0.5],['out'])


def end_of_turn():

    if not deck1.interactable:
        deck1.set_interactable(True)
    deck1.lower()
    pioche_button.kill()
    pioche_fleche.kill()
    timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS,"flip_deck1"))
    timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS + assets.CARDS_REVERSE_ANIMATION_SECONDS[0]*2 + 0.5,"appear_splash_titles"))


def rotate_animation():
        
    fleche4.translate([fleche4.pos,fleche4.pos,game.pos,game.pos,fleche4.pos],[0.5,0.3,1+0.5,0.3],['linear','in','linear','out'],1)
    fleche4.resize([1,1,2.5,2.5,1],[0.5,0.3,1+0.5,0.3],['linear','in','linear','out'],1)
    timers.append(Timer(0.5+0.3+0.5,'switch_fleche4'))
    if (fleche4.degrees % 360) //2 <= 180:
        rot_deg = -720
    else:
        rot_deg = -360
    if game.clockwise_direction:
        fleche4.rotate([fleche4.degrees,fleche4.degrees,fleche4.degrees + rot_deg,fleche4.degrees + rot_deg],[0.5+0.3,1,0.5+0.3],['linear','inout','linear'],1)
        fleche4.rotate([0,-180,-180,-360,-360],[2,0.5,2,0.5],["inout","linear","inout","linear","inout"])
    else:
        
        fleche4.rotate([fleche4.degrees,fleche4.degrees,fleche4.degrees - rot_deg,fleche4.degrees - rot_deg],[0.5+0.3,1,0.5+0.3],['linear','inout','linear'],1)
        fleche4.rotate([0,180,180,360,360],[2,0.5,2,0.5],["inout","linear","inout","linear","inout"])
    

def skip_animation(skip_seconds):

    duree = [0.25,0.75,skip_seconds,0.75]
    skip_logo.liven()
    skip_logo.change_alpha([0,0,255,255,0],duree,['linear','inout','linear','inout'],1)
    skip_logo.resize([0.25,0.25,1,1,0.25],duree,['linear','inout','linear','inout'],1)
    dark_area.liven()
    dark_area.change_alpha([0,0,191,191,0],duree,['linear','inout','linear','inout'],1)
    dark_area.resize([0.25,0.25,1,1,0.25],duree,['linear','inout','linear','inout'],1)
    

def pause_trigger(paused_game):

    if paused_game:
        reprendre_button.liven()
        sauvegarder_button.liven()
        parametres_button.liven()
        quitter_button.liven()
        pause_background.liven()
        pause_button.set_hoverable(False)
    else:
        reprendre_button.kill()
        sauvegarder_button.kill()
        parametres_button.kill()
        pause_background.kill()
        quitter_button.kill()
        pause_button.set_hoverable(True)