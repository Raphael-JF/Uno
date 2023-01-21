"""
Ce module contient les éléments et widgets du menu "Créer une partie". Il contient aussi le code de gestion utilisateur pour ce menu.
"""

import pygame,sys,assets
pygame.init()
from classes.box import Box
from classes.title import Title
from classes.button import Button
from classes.image import Image
from classes.input_field import Input_field
from classes.button_family import Button_family

background = Box(
    winsize = assets.BASE_SIZE,
    size = [802,452],
    loc = [[0,0],"topleft"],
    background_clr=(191, 23, 29),
    border = [-1,(0,0,0),0,"inset"],
)

title = Title(
    winsize = assets.BASE_SIZE, 
    loc = [(400,25),"midtop"], 
    background_clr = (235,235,235),
    size = [250 ,50],
    border=[2,(25,25,25),0,"inset"],
    text = "Nouvelle partie",
    font_clrs = [(25,25,25)],
    font_size = 40,
    font_family = "RopaSans-Regular.ttf",
    layer = 1
)

annuler = Button(
    winsize=assets.BASE_SIZE,
    loc = [(250,400),"center"],
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
    layer = 1
)

creer_partie = Button(
    winsize=assets.BASE_SIZE,
    loc = [(550,400),"center"],
    background_clr = (250,250,250),
    size = [235,40],
    border=[2,(25,25,25),2,"inset"],
    text = "Créer la partie",
    font_clrs=[(25,25,25)],
    font_size=30,
    font_family="RopaSans-Regular.ttf",
    ease_seconds=0.25,
    ease_mode="inout",
    hov_background_clr=(230,230,230),
    hov_border=[2,(25,25,25),0],
    active_background_clr=(210,210,210),
    active_border=[3,(25,25,25),0],
    layer = 1
)

# Joueur 1
conteneur_j1 = Box(
    winsize = assets.BASE_SIZE,
    loc = [(385,173),"midright"],
    size = [275,75],
    border = [2,(25,25,25),2,"inset"],
    background_clr = (250,250,250),
    layer = 1
)
champ_j1 = Input_field(
    winsize = assets.BASE_SIZE,
    loc = [(205,173),'center'],
    size = [150,35],
    font_size = 26,
    font_family = "RopaSans-Regular.ttf",
    font_clr = (0,0,0),
    background_clr = (230,230,230),
    border = [1,(0,0,0),0,"inset"],
    text_align = [10,"left"],
    text = "Joueur 1",
    layer = 2,
    hov_background_clr = (250,250,250),
    hov_border = [1,(0,0,0),0],
    active_background_clr = (250,250,250),
    active_border = [2,(0,0,0),0],
    ease_mode="inout",
    ease_seconds=0.25,
)
ordi_j1 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((331,160),"center"),
    size = (70,20),
    text = "ordi",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)
humain_j1 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((331,186),"center"),
    size = (70,20),
    text = "humain",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)


#Joueur 2
conteneur_j2 = Box(
    winsize = assets.BASE_SIZE,
    loc = [(415,173),"midleft"],
    size = [275,75],
    border = [2,(25,25,25),2,"inset"],
    background_clr = (250,250,250),
    layer = 1
)
champ_j2 = Input_field(
    winsize = assets.BASE_SIZE,
    loc = [(510,173),'center'],
    size = [150,35],
    font_size = 26,
    font_family = "RopaSans-Regular.ttf",
    font_clr = (0,0,0),
    background_clr = (230,230,230),
    border = [1,(0,0,0),0,"inset"],
    text_align = [10,"left"],
    text = "Joueur 2",
    layer = 2,
    hov_background_clr = (250,250,250),
    hov_border = [1,(0,0,0),0],
    active_background_clr = (250,250,250),
    active_border = [2,(0,0,0),0],
    ease_mode="inout",
    ease_seconds=0.25,
)
ordi_j2 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((636,160),"center"),
    size = (70,20),
    text = "ordi",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)
humain_j2 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((636,186),"center"),
    size = (70,20),
    text = "humain",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)


