from enum import Enum
from typing import NamedTuple, List, Optional, Self, Tuple

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

        chains = self.identify_chains()

        for chain in chains:
            for row_idx, col_idx in chain:
                self.move_unit(row_idx, col_idx)

    def resolve_conflict(self, row_idx: int, col_idx: int):
        pass

    def move_unit(self, row_idx: int, col_idx: int):
        pass
    def identify_chains(self) -> List[List[Tuple[int, int]]]:
        chains_starting_points = {}
        identified_unit_points = set()

        # Iterate over all units on the board, finding each ones' chain.
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                if (row_idx, col_idx) in identified_unit_points:
                    continue
                if tile.unit is not None:
                    chain = self.extract_chain(row_idx, col_idx)
                    if chain is not None:
                        identified_unit_points.update(chain)

                        # Remove any smaller subchains that were identified earlier
                        chains_to_remove = set()
                        for starting_point in chains_starting_points:
                            if starting_point in chain:
                                chains_to_remove.add(starting_point)

                        for chain_to_remove in chains_to_remove:
                            chains_starting_points.pop(chain_to_remove)

                        chains_starting_points[(row_idx, col_idx)] = chain

        return list(chains_starting_points.values())



    def extract_chain(self, row_idx: int, col_idx: int) -> Optional[List[Tuple[int, int]]]:
        """
        Returns a chain of units that must move in order, starting from the specified row_idx, col_idx.
        Returns None if the unit cannot move
        """

        faced_tile, f_row_idx, f_col_idx = self.get_faced_tile(row_idx, col_idx)

        if faced_tile is None or not faced_tile.type.value.is_passable:
            return None
        if faced_tile.is_free():
            return [(row_idx, col_idx)]

        # If the faced tile is occupied by a unit that is also free to move next turn, we can move to it

        chain = self.extract_chain(f_row_idx, f_col_idx)
        if chain is not None:
            return chain + [(row_idx, col_idx)]
        else:
            return None


    def get_faced_tile(self, row_idx: int, col_idx: int) -> Tuple[Optional[Tile], int, int]:
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
            return self.tiles[row_idx][col_idx], row_idx, col_idx
        return None, row_idx, col_idx


pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")


def main():
    board = Board.from_string(
        [
            "GGGG",
            "GGGG",
            "GGGG"
        ]
    )

    board.tiles[0][0].unit = Unit(UnitType.NORMAL, Direction.RIGHT)
    board.tiles[0][1].unit = Unit(UnitType.NORMAL, Direction.RIGHT)
    board.tiles[0][2].unit = Unit(UnitType.NORMAL, Direction.RIGHT)
    board.tiles[1][0].unit = Unit(UnitType.NORMAL, Direction.UP)
    board.tiles[2][0].unit = Unit(UnitType.NORMAL, Direction.UP)
    board.tiles[2][1].unit = Unit(UnitType.NORMAL, Direction.LEFT)
    board.tiles[2][2].unit = Unit(UnitType.NORMAL, Direction.LEFT)
    board.tiles[1][2].unit = Unit(UnitType.NORMAL, Direction.DOWN)

    print(board.identify_chains())

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
