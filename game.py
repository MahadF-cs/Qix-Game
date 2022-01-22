import pygame
import random
from map import Map
from player import Player
from qix import Qix
from sparx import Sparx
from settings import *


class Game:
    """
    The is class handles all of the Pygame modules and game rules

    Attributes:
        screen (Pygame): Pygame module displayed screen
        clock (Pygame): Pygame module that sets game frame rate
        key_pressed (Pygame): current key that is being pressed
        map (Map): a Map object containing all of the field information
        player (Player): instance of the player in the game
        sparx_list (list): list of all sparx objects
        qix (Qix): entity that roams around the uncaptured territory
        slow_movement(bool): player moves twice as fast as other entities
    """
    # Private Attibutes:
    #   _playing (bool): True iff the game is playing
    #   _goal_percentage(int): Goal of captured field in current game
    #   _difficulty: the difficulty of the stage
    #   _lives (int): player total lives

    screen: pygame
    clock: pygame
    key_pressed: pygame
    map: Map
    player: Player
    sparx_list: list
    qix: Qix
    slow_movement: bool
    _playing: bool
    _goal_percentage: int
    _difficulty: int
    _lives: int

    def __init__(self, size: int, difficulty: int, screen) -> None:
        """
        Initialize game by setting the field map to <size> and creating the starting level
        """
        # Set screen, frame rate, and current key pressed
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.key_pressed = None

        # Set starting <goal> percentage and difficulty
        self._goal_percentage = 60
        self._difficulty = difficulty

        # Set all entity attributes
        self.sparx_list = []
        self.size = size
        self.qix = None
        self.map = None
        self.slow_movement = True

        self._lives = 3

        # Creates the initial state of a level
        self.set_up_level()

        self._playing = False

    def run(self) -> None:
        """
        Runs game until all lives are lost or the game is exited
        """
        self._playing = True

        while self._playing:
            # Set clock tick rate
            self.clock.tick(7)
            for event in pygame.event.get():
                # Check if game window is closed
                if event.type == pygame.QUIT:
                    self._playing = False
            # Game over if all lives are lost
            if self._lives <= 0:
                self._playing = False

            # Check if minimum goal percentage is met
            if self._goal_percentage <= self.map.capture_percentage():
                # Displays congrats message
                self.screen.blit(pygame.image.load("resources/congratulations.png"), pygame.Rect(207, 282, 250, 100))
                pygame.display.update()
                pygame.time.wait(300)

                # Increases difficulty and resets level
                if self._goal_percentage <= 85:
                    self._goal_percentage += 5
                self._difficulty += 1
                self.set_up_level()

            # Update all entity movement according to their specific <move> and redraw them onto <screen>
            self.update()
            self.draw_background()
            self.draw_entity()

            pygame.display.update()
        pygame.quit()

    def update(self) -> None:
        """
        Updates all entities in the game field depending on eaches movement
        """
        self.key_pressed = pygame.key.get_pressed()
        self.player.move(self)

        # Non-player entities move twice as slow as <player>
        if self.slow_movement:
            self.qix.move(self)
            for sparx in self.sparx_list:
                sparx.move(self)
            self.slow_movement = False
        else:
            self.slow_movement = True

    def draw_background(self) -> None:
        """
        Draws background of game onto <screen>
        """
        pixel_font = pygame.font.Font("resources/game_font.ttf", 40)

        # Sets background
        self.screen.blit(pygame.image.load("resources/background.png"), pygame.Rect(0, 0, WIDTH, HEIGHT))

        # Sets interface along the bottom of <screen>

        # Lives count
        self.screen.blit(pygame.image.load("resources/sprite_player.png"), pygame.Rect(72, 665, 24, 24))
        self.screen.blit(pixel_font.render('x', False,  (238, 236, 222)),(96, 658))
        self.screen.blit(pixel_font.render(str(self._lives), False, (238, 236, 222)), (116, 658))

        # Current level
        self.screen.blit(pixel_font.render('Level:', False, (238, 236, 222)), (169, 658))
        self.screen.blit(pixel_font.render(str(self._difficulty), False, (238, 236, 222)), (249, 658))

        # Current capture percentage
        self.screen.blit(pixel_font.render('Current:', False, (238, 236, 222)), (303, 658))
        self.screen.blit(pixel_font.render(str(self.map.capture_percentage()) + '%', False, (238, 236, 222)), (413, 658))

        # Goal percentage of the level
        self.screen.blit(pixel_font.render('Goal:', False, (238, 236, 222)), (496, 658))
        self.screen.blit(pixel_font.render(str(self._goal_percentage) + '%', False, (238, 236, 222)), (561, 658))

    def draw_entity(self) -> None:
        """
        Draws all entities onto <screen>
        """
        self.map.draw(self.screen)
        self.qix.draw(self.screen)
        self.player.draw(self.screen)

        for sparx in self.sparx_list:
            sparx.draw(self.screen)

    def set_up_level(self) -> None:
        """
        Sets up each level to its initial state
        """
        # Gives times before the level begins
        if self._difficulty != 1:
            pygame.time.wait(1000)

        self.map = Map(self.size)
        # Player is always spawned in the middle of the bottom row
        self.player = Player(12, 24)
        # Qix is spawned randomly in the uncaptured field
        self.qix = Qix(random.randrange(1, 24), random.randrange(1, 24))

        # Sparx is spawned randomly along the perimeter
        self.sparx_list = []
        for sparx in range(self._difficulty):
            location = random.choice(self.map.perimeter)
            if sparx % 2 == 0:
                self.sparx_list.append(Sparx(location[0], location[1], True))
            else:
                self.sparx_list.append(Sparx(location[0], location[1], False))

    def lose_live(self) -> None:
        """
        Reduces the total number of lives by one
        """
        self._lives -= 1
