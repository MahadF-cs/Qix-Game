import pygame
from entity import Entity


class Tile(Entity):
    """
    A class representing the Tile in the game

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
        icon (str): the file path containing the image representing this entity
        captured (bool): True iff tile is captured
    """
    x: int
    y: int
    icon: pygame.Surface
    captured: bool

    def __init__(self, x, y) -> None:
        """
        Initialize the entity with the  <icon_file> and given <x> and <y> position on the game.
        """
        super().__init__(x, y)
        self.set_icon("../images/sprite_unclaimed.png")
        self.captured = False

    def capture(self) -> None:
        """
        Changes the Tile status to captured updating its icon
        """
        self.captured = True
        self.set_icon("../images/sprite_claimed.png")
