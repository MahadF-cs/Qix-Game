import pygame
from entity import Entity


class Sparx(Entity):
    """
    A class representing the Sparx in the game.

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
        icon (str): the file path containing the image representing this entity
    """
    x: int
    y: int
    icon: pygame.Surface

    def __init__(self, x: int, y: int, direction: bool) -> None:
        """
        Initialize the Player with the  <icon_file> and given <x> and <y> position on the game.
        """

        super().__init__(x, y)
        self.set_icon("../images/sprite_sparx.png")
        # Spawn the Sparx with a clockwise or counter-clockwise direction traversing the <game.map.perimeter> list
        self.clockwise = direction
        if self.clockwise:
            self.x_direction, self.y_direction = 1, 0
        else:
            self.x_direction, self.y_direction = -1, 0

    def move(self, game: 'Game') -> None:
        """
        The Sparx is spawned on the edge of the field and its movement its restricted to its edge. If the Sparx comes
        into contact with the <Player> its movement is then reversed.
        """
        if (self.x, self.y) not in game.map.perimeter:
            (self.x, self.y) = game.map.perimeter[0]

        if (self.x + self.x_direction, self.y + self.y_direction) not in game.map.perimeter:
            if self.x_direction:
                self.x_direction = 0
                if (self.x, self.y - 1) in game.map.perimeter:
                    self.y_direction = -1
                else:
                    self.y_direction = 1
            else:
                self.y_direction = 0
                if (self.x - 1, self.y) in game.map.perimeter:
                    self.x_direction = -1
                else:
                    self.x_direction = 1

        self.x += self.x_direction
        self.y += self.y_direction
