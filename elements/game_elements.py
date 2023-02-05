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
from classes.moving_image import Moving_image
pygame.init()

all_group = pygame.sprite.Group()
buttons_group = pygame.sprite.LayeredUpdates()
to_draw_group = pygame.sprite.LayeredUpdates()
cards_group = pygame.sprite.LayeredUpdates()


background = Box(
    winsize = assets.BASE_SIZE,
    size = [802,452],
    loc = [[0,0],"topleft"],
    background_clr=(191, 23, 29),
    border = [-1,(0,0,0),0,"inset"],
    layer=1,
    parent_groups = [all_group,to_draw_group]
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

pioche_fleche = Moving_image(
    name=["arrow.png"],
    winsize=assets.BASE_SIZE,
    scale_axis=['x',55],
    loc=[[220,85],"center"],
    alt_pos = [250,85],
    ease_seconds = [assets.DRAW_PILE_ARROW_ANIMATION_SECONDS]*2,
    ease_modes = ['linear','linear'],
    layer=9,
    parent_groups = [all_group,to_draw_group],
    living = False
)

dark_background = Box(
    winsize = assets.BASE_SIZE,
    size = [800,450],
    loc = [[0,0],"topleft"],
    background_clr=(0, 0, 0, 100),
    border = [-1,(0,0,0),0,"inset"],
    layer=5000,
    parent_groups = [all_group,to_draw_group],
    living = False
)

splash_title1 = Splash_title(
    winsize = assets.BASE_SIZE,
    text_center = [400,175],
    background_clr = (0,0,0,205),
    font_clrs = [(250,250,250),(250,250,250)],
    font_size = 64,
    start_y = 125,
    appearing_ease = [0.75,'out'],
    living = False,
    text = "Au tour de",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    dismiss_ease = [0.5,'out'],
    parent_groups = [all_group,to_draw_group]
)

splash_title2 = Splash_title(
    winsize = assets.BASE_SIZE,
    text_center = [400,225],
    background_clr = (0,0,0,0),
    font_clrs = [(250,250,250),(250,250,250)],
    font_size = 64,
    start_y = 125,
    appearing_ease = [0.75,'out'],
    living = False,
    text = "Joueur 1",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    dismiss_ease = [0.5,'out'],
    parent_groups = [all_group,to_draw_group]
)
splash_title3 = Splash_title(
    winsize = assets.BASE_SIZE,
    text_center = [400,400],
    background_clr = (0,0,0,0),
    font_clrs = [(250,250,250)],
    font_size = 30,
    start_y = 400,
    appearing_ease = [0.75,'out'],
    living = False,
    text = "Appuyez sur [Espace] pour jouer",
    font_family = "RopaSans-Regular.ttf",
    layer = 5000,
    dismiss_ease = [0.5,'out'],
    parent_groups = [all_group,to_draw_group]
)

pseudo1 = Player_name(
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
    parent_groups = [all_group,to_draw_group]
)

pseudo2 = Player_name(
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
    parent_groups = [all_group,to_draw_group]
)

pseudo3 = Player_name(
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
    parent_groups = [all_group,to_draw_group]
)

pseudo4 = Player_name(
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
last_played_card = None



def loop(screen,new_winsize, dt,fps,game_infos = None):

    global timers,last_played_card

    if game_infos != None:
        timers.append(Timer(assets.SECONDS_BEFORE_GAME_START,'appear_splash_titles'))
        temp_decks = random.sample(decks,4)
        for i,(name,mode) in enumerate(game_infos.items()):
            temp_decks[i].set_infos(mode,name)
            temp_decks[i].draw_cards(7,False)
        update_pseudos()

    cursor = pygame.mouse.get_pos()
    hovered_button = (buttons_group.get_sprites_at(cursor) or [None])[-1]
    hovered_card:Card = (cards_group.get_sprites_at(cursor) or [None])[-1]

    if hovered_card:
        if hovered_card.get_face() == "hidden" or splash_title1.alive() or dark_background.alive():
            hovered_card = None

    for deck in decks:
        deck.update(new_winsize,dt,fps,cursor,hovered_card)
    played_card = deck1.get_played_card()
    
    if played_card:
        last_played_card = played_card
        
        if played_card.get_value() in ["wild","4wild"]:
            game.card_centered(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
            timers.append(Timer(assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,"liven_wild_buttons"))
        else:
            game.card_played(played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
            apply_clrval_to_decks(game.get_color(),game.get_value())
            end_of_turn()

        
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
                if hovered_button:
                    hovered_button.set_clicking(True)

        if event.type == pygame.MOUSEBUTTONUP and not splash_title1.alive():
            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_LEFT):
                if hovered_card:
                    hovered_card.set_clicking(False)
                if hovered_button:
                    if hovered_button.get_clicking():
                        click_manage(hovered_button,new_winsize)
                        
                        hovered_button.set_clicking(False)
                for button in buttons_group.sprites():
                    button.set_clicking(False)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if splash_title1.get_state() in ["showed","appearing"]:
                    swap_decks()
                    splash_title1.dismiss()
                    splash_title2.dismiss()
                    splash_title3.dismiss()
                    timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS,"flip_deck1"))
                    deck1.elevate()
                    pioche_button.liven()
                    pioche_fleche.liven()
                    pseudo1.set_highlight()

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
        apply_clrval_to_decks(game.get_color(),game.get_value())



def apply_clrval_to_decks(color,value):
    for deck in decks:
        deck.set_pile_clrval(color,value)


def timer_handling(id,infos = None):

    if id == "appear_splash_titles":
        update_pseudos()
        splash_title1.appear()
        splash_title2.appear()
        splash_title3.appear()

    elif id == "flip_deck1":
        deck1.flip_cards()

    elif id == "playable_card":
        dark_background.liven()
        playable_card_box.liven()
        keep_card_button.liven()
        play_card_button.liven()

    elif id == "end_of_turn":
        end_of_turn()

    elif id == "liven_wild_buttons":
        red_button.liven()
        yellow_button.liven()
        blue_button.liven()
        green_button.liven()
        dark_background.liven()
        cancel_wild.liven()
    

def update_pseudos():

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


def click_manage(button:Button,new_winsize):

    global last_played_card
    
    if button in [red_button,yellow_button,blue_button,green_button]:
        red_button.kill()
        yellow_button.kill()
        blue_button.kill()
        green_button.kill()
        dark_background.kill()
        cancel_wild.kill()
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

    if button is cancel_wild:
        red_button.kill()
        yellow_button.kill()
        blue_button.kill()
        green_button.kill()
        dark_background.kill()
        cancel_wild.kill()
        deck1.add_card(last_played_card)
        last_played_card.resize(assets.CARDS_ELEVATION_SIZE_RATIO,assets.CARDS_SORTING_ANIMATION_SECONDS,"out")
        deck1.arrange()
        deck1.shift_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,"inout")
        deck1.rotate_cards(assets.CARDS_SORTING_ANIMATION_SECONDS,"inout")

    if button is pioche_button:

        pioche_button.kill()
        pioche_fleche.kill()

        x,y = assets.DRAW_PILE_CENTER
        h = assets.CARD_SIZE[1]

        pos = [x, y - h/2]
        valeur = deck1.draw_pile.pop(random.randint(0,len(deck1.draw_pile)-1))
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
            deck1.arrange()
            deck1.shift_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"out")
            deck1.rotate_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"inout")
            timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS*0.75,"end_of_turn"))
        
    if button is play_card_button:

        print(last_played_card.value)
        dark_background.kill()
        playable_card_box.kill()
        keep_card_button.kill()
        play_card_button.kill()
        if last_played_card.value in ["wild","4wild"]:
            red_button.liven()
            yellow_button.liven()
            blue_button.liven()
            green_button.liven()
            dark_background.liven()
        else:
            game.card_played(last_played_card,assets.CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS,'out')
            end_of_turn()

    if button is keep_card_button:

        dark_background.kill()
        playable_card_box.kill()
        keep_card_button.kill()
        play_card_button.kill()
        deck1.add_card(last_played_card)
        last_played_card.resize(assets.CARDS_ELEVATION_SIZE_RATIO,assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"out")
        deck1.arrange()
        deck1.shift_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"out")
        deck1.rotate_cards(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS,"inout")
        timers.append(Timer(assets.CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS*0.65,"end_of_turn"))
        
            


def end_of_turn():

    deck1.lower()
    pioche_button.kill()
    pioche_fleche.kill()
    pseudo1.set_highlight()
    timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS,"flip_deck1"))
    timers.append(Timer(assets.DECK_ELEVATION_ANIMATION_SECONDS + assets.CARDS_REVERSE_ANIMATION_SECONDS[0]*2 + 0.5,"appear_splash_titles"))