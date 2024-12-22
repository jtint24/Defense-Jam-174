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
            "FGGGLLGF",
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
            (5, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),

        }
        ),
        "Plinth Panic!",
        Dialogue.from_list([
            ("That general thought he could knock us out? Well he was quite wrong!", GENERAL_IMAGE, None),
            ("But what's this? It seems there are some plinths on this battlefield?", GENERAL_IMAGE, None),
            ("Our troops could break them down, but they look tough... A stronger unit would get it down faster!", GENERAL_IMAGE, None),
            ("It might take them quite a while. I'll ^pause the action every 10 turns, to allow you to place down more troops if you need to!", GENERAL_IMAGE, None)
        ]),
        bonus_troops=2
    ),
    Level(
    Board.from_string(
        [
            "FWGGGGGDDGGGGF",
            "FGGGGGDGDGLGGF",
            "FGGGGLGGGGLGGF",
            "FGGGGLGGGDGGGF",
            "FGGGGLGGDDGGGF",
        ],
        editable_columns={1, 2, 3},
        units={
            (0, 9): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (2, 11): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 10): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 7): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (0, 12): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 11): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (2, 12): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 11): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 12): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),

        }
        ),
        "Skirmish at the Ruins!",
        None,
        bonus_troops=3
    ),

Level(
    Board.from_string(
        [
            "FGGGGGGGGGLGGF",
            "FGGGGWGGGGLGGF",
            "FGGGGGGGGGLGGF",
            "FGGGGGLGGGLGGF",
            "FGGGGGLGGGLGGF",
        ],
        editable_columns={1, 2, 3},
        units={
            (0, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (2, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (0, 12): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 11): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (2, 12): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 11): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 12): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),

        }
        ),
        "Voyage of the Dam!",
        Dialogue.from_list(
            [
                ("You've really improved! We'll best those apples yet!", GENERAL_IMAGE, None),
                ("Really? Because I think you still ^stink!", GENERAL_APPLE_IMAGE, None),
                ("Apple general! Don't you think you've done enough?", GENERAL_IMAGE, None),
                ("Don't you think YOU'VE done enough?", GENERAL_APPLE_IMAGE, None),
                ("I fail to see how that's a response to me...", GENERAL_IMAGE, None),
                ("YOU ARE OLD AND STUPID! I'll dispatch your corporal, then you!", GENERAL_APPLE_IMAGE, None),
                ("Just try taking out THIS army!", GENERAL_APPLE_IMAGE, None),
            ]
        ),
        bonus_troops=3
    ),

    Level(
    Board.from_string(
        [
            "FWGGGGGGGGGGGF",
            "FGGGGGGGGGRGGF",
            "FGGGGGGGGGRGGF",
            "FGGGGGGGGGRGGF",
            "FWGGGGGGGGGGGF",
        ],
        editable_columns={1, 2, 3},
        units={
            (1, 9): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 9): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (2, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
        }
        ),
        "Magma Melee!",
        Dialogue.from_list(
            [
                ("Blast! There seems to be lava on the field!", GENERAL_IMAGE, None),
                ("Those apples are up to their old tactics yet again... any troops that walk into it will surely be lost.", GENERAL_IMAGE, None),
                ("But how shall we battle in this environment? ", GENERAL_IMAGE, None),
            ]
        ),
        bonus_troops=3
    ),

Level(
    Board.from_string(
        [
            "FGGGGGGGRGGGF",
            "FGGGGGGGRGGGF",
            "FGGGGLGGGGGGF",
            "FGGGGLGGGGGGF",
            "FGGGGLGGGGGGF",
            "FWGGGGGGGGGGF",
        ],
        editable_columns={1, 2, 3, 4},
        units={
            (0, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 6): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (0, 7): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (1, 7): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (3, 8): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 7): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (5, 10): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (5, 9): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 10): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            (4, 9): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),

        }
        ),
        "The Final Battle",
        Dialogue.from_list(
            [
                ("Hmm... the final battle!", GENERAL_IMAGE, None),
                ("But that means...", GENERAL_IMAGE, None),
                ("That's right, you old man! I'm here!", GENERAL_APPLE_IMAGE, None),
                ("I'm throwing all my remaining troops at you!", GENERAL_APPLE_IMAGE, None),
                ("You and your corporal should prepare to face your demise!", GENERAL_APPLE_IMAGE, None),
            ]
        ),
        bonus_troops=3
    ),





]