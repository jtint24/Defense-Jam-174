from enum import Enum
from typing import Self, Optional, NamedTuple, Tuple

import pygame
from pygame import Surface

from tile_images import FINISH_LINE_IMAGE, WATER_IMAGE, GRASS_IMAGE, ORANGE_IMAGE, ORANGE_TROOP_IMAGE, \
    ORANGE_TANK_IMAGE, APPLE_IMAGE, TRAMPOLINE_SLASH, GRAVESTONE_IMAGE, BROKEN_GRAVESTONE_IMAGE, LAVA_IMAGE


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
    ORANGE = "ORANGE"
    APPLE = "APPLE"


def get_image_by_team(team: Team):
    if team == Team.ORANGE:
        return [ORANGE_IMAGE, ORANGE_TROOP_IMAGE, ORANGE_TANK_IMAGE]
    elif team == Team.APPLE:
        return [APPLE_IMAGE]


class Unit:
    def __init__(self, type: UnitType, direction: Direction, team: Team):
        self.type = type
        self.direction = direction
        self.team = team
        self.defense = 1

    def rotate_cw(self):
        match self.direction:
            case Direction.UP:
                self.direction = Direction.RIGHT
            case Direction.RIGHT:
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case _:
                self.direction = Direction.UP

    def rotate_ccw(self):
        match self.direction:
            case Direction.UP:
                self.direction = Direction.LEFT
            case Direction.RIGHT:
                self.direction = Direction.UP
            case Direction.DOWN:
                self.direction = Direction.RIGHT
            case _:
                self.direction = Direction.DOWN

    def get_image(self):
        image_list = get_image_by_team(self.team)
        try:
             retval = image_list[self.type.value - 1]
        except IndexError:
            print("Uh Oh!! Time for moe ASSETTS")
            print(image_list)
            print(self.type)
            retval = APPLE_IMAGE
        if self.team == Team.APPLE:
            match self.direction:
                case Direction.RIGHT:
                    return pygame.transform.flip(retval, True, False)
                case Direction.UP:
                    return pygame.transform.rotate(retval,270)
                case Direction.DOWN:
                    return pygame.transform.rotate(retval,90)
                case _:
                    return retval
        elif self.team == Team.ORANGE:
            match self.direction:
                case Direction.LEFT:
                    return pygame.transform.flip(retval, True, False)
                case Direction.UP:
                    return pygame.transform.rotate(retval, 90)
                case Direction.DOWN:
                    return pygame.transform.rotate(retval, 270)
                case _:
                    return retval


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
    TRAMPOLINE = TileTypeData(True, TRAMPOLINE_SLASH, "T")
    WALL = TileTypeData(False, GRAVESTONE_IMAGE, "L")
    DEADWALL = TileTypeData(True, BROKEN_GRAVESTONE_IMAGE, "D")
    TRAPDOOR = TileTypeData(True, LAVA_IMAGE, "R")
    FINISH_LINE = TileTypeData(True, FINISH_LINE_IMAGE, "F")

    @classmethod
    def from_str(cls, name: str):
        for tile_type in TileType:
            if tile_type.value.char_code == name:
                return tile_type

class Tile:
    def __init__(self, type: TileType, unit: Optional[Unit], is_placeable: bool = True, health:int = 5,
                 rotation:Direction = Direction.RIGHT, destination:Tuple[int] = (0, 0)):
        self.type = type
        self.unit = unit
        self.is_placeable = is_placeable
        self.health = health
        self.rotation = rotation
        self.destination = destination

    def is_free(self) -> bool:
        "Returns whether the tile is clear to walk on, based on tile type and other units on it"
        return self.type.value.is_passable and self.unit is None

    def render(self, screen: Surface, tile_x, tile_y):
        match self.type:
            case TileType.TRAMPOLINE:
                if self.rotation == Direction.RIGHT or self.rotation == Direction.LEFT:
                    screen.blit(self.type.value.image, (tile_x, tile_y))
                else:
                    screen.blit(pygame.transform.flip(self.type.value.image, True, False), (tile_x, tile_y))
            case _:
                screen.blit(self.type.value.image, (tile_x, tile_y))

    def rotate_cw(self):
        match self.rotation:
            case Direction.UP:
                self.rotation = Direction.RIGHT
            case Direction.RIGHT:
                self.rotation = Direction.DOWN
            case Direction.DOWN:
                self.rotation = Direction.LEFT
            case _:
                self.rotation = Direction.UP

    def rotate_ccw(self):
        match self.rotation.rotation:
            case Direction.UP:
                self.rotation = Direction.LEFT
            case Direction.RIGHT:
                self.rotation = Direction.UP
            case Direction.DOWN:
                self.rotation = Direction.RIGHT
            case _:
                self.rotation = Direction.DOWN

    def trampoline_bounce_calculator(self):
        if self.unit is not None and self.type == TileType.TRAMPOLINE:
            if self.rotation == Direction.RIGHT or self.rotation == Direction.LEFT:
                if self.unit.direction == Direction.RIGHT or self.unit.direction == Direction.LEFT:
                    self.unit.rotate_ccw()
                else:
                    self.unit.rotate_cw()
            else:
                if self.unit.direction == Direction.RIGHT or self.unit.direction == Direction.LEFT:
                    self.unit.rotate_cw()
                else:
                    self.unit.rotate_ccw()
    def __eq__(self, other: Self):
        return other is not None and (
            self.type == other.type and
            self.unit == other.unit and
            self.is_placeable == other.is_placeable and
            self.health == other.health and
            self.destination == other.destination and
            self.rotation == other.rotation
        )

