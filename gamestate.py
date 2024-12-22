from enum import Enum


class GameState(Enum):
    TITLE_SCREEN = 1
    EDIT_TROOPS = 2
    PLAY_TROOPS = 3
    RESULTS_SCREEN = 4
    DIALOGUE = 5
    EDIT_LEVEL = 6
