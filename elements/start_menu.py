"""
Ce module contient les éléments et widgets du menu de lancement. Il contient aussi le code de gestion utilisateur pour ce menu.
"""

import pygame,sys,assets
pygame.init()
from classes.box import Box
from classes.button import Button
from classes.image import Image

all_group = pygame.sprite.Group()
to_draw_group = pygame.sprite.LayeredUpdates()
clickable_group = pygame.sprite.LayeredUpdates()

background = Box(
    winsize = assets.BASE_SIZE,
    size = [802,452],
    loc = [[0,0],"topleft"],
    background_clr=(191, 23, 29),
    border = [-1,(0,0,0),0,"inset"],
    parent_groups = [all_group, to_draw_group],
)

title = Image(
    name = ["logo.png"],
    winsize = assets.BASE_SIZE,
    scale_axis = ['y',150],
    loc = [[400,20],"midtop"],
    border = [0,(0,0,0,0)],
    layer = 1,
    parent_groups = [all_group, to_draw_group],
)

charger_partie = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,215),"center"], 
    background_clr = (250,250,250),
    size = [350,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Charger une partie",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 1,
    parent_groups = [all_group, to_draw_group, clickable_group],
)

nouvelle_partie = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,261),"center"], 
    background_clr = (250,250,250),
    size = [350,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Nouvelle partie",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 1,
    parent_groups = [all_group, to_draw_group, clickable_group],
)

options = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(400,307),"center"], 
    background_clr = (250,250,250),
    size = [350,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Options",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 1,
    parent_groups = [all_group, to_draw_group, clickable_group],
)

credits = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(397,353),"midright"], 
    background_clr = (250,250,250),
    size = [172 ,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Crédits",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 1,
    parent_groups = [all_group, to_draw_group, clickable_group],
)

quitter = Button(
    winsize = assets.BASE_SIZE, 
    loc = [(403,353),"midleft"], 
    background_clr = (250,250,250),
    size = [172,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Quitter",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 1,
    parent_groups = [all_group, to_draw_group, clickable_group],
)


def loop(screen,new_winsize, dt,fps):

    cursor = pygame.mouse.get_pos()

    hovered_button = (clickable_group.get_sprites_at(cursor) or [None])[-1]

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

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_RIGHT):
                if hovered_button != None :
                    hovered_button.set_clicking(True)

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_RIGHT): 
                if hovered_button != None :
                    if hovered_button.get_clicking():
                        res = click_manage(hovered_button)
                        hovered_button.set_clicking(False)
                        return res
                        
                for button in clickable_group.sprites():
                    button.set_clicking(False)


def click_manage(button:Button):

    # for but in clickable_group.sprites():
    #     but.reset_attributes()

    if button == charger_partie:
        return 1
    if button == nouvelle_partie:
        return 2
    if button == options:
        return 3
    if button == credits:
        return 4
    if button == quitter:
        return 5