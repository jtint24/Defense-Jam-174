from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Self

from board import Board, Unit, UnitType, Direction, Team
from dialogue import Dialogue, opening_dialogue, DialogueImage


@dataclass
class Level:
    board: Board
    name: str
    opening_dialogue: Optional[Dialogue]
    bonus_troops: int

    def serialize(self) -> Dict[str, str | int | List[
        List[Dict[str, Optional[Dict[str, int | str]] | bool | int | str | Tuple[int]]]] | List[Dict[str, Optional[str]]]]:
        return {"Board": self.board.serialize_board(), "Name": self.name, "Opening Dialogue": self.opening_dialogue.serialize() if self.opening_dialogue else None, "Bonus Troops": self.bonus_troops}
    @classmethod
    def from_serialized(cls, serialized_data: Dict[str, str | int | List[
        List[Dict[str, Optional[Dict[str, int | str]] | bool | int | str | Tuple[int]]]] | List[Dict[str, Optional[str]]]]) -> Self:
        return Level(
            Board.from_serialized(serialized_data["Board"]),
            serialized_data["Name"],
            Dialogue.from_serialized(serialized_data["Opening Dialogue"]) if serialized_data["Opening Dialogue"] is not None else None,
            serialized_data["Bonus Troops"])


level_data = [
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
             ("Good show, jolly good show!", DialogueImage.GENERAL_ORANGE, None),
             ("And now our ranks have grown! I'll let you tackle this challenge on your own.", DialogueImage.GENERAL_ORANGE, None),
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
            ("You made it out of that scrape!", DialogueImage.GENERAL_ORANGE, None),
            ("But... oh no! It's the sinister general of the apples!", DialogueImage.GENERAL_ORANGE, None),
            ("MUAHAHAHA!!! Well, well... if it isn't the stupid and incompetent orange general!", DialogueImage.GENERAL_APPLE, None),
            ("Having some corporal fight all your battles for you, hmm??", DialogueImage.GENERAL_APPLE, None),
            ("Well let's see how this greenhorn fares against our biggest army yet!", DialogueImage.GENERAL_APPLE, None),
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
            ("That general thought he could knock us out? Well he was quite wrong!", DialogueImage.GENERAL_ORANGE, None),
            ("But what's this? It seems there are some plinths on this battlefield?", DialogueImage.GENERAL_ORANGE, None),
            ("Our troops could break them down, but they look tough... A stronger unit would get it down faster!", DialogueImage.GENERAL_ORANGE, None),
            ("It might take them quite a while. I'll ^pause the action every 10 turns, to allow you to place down more troops if you need to!", DialogueImage.GENERAL_ORANGE, None)
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
                ("You've really improved! We'll best those apples yet!", DialogueImage.GENERAL_ORANGE, None),
                ("Really? Because I think you still ^stink!", DialogueImage.GENERAL_APPLE, None),
                ("Apple general! Don't you think you've done enough?", DialogueImage.GENERAL_ORANGE, None),
                ("Don't you think YOU'VE done enough?", DialogueImage.GENERAL_APPLE, None),
                ("I fail to see how that's a response to me...", DialogueImage.GENERAL_ORANGE, None),
                ("YOU ARE OLD AND STUPID! I'll dispatch your corporal, then you!", DialogueImage.GENERAL_APPLE, None),
                ("Just try taking out THIS army!", DialogueImage.GENERAL_APPLE, None),
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
                ("Blast! There seems to be lava on the field!", DialogueImage.GENERAL_ORANGE, None),
                ("Those apples are up to their old tactics yet again... any troops that walk into it will surely be lost.", DialogueImage.GENERAL_ORANGE, None),
                ("But how shall we battle in this environment? ", DialogueImage.GENERAL_ORANGE, None),
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
                ("Hmm... the final battle!", DialogueImage.GENERAL_ORANGE, None),
                ("But that means...", DialogueImage.GENERAL_ORANGE, None),
                ("That's right, you old man! I'm here!", DialogueImage.GENERAL_APPLE, None),
                ("I'm throwing all my remaining troops at you!", DialogueImage.GENERAL_APPLE, None),
                ("You and your corporal should prepare to face your demise!", DialogueImage.GENERAL_APPLE, None),
            ]
        ),
        bonus_troops=3
    ),





]
