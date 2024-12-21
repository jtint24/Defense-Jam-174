from dataclasses import dataclass
from typing import Optional

from board import Board, Unit, UnitType, Direction, Team
from dialogue import Dialogue, opening_dialogue


@dataclass
class Level:
    board: Board
    name: str
    opening_dialogue: Optional[Dialogue]
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
        opening_dialogue,
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
        Dialogue.from_list([("Good show, jolly good show!", None, None)]),
        bonus_troops=4
    ),
]