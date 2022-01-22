import pygame
import math
from tile import Tile
from wire import Wire
from settings import *


class Map:
    """
    A class that handles map functionality

    Attributes:
        size(int): the length of the square map
        tiles(list(list)): matrix of the tiles
        perimeter list(tuples)): contains the coordinates of the captured perimeter
        wires List(wire): list of wire entities
        wire_coordinates list(tuples): list wire coordinates
    """

    size: int
    tiles: list
    perimeter: list
    wires: list
    wire_coordinates: list

    def __init__(self, size: int) -> None:
        """
        Initialize the field map with the given <size>. Populate all respective attributes with their in-game default
        states.
        """
        # Initialize class attributes
        self.size = size
        self.tiles = []
        self.perimeter = []
        self.wires = []
        self.wire_coordinates = []

        # Populate <tiles> attribute with tile objects
        for y in range(size):
            row = []
            for x in range(size):
                row.append(Tile(x, y))
            self.tiles.append(row)

        # Set edges of tiles to be captured and include them into the initial perimeter
        for i in range(self.size):
            self.tiles[i][0].capture()
        for i in range(1, self.size - 1):
            self.tiles[self.size - 1][i].capture()
        for i in range(self.size - 1, -1, -1):
            self.tiles[i][self.size - 1].capture()
        for i in range(self.size - 2, 0, -1):
            self.tiles[0][i].capture()

        self.get_perimeter()

    def push(self, x: int, y: int) -> None:
        """
        Builds wire along the players path while they are travelling the uncaptured territory
        """
        # Disregards invalid inputs and updates <wire> and <wire_coordinates> accordingly
        if (x, y) not in self.wire_coordinates:
            self.wires.append(Wire(x, y))
            self.wire_coordinates.append((x, y))

    def draw(self, screen: pygame.display) -> None:
        """
        Draws <tiles> and <wires> onto <screen> with their updated captured status
        """
        # Draws all field tiles onto screen
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)
        # Draws all wires onto screen
        for wire in self.wires:
            wire.draw(screen)

    def capture_percentage(self) -> int:
        """
        Returns current capture percentage of the field as a percentage of captured / total.
        """
        # Sum of all captured tiles
        total = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.is_captured(i, j):
                    total += 1

        # Current captured percentage rounded down to the nearest ones
        return math.floor((total / self.size ** 2) * 100)

    def is_captured(self, x: int, y: int) -> bool:
        """
        Returns true iff Tile at <x> and <y> coordinate is captured
        """
        # Disregard invalid input and returns their respective captured status
        if x in range(self.size) and y in range(self.size):
            return self.tiles[y][x].captured
        return True

    def get_perimeter(self) -> None:
        """
        Updates <perimeter> tuples with new coordinates of captured tiles that are adjacent to uncaptured tiles
        """
        self.perimeter = []
        # Iterate through matrix
        for y in range(self.size):
            for x in range(self.size):
                # Check if current tile is captured
                if self.is_captured(x, y):
                    # Coordinates of adjacent tiles
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            # Checks if adjacent tiles are uncaptured
                            if not self.is_captured(x + i, y + j) and (x, y) not in self.perimeter:
                                self.perimeter.append((x, y))
                                break

    def capture_field(self) -> None:
        """
        Decides and captures the field with the smallest percentage. Updates <tiles> with each specific tiles
        <captured> status
        """
        # Sets all tiles along the wire to captured
        for wire in self.wires:
            self.tiles[wire.y][wire.x].capture()

        # Orientation of wire when leaving <perimeter>
        direction = (self.wires[0].x - self.wires[1].x, self.wires[0].y - self.wires[1].y)

        # Boolean matrix of <tiles> with each tiles respective captured status for faster performance
        temp_tiles_left = [[False for x in range(self.size)] for x in range(self.size)]
        temp_tiles_right = [[False for x in range(self.size)] for x in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                temp_tiles_left[j][i] = self.is_captured(i, j)
                temp_tiles_right[j][i] = self.is_captured(i, j)

        # Flood fill both matrices from two different starting points
        if direction[0]:
            self.flood_fill(temp_tiles_left, self.wires[1].x, self.wires[1].y + 1)
            self.flood_fill(temp_tiles_right, self.wires[1].x, self.wires[1].y - 1)
        else:
            self.flood_fill(temp_tiles_left, self.wires[1].x + 1, self.wires[1].y)
            self.flood_fill(temp_tiles_right, self.wires[1].x - 1, self.wires[1].y)

        # The resulting percentage of each flood fill
        count_left = self._captured_count(temp_tiles_left)
        count_right = self._captured_count(temp_tiles_right)

        # Chooses smaller percentage and updates respective tiles in the flood fill
        if count_left < count_right:
            for i in range(self.size):
                for j in range(self.size):
                    if temp_tiles_left[i][j]:
                        self.tiles[i][j].capture()
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if temp_tiles_right[i][j]:
                        self.tiles[i][j].capture()

        # Update perimeter and remove all wires
        self.get_perimeter()
        self.wires = []
        self.wire_coordinates = []

    def _captured_count(self, matrix: list) -> int:
        """
        Returns the current percentage of the field that is captured. Only works with boolean matrices
        """
        # Sum of captured tiles
        curr = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j]:
                    curr += 1

        return curr

    def flood_fill(self, matrix: list, x: int, y: int) -> None:
        """
        Fills boolean matrices at given <x> and <y> coordinates. Adapted from the following source:
        https://stackoverflow.com/questions/19839947/flood-fill-in-python
        """
        if not matrix[y][x]:
            matrix[y][x] = True
            # recursively invoke flood fill on all surrounding cells:
            self.flood_fill(matrix, x - 1, y)
            self.flood_fill(matrix, x + 1, y)
            self.flood_fill(matrix, x, y - 1)
            self.flood_fill(matrix, x, y + 1)
