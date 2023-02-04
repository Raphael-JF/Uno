import pygame

a = pygame.sprite.Group()
b = pygame.sprite.Sprite()
a.add(b)
print(a)
a.add(b)
print(a)