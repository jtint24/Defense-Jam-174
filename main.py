from enum import Enum
from typing import NamedTuple, List, Optional, Self

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from tile_images import GRASS_IMAGE, WATER_IMAGE, ORANGE_IMAGE


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4


class UnitType(Enum):
    NORMAL = ORANGE_IMAGE


class Unit:
    def __init__(self, type: UnitType, direction: Direction):
        self.type = type
        self.direction = direction


class TileTypeData(NamedTuple):
    is_passable: bool
    image: pygame.Surface
    char_code: str


class TileType(Enum):
    GRASS = TileTypeData(True, GRASS_IMAGE, "G")
    WATER = TileTypeData(False, WATER_IMAGE, "W")

    @classmethod
    def from_str(cls, name: str):
        for tile_type in TileType:
            if tile_type.value.char_code == name:
                return tile_type


class Tile:
    def __init__(self, type: TileType, unit: Optional[Unit]):
        self.type = type
        self.unit = unit

    def is_free(self) -> bool:
        "Returns whether the tile is clear to walk on, based on tile type and other units on it"
        return self.type.value.is_passable and self.unit is None


class Board:
    def __init__(self, tiles: List[List[Tile]]):
        self.tiles = tiles

    @staticmethod
    def row_from_string(row_str: str) -> List[Tile]:
        return [
            Tile(TileType.from_str(code), None)
            for code in row_str
        ]

    @classmethod
    def from_string(cls, board_strs: List[str]) -> Self:
        return Board([cls.row_from_string(row_str) for row_str in board_strs])

    def render(self):
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                screen.blit(tile.type.value.image, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))
                if tile.unit is not None:
                    screen.blit(tile.unit.type.value, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

    def update(self):
        # Start by populating new_tiles with the base tiles (not units) from the current board
        new_tiles = [
            [
                Tile(tile.type, None)
                for tile in row
            ]
            for row in self.tiles
        ]

        # Then, place units in their new positions, detecting collisions where they exist

        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                if tile.unit is not None:

                    faced_tile = self.get_faced_tile(row_idx, col_idx)

                    # If the faced tile is clear to walk on, the unit just moves ahead.

                    if faced_tile is not None and faced_tile.is_free():
                        faced_tile.unit = tile.unit
                        tile.unit = None

                    # Add logic for collisions w/ other units or obstacles...



    def resolve_conflict(self, row_idx: int, col_idx: int):
        pass

    def get_faced_tile(self, row_idx: int, col_idx: int) -> Optional[Tile]:
        """
        Gets the tile faced by a unit at a row, col. If the tile faces the edge, gives None
        """

        facing_tile = self.tiles[row_idx][col_idx]

        if facing_tile.unit.direction == Direction.RIGHT:
            row_idx, col_idx = row_idx, col_idx + 1
        elif facing_tile.unit.direction == Direction.LEFT:
            row_idx, col_idx = row_idx, col_idx - 1
        elif facing_tile.unit.direction == Direction.UP:
            row_idx, col_idx = row_idx - 1, col_idx
        elif facing_tile.unit.direction == Direction.DOWN:
            row_idx, col_idx = row_idx + 1, col_idx

        # Add more logic for different types of units, if necessary...

        if 0 <= row_idx < len(self.tiles) and 0 <= col_idx < len(self.tiles[row_idx]):
            return self.tiles[row_idx][col_idx]
        return None




pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")


def main():
    board = Board.from_string(
        [
            "GGGW",
            "WWWG",
            "WWWWWWW"
        ]
    )

    board.tiles[0][0].unit = Unit(UnitType.NORMAL, Direction.RIGHT)

    board.update()


    running = True
    while running:
        screen.fill((255, 255, 255))
        board.render()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
