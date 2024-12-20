from enum import Enum
from typing import NamedTuple, List, Optional

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from tile_images import GRASS_IMAGE, WATER_IMAGE, ORANGE_IMAGE


class UnitType(Enum):
    NORMAL = ORANGE_IMAGE


class Unit:
    def __init__(self, type: UnitType):
        self.type = type


class TileType(Enum):
    GRASS = GRASS_IMAGE
    WATER = WATER_IMAGE


class Tile:
    def __init__(self, type: TileType, unit: Optional[Unit]):
        self.type = type
        self.unit = unit


class Board:
    def __init__(self, tiles: List[List[Tile]]):
        self.tiles = tiles

    def render(self):
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                screen.blit(tile.type.value, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))
                if tile.unit is not None:
                    screen.blit(tile.unit.type.value, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

    def update_frames(self):
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                pass

    def advance_unit(self, row_idx: int, col_idx: int):
        self.tiles[row_idx][col_idx+1].unit = self.tiles[row_idx][col_idx].unit
        self.tiles[row_idx][col_idx].unit = None


pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")


def main():
    board = Board(tiles=[
        [Tile(TileType.GRASS, Unit(UnitType.NORMAL)), Tile(TileType.WATER, None), Tile(TileType.GRASS, None)],
        [Tile(TileType.WATER, Unit(UnitType.NORMAL)), Tile(TileType.GRASS, None), Tile(TileType.WATER, None)],
        [Tile(TileType.GRASS, Unit(UnitType.NORMAL)), Tile(TileType.GRASS, None), Tile(TileType.GRASS, None)],
    ])

    board.advance_unit(0, 1)

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
