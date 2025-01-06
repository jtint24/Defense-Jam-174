from dataclasses import dataclass

from board import Board
from dialogue import Dialogue
from gamemode import GameMode


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