#Joueur 3
conteneur_j3 = Box(
    winsize = assets.BASE_SIZE,
    loc = [(385,277),"midright"],
    size = [275,75],
    border = [2,(25,25,25),2,"inset"],
    background_clr = (250,250,250),
    layer = 1
)
champ_j3 = Input_field(
    winsize = assets.BASE_SIZE,
    loc = [(205,277),'center'],
    size = [150,35],
    font_size = 26,
    font_family = "RopaSans-Regular.ttf",
    font_clr = (0,0,0),
    background_clr = (230,230,230),
    border = [1,(0,0,0),0,"inset"],
    text_align = [10,"left"],
    text = "Joueur 3",
    layer = 2,
    hov_background_clr = (250,250,250),
    hov_border = [1,(0,0,0),0],
    active_background_clr = (250,250,250),
    active_border = [2,(0,0,0),0],
    ease_mode="inout",
    ease_seconds=0.25,
)
ordi_j3 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((331,264),"center"),
    size = (70,20),
    text = "ordi",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)
humain_j3 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((331,290),"center"),
    size = (70,20),
    text = "humain",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)


#Joueur 4
conteneur_j4 = Box(
    winsize = assets.BASE_SIZE,
    loc = [(415,277),"midleft"],
    size = [275,75],
    border = [2,(25,25,25),2,"inset"],
    background_clr = (250,250,250),
    layer = 1
)
champ_j4 = Input_field(
    winsize = assets.BASE_SIZE,
    loc = [(510,277),'center'],
    size = [150,35],
    font_size = 26,
    font_family = "RopaSans-Regular.ttf",
    font_clr = (0,0,0),
    background_clr = (230,230,230),
    border = [1,(0,0,0),0,"inset"],
    text_align = [10,"left"],
    text = "Joueur 4",
    layer = 2,
    hov_background_clr = (250,250,250),
    hov_border = [1,(0,0,0),0],
    active_background_clr = (250,250,250),
    active_border = [2,(0,0,0),0],
    ease_mode="inout",
    ease_seconds=0.25,
)
ordi_j4 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((636,264),"center"),
    size = (70,20),
    text = "ordi",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)
humain_j4 = Button(
    winsize = assets.BASE_SIZE,
    loc = ((636,290),"center"),
    size = (70,20),
    text = "humain",
    border = [1,(25,25,25),0,'inset'],
    background_clr = (250,250,250),
    font_clrs = [(25,25,25)],
    font_size = 22,
    font_family = "RopaSans-Regular.ttf",
    layer = 2,
    ease_mode = "inout",
    ease_seconds= 0.3,
)


famille_boutons_j1 = Button_family("enabled","disabled")
famille_boutons_j1.add_button(ordi_j1,"disabled")
famille_boutons_j1.add_button(humain_j1,"enabled")
famille_boutons_j1.add_style_rule("enabled",background_clr = (250,250,250), border = [2,(25,25,25),0])
famille_boutons_j1.add_style_rule("disabled",background_clr = (110,110,110), border = [1,(25,25,25),0],hov_background_clr = (150,150,150),active_background_clr = (200,200,200))

famille_boutons_j2 = Button_family("enabled","disabled")
famille_boutons_j2.add_button(ordi_j2,"enabled")
famille_boutons_j2.add_button(humain_j2,"disabled")
famille_boutons_j2.add_style_rule("enabled",background_clr = (250,250,250), border = [2,(25,25,25),0])
famille_boutons_j2.add_style_rule("disabled",background_clr = (110,110,110), border = [1,(25,25,25),0],hov_background_clr = (150,150,150),active_background_clr = (200,200,200))

famille_boutons_j3 = Button_family("enabled","disabled")
famille_boutons_j3.add_button(ordi_j3,"enabled")
famille_boutons_j3.add_button(humain_j3,"disabled")
famille_boutons_j3.add_style_rule("enabled",background_clr = (250,250,250), border = [2,(25,25,25),0])
famille_boutons_j3.add_style_rule("disabled",background_clr = (110,110,110), border = [1,(25,25,25),0],hov_background_clr = (150,150,150),active_background_clr = (200,200,200))

famille_boutons_j4 = Button_family("enabled","disabled")
famille_boutons_j4.add_button(ordi_j4,"enabled")
famille_boutons_j4.add_button(humain_j4,"disabled")
famille_boutons_j4.add_style_rule("enabled",background_clr = (250,250,250), border = [2,(25,25,25),0])
famille_boutons_j4.add_style_rule("disabled",background_clr = (110,110,110), border = [1,(25,25,25),0],hov_background_clr = (150,150,150),active_background_clr = (200,200,200))



