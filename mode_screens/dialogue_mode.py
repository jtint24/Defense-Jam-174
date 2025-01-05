from typing import Tuple

import pygame
from pygame import Surface
from pygame.font import Font

from board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from dialogue import Dialogue
from gamestate import GameState
from ui import GameScreen


class DialogueScreen(GameScreen):
    def __init__(self):
        pass

    def draw(self, screen: Surface, board: Board, current_game_state: GameState, frame_count: int, current_dialogue: Dialogue, big_font: Font):
        board.render(screen, current_game_state, frame_count)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        if current_dialogue is not None:
            current_dialogue.render(screen, big_font, frame_count)

    def run(self, pos: Tuple[int, int], key: int, board: Board, current_dialogue: Dialogue, frame_count: int):
        if pos:
            if current_dialogue.is_complete(frame_count):
                current_dialogue = current_dialogue.next
            else:
                current_dialogue.first_appear_frame = -10000
        return current_dialogue


def get_dialogue_screen():
    return DialogueScreen()
