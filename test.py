import pygame

pygame.display.init()
pygame.display.set_mode((200,120))

image = pygame.image.load("images/cartes/hidden.png").convert()
print(image.get_bitsize())