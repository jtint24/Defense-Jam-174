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
            Dialogue.from_serialized(serialized_data["Opening Dialogue"]),
            serialized_data["Bonus Troops"])


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
            ("That general thought he could knock us out? Well he was quite wrong!", DialogueImage.GENERAL_ORANGE, None),
            ("But what's this? It seems there are some plinths on this battlefield?", DialogueImage.GENERAL_ORANGE, None),
            ("Our troops could break them down, but it might take them a while... A stronger unit would get it down faster!", DialogueImage.GENERAL_ORANGE, None),
        ]),
        bonus_troops=2
    ),
        Level(
        Board.from_string(
            [
                "FGGGGGLGGF",
                "FGGGGGLGGF",
                "FGGGGGLGGF",
                "FGGGGGLGGF",
                "FGGGGGGGGF",
                "FGGFFGGGGF",
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
            ("That general thought he could knock us out? Well he was quite wrong!", DialogueImage.GENERAL_ORANGE, None),
            ("But what's this? It seems there are some plinths on this battlefield?", DialogueImage.GENERAL_ORANGE, None),
            ("Our troops could break them down, but it might take them a while... A stronger unit would get it down faster!", DialogueImage.GENERAL_ORANGE, None),
        ]),
        bonus_troops=2
    ),
        Level(
        Board.from_string(
            [

                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",
                "FGGGGGGGGGGGGGGGGF",


            ],
            editable_columns={1, 2},
            units={
                (1, 4): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (2, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 3): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 4): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
                (3, 5): Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE),
            },
        ),
        "The best level ever",
        opening_dialogue,
        bonus_troops=2
    ),

]
