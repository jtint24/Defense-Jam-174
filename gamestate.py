from dataclasses import dataclass

from board import Board
from dialogue import Dialogue
from gamemode import GameMode
from level import Level


@dataclass
class GameState:
    board: Board
    game_mode: GameMode
    max_units: int
    bonus_troops: int
    troops_killed: int
    level_name: str
    current_dialogue: Dialogue
    frame_count: int
    placed_units: int

    def data_from_level(self, level: Level):
        self.board = level.board
        self.level_name = level.name
        self.bonus_troops = level.bonus_troops
        self.current_dialogue = level.opening_dialogue

    def data_to_level(self) -> Level:
        level = Level(self.board, self.level_name, self.current_dialogue, self.bonus_troops)
        return level