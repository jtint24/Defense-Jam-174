from dataclasses import dataclass
from typing import Optional

from board import Board, Unit, UnitType, Direction, Team
from dialogue import Dialogue, opening_dialogue
from tile_images import GENERAL_IMAGE, GENERAL_APPLE_IMAGE


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
                "FGGGGGGF",
                "FGGGGGGF",
                "FGWWGGGF",
                "FGGGGGGF",
                "FGGGGGGF",

            ],
            editable_columns={1, 2},
            units={
                (0, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (1, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 4): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (4, 4): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (4, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
            }
        ),
        "The Apple General's Gambit!",
        Dialogue.from_list([
            ("You made it out of that scrape!", GENERAL_IMAGE, None),
            ("But... oh no! It's the sinister general of the apples!", GENERAL_IMAGE, None),
            ("MUAHAHAHA!!! Well, well... if it isn't the stupid and incompetent orange general!", GENERAL_APPLE_IMAGE, None),
            ("Having some corporal fight all your battles for you, hmm??", GENERAL_APPLE_IMAGE, None),
            ("Well let's see how this greenhorn fares against our biggest army yet!", GENERAL_APPLE_IMAGE, None),
        ]),
        bonus_troops=3
    ),
        Level(
        Board.from_string(
            [
                "FGGGLGGF",
                "FGGGLGGF",
                "FGGGLGGF",
                "FGGGLGGF",
                "FGGGGGGF",
                "FGGGGGGF",
            ],
            editable_columns={1, 2},
            units={
                (5, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (4, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (1, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (4, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),

            }
        ),
        "Plinth Panic!",
        Dialogue.from_list([
            ("That general thought he could knock us out? Well he was quite wrong!", GENERAL_IMAGE, None),
            ("But what's this? It seems there are some plinths on this battlefield?", GENERAL_IMAGE, None),
            ("Our troops could break them down, but it might take them a while... A stronger unit would get it down faster!", GENERAL_IMAGE, None),
        ]),
        bonus_troops=2
    ),

]