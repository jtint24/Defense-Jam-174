from typing import List, Tuple

import pygame
from pygame import Surface
from pygame.font import Font

from board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from gamemode import GameMode
from level import Level
from ui import GameScreen, TextButton
from unit import Team

write_moratorium = False


class ResultsScreen(GameScreen):
    def __init__(self, next_button: TextButton):
        self.next_button = next_button
        self.next_round_troops = 0

    def draw(self, screen: Surface, board: Board, current_game_state: GameMode, frame_count: int, levels: List[Level], level_idx: int, max_units: int, title_font: Font, big_font: Font):

        bonus_troops = levels[level_idx].bonus_troops
        board = levels[level_idx].board
        troops_killed = board.units_killed_by_team[Team.ORANGE]
        success = board.finished_units_by_team[Team.ORANGE] > board.finished_units_by_team[Team.APPLE]
        self.next_round_troops = max_units + (bonus_troops if success else 0) - troops_killed

        result_text = "SUCCESS!" if success else "FAILURE!"
        result_color = (106, 190, 48) if success else (172, 50, 50)
        result_surface = title_font.render(result_text, False, result_color)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(result_surface, result_rect)

        lines = [
            f"Base Troops: {max_units}",
            f"Clear Bonus: {bonus_troops if success else 0}",
            f"Killed Troops: {-troops_killed}",
            f"Troops for Next Round: {self.next_round_troops}",
            "Game over!" if self.next_round_troops <= 0 else ""
        ]

        # Render and display each line
        y_offset = SCREEN_HEIGHT // 3
        line_spacing = 40

        for i, text in enumerate(lines):
            if text:  # Only render non-empty lines
                line_surface = big_font.render(text, False, (0, 0, 0))
                line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * line_spacing))
                screen.blit(line_surface, line_rect)

        # Show "Next Level" button only if the game is not over
        if self.next_round_troops > 0 and len(levels) > level_idx + 1:
            self.next_button.draw(screen)

    def run(self, pos: Tuple[int, int], key: int, board: Board):
        pass


def get_results_screen(big_font: Font):
    next_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Next Level",
                             big_font)  # Define next button
    return ResultsScreen(next_button)