boutons_familles = [famille_boutons_j1,famille_boutons_j2,famille_boutons_j3,famille_boutons_j4]



all_group = pygame.sprite.Group()
all_group.add([
    background,
    title,
    annuler,
    creer_partie,

    conteneur_j1,
    champ_j1,
    ordi_j1,
    humain_j1,

    conteneur_j2,
    champ_j2,
    ordi_j2,
    humain_j2,

    conteneur_j3,
    champ_j3,
    ordi_j3,
    humain_j3,

    conteneur_j4,
    champ_j4,
    ordi_j4,
    humain_j4,
    
])

to_draw_group = pygame.sprite.LayeredUpdates()
to_draw_group.add([
    background,
    title,
    annuler,
    creer_partie,

    conteneur_j1,
    champ_j1,
    ordi_j1,
    humain_j1,

    conteneur_j2,
    champ_j2,
    ordi_j2,
    humain_j2,

    conteneur_j3,
    champ_j3,
    ordi_j3,
    humain_j3,

    conteneur_j4,
    champ_j4,
    ordi_j4,
    humain_j4,
])

clickable_group = pygame.sprite.LayeredUpdates()
clickable_group.add([
    annuler,
    creer_partie,
    champ_j1,
    ordi_j1,
    humain_j1,

    champ_j2,
    ordi_j2,
    humain_j2,
   
    champ_j3,
    ordi_j3,
    humain_j3,
    
    champ_j4,
    ordi_j4,
    humain_j4,
])

fields_group = pygame.sprite.LayeredUpdates()
fields_group.add([champ_j1,champ_j2,champ_j3,champ_j4])



def loop(screen,new_winsize, dt,fps):

    cursor = pygame.mouse.get_pos()

    hovered_clickable = (clickable_group.get_sprites_at(cursor) or [None])[-1]

    focused_field = None
    for field in fields_group.sprites():
        if field.get_focus():
            focused_field = field


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
            if len(clickable_group.get_sprites_at(cursor)) == 0:
                for field in fields_group.sprites():
                    field.blured()

            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_RIGHT):
                if hovered_clickable != None :
                    hovered_clickable.set_clicking(True)

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button in (pygame.BUTTON_LEFT,pygame.BUTTON_RIGHT): 
                if hovered_clickable != None :
                    if hovered_clickable.get_clicking():
                        res = click_manage(hovered_clickable)
                        hovered_clickable.set_clicking(False)
                        return res
                        
                for button in clickable_group.sprites():
                    button.set_clicking(False)
            
        elif event.type == pygame.KEYDOWN:
            
            if focused_field != None:
                focused_field.receive_keydown(event)

            elif event.key == pygame.K_ESCAPE:
                return click_manage(annuler)
            
        elif event.type == pygame.KEYUP:

            if focused_field != None:
                focused_field.receive_keyup(event)



def click_manage(clickable:Input_field|Button):
    
    if type(clickable) is Button:
        if clickable == annuler:
            # for bouton_famille in boutons_familles:
            #     bouton_famille.reset_states()
            # for but in clickable_group.sprites():
            #     but.reset_attributes()
            return 1
        
        if clickable == creer_partie:
            sortie = {}
            for bouton_famille,field in zip(boutons_familles,fields_group.sprites()):
                boutons = bouton_famille.get_buttons()
                for i in range(len(boutons)):
                    if bouton_famille.get_state(boutons[i]) == 'enabled':
                        joueur = i 
                        # 0 : ordi
                        # 1 : humain

                sortie[field.get_text()] = joueur
            return sortie

        for famille in boutons_familles:
            if clickable in famille:
                if famille.get_state(clickable) == "disabled":
                    for button in famille.get_buttons():
                        famille.set_state(button,state_switch(famille.get_state(button)))

    elif type(clickable) is Input_field:
        for field in fields_group.sprites():
            field.blured()
        clickable.clicked()


def state_switch(state):

    if state == "enabled":
        return "disabled"

    elif state == "disabled":
        return "enabled"

    else:
        pass
    