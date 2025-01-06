from typing import Tuple

import pygame
from pygame import Surface

import constants
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from gamestate import GameState
from ui import GameScreen


class DialogueScreen(GameScreen):
    def __init__(self):
        pass

    def draw(self, screen: Surface, game_state: GameState):
        game_state.board.render(screen, game_state.game_mode, game_state.frame_count)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        if game_state.current_dialogue is not None:
            game_state.current_dialogue.render(screen, constants.big_font, game_state.frame_count)

    def run(self, pos: Tuple[int, int], key: int, game_state: GameState):
        if game_state.current_dialogue is not None:
            if pos:
                if game_state.current_dialogue.is_complete(game_state.frame_count):
                    game_state.current_dialogue = game_state.current_dialogue.next
                else:
                    game_state.current_dialogue.first_appear_frame = -10000
            return game_state.current_dialogue
        return None


def get_dialogue_screen():
    return DialogueScreen()
