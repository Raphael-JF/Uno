"""
Ce module contient les éléments et widgets du menu jeu. Il contient aussi le code de gestion utilisateur pour ce menu.
"""

import random
import pygame,assets,sys,itertools
from classes.timer import Timer
from classes.splash_title import Splash_title
from classes.box import Box
from classes.image import Image
from classes.title import Title
from classes.deck import Deck
from classes.card import Card
from classes.game import Game
pygame.init()

all_group = pygame.sprite.Group()
to_draw_group = pygame.sprite.LayeredUpdates()
cards_group = pygame.sprite.LayeredUpdates()


background = Box(
    winsize = assets.BASE_SIZE,
    size = [802,452],
    loc = [[0,0],"topleft"],
    background_clr=(191, 23, 29),
    border = [-1,(0,0,0),0,"inset"],
    layer=1,
)

pioche = Image(
    name=["cartes","hidden.png"],
    winsize=assets.BASE_SIZE,
    degrees=assets.DRAW_PILE_DEGREES,
    scale_axis=['y',assets.CARD_SIZE[1]],
    loc=[assets.DRAW_PILE_CENTER,"center"],
    layer=9
)

splash_title1 = Splash_title(
    winsize = assets.BASE_SIZE,
    text_center = [400,175],
    background_clr = (0,0,0,205),
    font_clrs = [(250,250,250),(250,250,250)],
    font_size = 64,
    start_y = 125,
    parent_groups = (all_group,to_draw_group),
    appearing_ease = [0.75,'out'],
    alive_at_start = True,
    text = "Au tour de",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    dismiss_ease = [0.5,'out'],
)

splash_title2 = Splash_title(
    winsize = assets.BASE_SIZE,
    text_center = [400,225],
    background_clr = (0,0,0,0),
    font_clrs = [(250,250,250),(250,250,250)],
    font_size = 64,
    start_y = 125,
    parent_groups = (all_group,to_draw_group),
    appearing_ease = [0.75,'out'],
    alive_at_start = True,
    text = "JOUEUR 1",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    dismiss_ease = [0.5,'out'],
)
splash_title3 = Splash_title(
    winsize = assets.BASE_SIZE,
    text_center = [400,400],
    background_clr = (0,0,0,0),
    font_clrs = [(250,250,250)],
    font_size = 30,
    start_y = 400,
    parent_groups = (all_group,to_draw_group),
    appearing_ease = [0.75,'out'],
    alive_at_start = True,
    text = "Appuyez sur [Espace] pour jouer",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    dismiss_ease = [0.5,'out'],
)

pseudo1 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,310],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    border = [-1,(0,0,0),0,'inset'],
    size = [133,27],
    text = "Joueur 1",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
)

pseudo2 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[570,200],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    border = [-1,(0,0,0),0,'inset'],
    size = [133,27],
    text = "Joueur 2",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
)

pseudo3 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[400,90],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    border = [-1,(0,0,0),0,'inset'],
    size = [133,27],
    text = "Joueur 3",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
)

pseudo4 = Title(
    winsize = assets.BASE_SIZE,
    loc = [[230,200],'center'],
    background_clr = (191, 23, 29),
    font_clrs = [[255, 237, 238]],
    font_size = 25,
    border = [-1,(0,0,0),0,'inset'],
    size = [133,27],
    text = "Joueur 4",
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
)


all_group.add([background,pioche,pseudo1,pseudo2,pseudo3,pseudo4])
to_draw_group.add([background,pioche,pseudo1,pseudo2,pseudo3,pseudo4])

deck1 = Deck(assets.BASE_SIZE,0,assets.DECK1_MIDTOP,400,[all_group,to_draw_group,cards_group],False)
deck2 = Deck(assets.BASE_SIZE,90,assets.DECK2_MIDTOP,225,[all_group,to_draw_group,cards_group],False)
deck3 = Deck(assets.BASE_SIZE,180,assets.DECK3_MIDTOP,400,[all_group,to_draw_group,cards_group],False)
deck4 = Deck(assets.BASE_SIZE,270,assets.DECK4_MIDTOP,225,[all_group,to_draw_group,cards_group],False)
decks = [deck1,deck2,deck3,deck4]


game = Game()
all_group.add(game)
to_draw_group.add(game)

