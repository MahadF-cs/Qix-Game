import pygame
from entity import Entity
from wire import Wire


class Player(Entity):
    """
    A class representing the Player

    Attributes:
        x (int): x coordinate of the entity on the field
        y (int): y coordinate of the entity on the field
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the Player with the  <icon_file> and the given <x> and <y> position on the field.
        """

        super().__init__(x, y)
        self.set_icon("resources/sprite_player.png")

    def move(self, game: 'Game') -> None:
        """
        Move the Player on the field based on the keyboard input. Movement is restricted to outer edge of field if
        not "pushed".
        """
        # Copy previous position
        new_x, new_y = self.x, self.y

        # Update <x> or <y> values based on keyboard input
        if game.key_pressed[pygame.K_LEFT] or game.key_pressed[pygame.K_a]:
            new_x -= 1
        elif game.key_pressed[pygame.K_RIGHT] or game.key_pressed[pygame.K_d]:
            new_x += 1
        elif game.key_pressed[pygame.K_UP] or game.key_pressed[pygame.K_w]:
            new_y -= 1
        elif game.key_pressed[pygame.K_DOWN] or game.key_pressed[pygame.K_s]:
            new_y += 1

        # If space is held
        if game.key_pressed[pygame.K_SPACE]:
            # And moving onto uncaptured territory
            if ((self.x, self.y) in game.map.perimeter and not game.map.is_captured(new_x, new_y) or
                    not (self.x, self.y) in game.map.perimeter and not game.map.is_captured(new_x, new_y))\
                    and (new_x, new_y) not in game.map.wire_coordinates:
                # Initial push
                if not game.map.wires:
                    game.map.wires.append(Wire(self.x, self.y))
                    game.map.wire_coordinates.append((self.x, self.y))
                    self.x, self.y = new_x, new_y
                    game.map.push(self.x, self.y)
                # Following push
                else:
                    self.x, self.y = new_x, new_y
                    game.map.push(self.x, self.y)
            # Returning to captured territory
            if not game.map.is_captured(self.x, self.y) and (new_x, new_y) in game.map.perimeter:
                game.map.capture_field()
                self.x, self.y = new_x, new_y
        # If space is not held
        else:
            # Move along the perimeter
            if (new_x, new_y) in game.map.perimeter and (self.x, self.y) in game.map.perimeter:
                self.x, self.y = new_x, new_y
