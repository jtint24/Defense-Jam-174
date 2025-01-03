from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Self

from board import Board
from dialogue import Dialogue


@dataclass
class Level:
    board: Board
    name: str
    opening_dialogue: Optional[Dialogue]
    bonus_troops: int

    def serialize(self) -> Dict[str, str | int | List[
        List[Dict[str, Optional[Dict[str, int | str]]
        | bool | int | str | Tuple[int]]]] | List[Dict[str, Optional[str]]]]:
        return {"Board": self.board.serialize(), "Name": self.name, "Opening Dialogue": self.opening_dialogue.serialize() if self.opening_dialogue else None, "Bonus Troops": self.bonus_troops}
    @classmethod
    def from_serialized(cls, serialized_data: Dict[str, str | int | List[
        List[Dict[str, Optional[Dict[str, int | str]] | bool | int | str | Tuple[int]]]] | List[Dict[str, Optional[str]]]]) -> Self:
        return Level(
            Board.from_serialized(serialized_data["Board"]),
            serialized_data["Name"],
            Dialogue.from_serialized(serialized_data["Opening Dialogue"]) if serialized_data["Opening Dialogue"] is not None else None,
            serialized_data["Bonus Troops"])

level_data = []
