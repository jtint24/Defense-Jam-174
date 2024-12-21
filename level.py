from dataclasses import dataclass

from board import Board, Unit, UnitType, Direction, Team


@dataclass
class Level:
    board: Board
    name: str
    bonus_troops: int


levels = [
    Level(
        Board.from_string(
            [
                "FGGWWWGGF",
                "FGGGGGGGF",
                "FGGGGGGGF",
                "FGGGGGGGF",
                "FGGWWWGGF",

            ],
            editable_columns={1, 2, 3},
            units={
                (1, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 7): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            },
        ),
        "The best level ever",
        bonus_troops=2
    ),
    Level(
        Board.from_string(
            [
                "FGGWWWGGF",
                "FGGGGGGGF",
                "FGGGWGGGF",
                "FGGGGGGGF",
                "FGGWWWGGF",

            ],
            editable_columns={1, 2, 3},
            units={
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The best level ever",
        bonus_troops=3
    ),
    Level(
        Board.from_string(
            [
                "FGGWWWWWGGF",
                "FGGGGGGGGGF",
                "FGGGGGWGGGF",
                "FGGGGGGGGGF",
                "FGGWWWWWGGF",

            ],
            editable_columns={1, 2},
            units={
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The best level ever electric boogalo",
        bonus_troops=4
    ),
]