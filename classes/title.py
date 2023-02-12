import pygame,os
from classes.box import Box

class Title(Box):
    """
    Héritant de l'objet Box, Title implémente la possibilité d'afficher du texte au centre d'une boite statique.
    """
    def __init__(
        self,
        winsize:list,
        loc:list,
        background_clr:tuple,
        font_clrs:list,
        font_size:int,
        parent_groups:list,
        size:list,
        border:list = [-1,(0,0,0),0,"inset"],
        text:str = "",
        font_family:str = "Arial",
        text_align:list = [0,"center"],
        layer:int = 0,
        underline:bool = False,
        living:bool = True
    ):
        """
        text = texte à afficher (retour-chariot permis)
        font_clrs = [*colors:tuples] -> une couleur pour chaque ligne de texte
        font_size -> taille de police
        font_family -> police. Entrer soit le nom d'une police, soit un chemin absolu en partant du dossier 'fonts'
        underline -> permet de souligner ou nom le texte
        text_align [distance_bord:int,mode:str] -> center ou left. quand 'left' est renseignée, distance_bord est la distance entre le bord de la box et le texte (comme le padding en html-css)
        size = [x:int, y:int] -> taille voulue

        Pour des informations sur d'autres attributs, se référer à la docu de Box.__init__()
        """

        self.underline = underline
        self.text_align = text_align
        self.texte = text
        self.font_clrs = font_clrs
        self.font_size = font_size
        self.font_family = font_family

        for i,clr in enumerate(self.font_clrs):
            self.font_clrs[i] = list(self.font_clrs[i])
            if len(clr) != 4:
                self.font_clrs[i].append(255)

        super().__init__(
            winsize = winsize,
            size = size,
            loc = loc,
            background_clr = background_clr,
            border = border,
            living = living,
            layer = layer,
            parent_groups = parent_groups
        )
        


    def calc_image(self,texte = None):
        """
        Recalcul de la surface du sprite
        """

        if not texte:
            texte = self.texte

        if self.font_family.endswith(".ttf"):
            font = pygame.font.SysFont(os.path.join(os.getcwd(),"fonts",self.font_family),round(self.font_size*self.resize_ratio))
        else:
            font = pygame.font.SysFont(self.font_family,round(self.font_size*self.resize_ratio))

        font.set_underline(self.underline)
        textes = texte.split("\n")
        texte_surfaces = []
        for i in range(len(textes)):
            font_clr = [round(j) for j in self.font_clrs[i]]
            texte_surfaces.append(font.render(textes[i],True,font_clr))

        self.text_height = sum([i.get_height() for i in texte_surfaces])
        self.text_width = max([i.get_width() for i in texte_surfaces])
        text_surface = pygame.Surface([
            self.text_width,self.text_height],pygame.SRCALPHA)
        # text_surface.fill((255,0,0,255))

        count_height = 0
        for i in texte_surfaces:
            text_surface.blit(i,i.get_rect(midtop=(self.text_width//2,count_height)))
            count_height += i.get_height()
        if text_surface.get_width() > self.width or text_surface.get_height() > self.height:
            return False

        super().calc_image()
        x,y = self.image.get_rect().center
        if self.text_align[1] == "center":
            text_rect = text_surface.get_rect(center=(x,y))
            self.image.blit(text_surface,text_rect)

        elif self.text_align[1] == "left":
            x = round(x - self.image.get_width()//2 + self.text_align[0])
            text_rect = text_surface.get_rect(midleft=(x,y))
            self.image.blit(text_surface,text_rect)


    def update(self,new_winsize,dt,**args):
        """Actualisation du sprite ayant lieu à chaque changement image"""

        if self.winsize != new_winsize:
            self.rescale(new_winsize)

        self.manage_frames(dt)
            

    def rescale(self, new_winsize):
        """actualisation des valeurs en cas de changement de résolution"""

        super().rescale(new_winsize)
        self.font_size *= self.ratio
        self.text_align[0] *= self.ratio

        self.calc_image()


    def set_text(self,text:str):

        self.texte = text
        self.calc_image()

