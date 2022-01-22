import pygame

from game import Game
from settings import *


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(pygame.image.load("resources/logo_qix.png"))
    qix = Game(GRIDSIZE, 1, screen)
    qix.run()

username = input("Enter username:")
print("Username is: " + username)