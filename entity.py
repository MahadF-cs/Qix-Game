import pygame
from settings import *


class Entity:
    """
    An abstract class representing all of the games entities

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
        screen (pygame.display): Screen that icon is being displayed on
    """
    # Private Attributes:
    #   _icon_path (str): Contains icon file path

    x: int
    y: int
    icon: pygame.Surface

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the entity with the  <icon> and given <x> and <y> position on the game.
        """
        self.x = x
        self.y = y
        self.set_icon("resources/sprite_black.png")

    def set_icon(self, path: str) -> None:
        """
        Sets <icon> to given file path
        """
        self.icon = pygame.image.load(path)

    def draw(self, screen: pygame.display) -> None:
        """
        Draw the entity at its <x> and <y> coordinates
        """
        # Set x, y, width and height of the tile rectangle
        tile = pygame.Rect(self.x * TILE_SIZE + BORDER,
                           self.y * TILE_SIZE + BORDER,
                           TILE_SIZE,
                           TILE_SIZE)
        # Update the icon onto the screen
        screen.blit(self.icon, tile)
