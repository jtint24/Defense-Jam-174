from dataclasses import dataclass
from typing import Optional

from board import Board, Unit, UnitType, Direction, Team
from dialogue import Dialogue, opening_dialogue


@dataclass
class Level:
    board: Board
    name: str
    opening_dialogue: Optional[Dialogue]


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
            editable_columns={1, 2},
            units={
                (1, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 7): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The best level ever",
        opening_dialogue
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
            editable_columns={1, 2},
            units={
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The best level ever",
        Dialogue.from_list([("Good show, jolly good show!", None, None)])
    ),
]