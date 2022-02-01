import pygame
from entity import Entity


class Wire(Entity):
    """
    A class representing the wire created by the player in the game

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
        icon (str): the file path containing the image representing this entity
    """
    x: int
    y: int
    icon: pygame.Surface

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the wire with the  <icon_file> and given <x> and <y> position on the game.
        """

        super().__init__(x, y)
        self.set_icon("../images/sprite_wire.png")