first_card = Card([assets.DRAW_PILE_CENTER,'midtop'],random.choice(assets.SIMPLE_CARDS),2,None)
cards_group.add(first_card)
all_group.add(first_card)
to_draw_group.add(first_card)



a_qui_le_tour = 0
clockwise_direction = random.choice([True, False])
timers = []



def loop(screen,new_winsize, dt,fps,game_infos = None):

    global timers

    if game_infos != None:
        timers.append(Timer(assets.SECONDS_BEFORE_GAME_START,'appear_splash_titles'))
        temp_decks = random.sample(decks,4)
        for i,(name,mode) in enumerate(game_infos.items()):
            temp_decks[i].set_infos(mode,name)
            temp_decks[i].draw_cards(7,False)

    cursor = pygame.mouse.get_pos()

    hovered_card:Card = (cards_group.get_sprites_at(cursor) or [None])[-1]
    if hovered_card:
        if hovered_card.get_face() == "hidden":
            hovered_card = None

    for deck in decks:
        deck.update(new_winsize,dt,fps,cursor,hovered_card)
    played_card = deck1.get_played_card()

    if played_card:
        game.card_played(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
        deck1.lower()
        timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS,"flip_deck1"))
        timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS + assets.CARDS_REVERSE_ANIMATION_SECONDS[0]*2 + 0.5,"appear_splash_titles"))
        

    for timer in timers:
        res,infos = timer.pass_time(dt)
        if res:
            timers.remove(timer)
            timer_handling(res,infos)

    all_group.update(
        new_winsize = new_winsize, 
        dt = dt, 
        fps = fps,
        cursor = cursor
    )

    to_draw_group.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_RIGHT) and not splash_title1.alive():
                if hovered_card:
                    hovered_card.set_clicking(True)
        
        if event.type == pygame.MOUSEBUTTONUP and not splash_title1.alive():
            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_LEFT):
                if hovered_card:
                    hovered_card.set_clicking(False)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if splash_title1.get_state() in ["showed","appearing"]:
                    swap_decks()
                    splash_title1.dismiss()
                    splash_title2.dismiss()
                    splash_title3.dismiss()
                    timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS,"flip_deck1"))
                    deck1.elevate()

            if event.key == pygame.K_a:
                deck1.draw_cards(1,True)
            
            if event.key == pygame.K_b:
                deck1.shift_cards(0,'inout')
                deck2.shift_cards(0,'inout')
                deck3.shift_cards(0,'inout')
                deck4.shift_cards(0,'inout')

            if event.key == pygame.K_KP1:
                deck1.flip_cards()
            elif event.key == pygame.K_KP2:
                deck2.flip_cards()
            elif event.key == pygame.K_KP3:
                deck3.flip_cards()
            elif event.key == pygame.K_KP4:
                deck4.flip_cards()
            elif event.key == pygame.K_ESCAPE:
                return 0
                
    if game_infos != None:
        first_card.add_timer(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS/2,'flip',[assets.CARDS_REVERSE_ANIMATION_SECONDS,['in','out']]))
        game.card_played(first_card,assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,'out')        

    

def timer_handling(id,infos = None):

    if id == "appear_splash_titles":
        if clockwise_direction:
            splash_title2.change_text(deck4.get_infos()[1])
            pseudo1.set_text(deck4.get_infos()[1])
            pseudo2.set_text(deck1.get_infos()[1])
            pseudo3.set_text(deck2.get_infos()[1])
            pseudo4.set_text(deck3.get_infos()[1])
        else:
            splash_title2.change_text(deck2.get_infos()[1])
            pseudo1.set_text(deck2.get_infos()[1])
            pseudo2.set_text(deck3.get_infos()[1])
            pseudo3.set_text(deck4.get_infos()[1])
            pseudo4.set_text(deck1.get_infos()[1])
        
        splash_title1.appear()
        splash_title2.appear()
        splash_title3.appear()

    if id == "flip_deck1":
        deck1.flip_cards()
    

def swap_decks():
    
    infos1 = deck1.get_infos()
    infos2 = deck2.get_infos()
    infos3 = deck3.get_infos()
    infos4 = deck4.get_infos()

    cartes1 = deck1.get_cards()
    cartes2 = deck2.get_cards()
    cartes3 = deck3.get_cards()
    cartes4 = deck4.get_cards()
    
    if clockwise_direction:
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