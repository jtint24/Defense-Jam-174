from enum import Enum
from typing import NamedTuple, List, Optional, Self

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from tile_images import GRASS_IMAGE, WATER_IMAGE, ORANGE_IMAGE


class UnitType(Enum):
    NORMAL = ORANGE_IMAGE


class Unit:
    def __init__(self, type: UnitType):
        self.type = type


class TileTypeData(NamedTuple):
    is_passable: bool
    image: pygame.Surface
    char_code: str
    health: int = -1


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

    def update_frames(self):
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                pass

    def advance_unit(self, row_idx: int, col_idx: int):
        if col_idx+1 < len(self.tiles[row_idx]):
            self.tiles[row_idx][col_idx+1].unit = self.tiles[row_idx][col_idx].unit
            self.tiles[row_idx][col_idx].unit = None


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

    board.advance_unit(0, 2)

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
