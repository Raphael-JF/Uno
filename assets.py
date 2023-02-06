"""Ce module contient toutes les constantes nécessaires au fonctionnement du programme."""

BASE_SIZE = (800,450) #échelle pour laquelle on définit les valeurs de nos widgets
TIME_TICKING = 60 #temps in game (immutable)
START_GAME_FPS = 60 #fps au démarrage du jeu

INPUT_FIELD_DASH_DELAY = 0.5 # délai de disparition/apparition du curseur dans un input_field
KEYPRESS_SPAM_DELAY = 0.5 # délai avant entrée en mode spam dans un input_field
CHARS_SPAM_DELAY = 0.05 # délai entre chaque placement de caractère en mode spam dans un input_field

BASE_CARD_SIZE = [325,500] # taille initiale des images de cartes
CARD_SIZE = [72,112] # taille des cartes selon BASE_SIZE

DECK1_MIDTOP = [400,366] # coordonnées du midtop de la zone du paquet du bas
DECK2_MIDTOP = [750,225] # coordonnées du midleft de la zone du paquet de droite (on écrit midtop car techniquement c'est le milieu du haut de la carte malgré la rotation antihoraire de 90°)
DECK3_MIDTOP = [400,50] # coordonnées du midbottom de la zone du paquet du haut (on écrit midtop car techniquement c'est le milieu du haut de la carte malgré la rotation antihoraire de 180°)
DECK4_MIDTOP = [50,225] # coordonnées du midright de la zone du paquet de gauche (on écrit midtop car techniquement c'est le milieu du haut de la carte malgré la rotation antihoraire de 270)

DRAW_PILE_CENTER = [110,75] # centre de la pioche selon BASE_SIZE
DRAW_PILE_DEGREES = 0 # angle d'inclinaison de la pioche
HOVERED_DECK_ELEVATION_PX = 15 #hauteur que prend le paquet entier pour indiquer qu'il faut jouer
HOVERED_CARD_ELEVATION_PX = 25 # hauteur que prend une carte survolée dans le paquet selon BASE_SIZE
SUGGESTED_CARD_ELEVATION_PX = 15 # hauteur que prend une carte suggérée dans le paquet selon BASE_SIZE

CARDS_ELEVATION_SIZE_RATIO = 1.1 #ratio de taille pour les cartes dont le paquet est surélevé


GAME_PILE_CENTER = [400,200] # centre de la surface de la pile de jeu selon BASE_SIZE
GAME_PILE_SIZE = [140,140] # dimensions de la surface de la pile de jeu
GAME_PILE_HITBOX = [250,150] # dimensions du rectangle de réactivité sur lequel la carte est sensible



SIMPLE_CARDS = [ #cartes numérotées
    'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9',
          'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9',
    'j0', 'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9',
          'j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8', 'j9',
    'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9',
          'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9',
    'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9',
          'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9']
SPECIAL_CARDS = [ #cartes non numérotées
    'b+2', 'breverse', 'bskip','b+2', 'breverse', 'bskip',
    'j+2', 'jreverse', 'jskip','j+2', 'jreverse', 'jskip',
    'r+2', 'rreverse', 'rskip','r+2', 'rreverse', 'rskip',
    'v+2', 'vreverse', 'vskip','v+2', 'vreverse', 'vskip',
    'wild','wild','wild','wild','4wild','4wild','4wild','4wild']
ALL_CARDS = SIMPLE_CARDS + SPECIAL_CARDS # contenu du paquet selon les règles officielles du Uno

CARD_RESIZE_ANIMATION_SECONDS = 0.25 # durée de l'animation de changement de taille d'une carte
CARDS_DRAWING_DELAY_BEFORE_FLIP = 0.35 # délai entre le tirage de la carte et le début de son animation de retournement
CARDS_REVERSE_ANIMATION_SECONDS = [0.1125,0.1125] # durée de rétrécissement et durée d'agrandissement lors de l'animation de retournement d'une carte
CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS = 1.25 # durée de l'animation de translation de carte
CARDS_SORTING_ANIMATION_SECONDS = 0.4
CARDS_HOVER_SHIFT_ANIMATION_SECONDS = 0.75 # durée de l'animation de sortie du paquet d'une carte (quand on met le curseur sur elle)
CARD_ATTRACTION_CENTER_PILE_ANIMATION_SECONDS = 0.35 # durée de l'animation de dépôt d'une carte sur la pile du jeu.
CARDS_DRAWING_DELAY_SECONDS = 0.35 #délai entre la pioche de plusieurs cartes
SECONDS_BEFORE_GAME_START = CARDS_DRAWING_DELAY_SECONDS*7 + CARDS_TRAVEL_FROM_DRAW_PILE_ANIMATION_SECONDS + CARDS_SORTING_ANIMATION_SECONDS +0.2# temps pour distribuer les cartes avant de commencer à faire jouer les joueurs
DECK_ELEVATION_ANIMATION_SECONDS = 0.35 #durée de l'animation d'élévation/descente du paquet.
DECK_ROTATION_ANIMATION_SECONDS = 0.25 #durée de l'animation de rotation du paquet
PLAYER_NAME_RESIZING_ANIMATION_SECONDS = 0.5 # durée de l'animation de rétrécissement / agrandissement du nom du joueur qui joue.
DRAW_PILE_ARROW_ANIMATION_SECONDS = 0.5 # durée de l'animation de mouvement de la flèche guidant vers la pioche




# ALL_CARDS = ["wild"]*15