from enum import Enum
from typing import Self, Optional, NamedTuple

import pygame

from tile_images import FINISH_LINE_IMAGE, WATER_IMAGE, GRASS_IMAGE, ORANGE_IMAGE, ORANGE_TROOP_IMAGE, \
    ORANGE_TANK_IMAGE, APPLE_IMAGE


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class UnitType(Enum):
    SOLDIER = 1
    HORSE = 2
    CANNON = 3
    # TANK = 4


class Team(Enum):
    ORANGE = [ORANGE_IMAGE, ORANGE_TROOP_IMAGE, ORANGE_TANK_IMAGE]
    APPLE = [APPLE_IMAGE]


class Unit:
    def __init__(self, type: UnitType, direction: Direction, team: Team):
        self.type = type
        self.direction = direction
        self.team = team
        self.defense = 1

    def get_image(self):
        return self.team.value[self.type.value - 1]

    def __eq__(self, other: Self):
        return other is not None and (
                self.type == other.type and
                self.direction == other.direction and
                self.team == other.team and
                self.defense == other.defense
        )


class TileTypeData(NamedTuple):
    is_passable: bool
    image: pygame.Surface
    char_code: str


class TileType(Enum):
    GRASS = TileTypeData(True, GRASS_IMAGE, "G")
    WATER = TileTypeData(False, WATER_IMAGE, "W")
    FINISH_LINE = TileTypeData(True, FINISH_LINE_IMAGE, "F")

    @classmethod
    def from_str(cls, name: str):
        for tile_type in TileType:
            if tile_type.value.char_code == name:
                return tile_type


class Tile:
    def __init__(self, type: TileType, unit: Optional[Unit], is_placeable: bool = True):
        self.type = type
        self.unit = unit
        self.is_placeable = is_placeable

    def is_free(self) -> bool:
        "Returns whether the tile is clear to walk on, based on tile type and other units on it"
        return self.type.value.is_passable and self.unit is None

    def __eq__(self, other: Self):
        return other is not None and (
            self.type == other.type and
            self.unit == other.unit and
            self.is_placeable == other.is_placeable
        )

