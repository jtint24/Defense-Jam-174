from dataclasses import dataclass
from typing import Optional

from board import Board, Unit, UnitType, Direction, Team
from dialogue import Dialogue, opening_dialogue
from tile_images import GENERAL_IMAGE


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
            editable_columns={1, 2},
            units={
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 4): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            },
        ),
        "The First Challenge!",
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
            editable_columns={1, 2},
            units={
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The Battle of the Pond!",
         Dialogue.from_list([
             ("Good show, jolly good show!", GENERAL_IMAGE, None),
             ("And now our ranks have grown! I'll let you tackle this challenge on your own.", GENERAL_IMAGE, None),
         ]),
        bonus_troops=2
    ),
    Level(
        Board.from_string(
            [
                "FGGGGGGGF",
                "FGGGGGGGF",
                "FGGGGGGGF",
                "FGGGGGGGF",
                "FGGGGGGGF",

            ],
            editable_columns={1, 2},
            units={
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The Battle of the Pond!",
        Dialogue.from_list([
            ("Good show, jolly good show!", GENERAL_IMAGE, None),
            ("And now our ranks have grown! I'll let you tackle this challenge on your own.", GENERAL_IMAGE, None),
        ]),
        bonus_troops=2
    ),
]