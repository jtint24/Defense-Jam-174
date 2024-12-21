from dataclasses import dataclass

from board import Board, Unit, UnitType, Direction, Team


@dataclass
class Level:
    board: Board
    name: str


level_1 = Level(
    Board.from_string(
        [
            "FGGWWWGGF",
            "FGGGGGGGF",
            "FGGGGGGGF",
            "FGGGGGGGF",
            "FGGGGGGGF",
            "FGGGGGGGF",

        ],
        editable_columns={1, 2},
        units={
            (2, 1): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
        }
    ),
    "The best level ever"
)