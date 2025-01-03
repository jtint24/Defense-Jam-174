from typing import List

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from level import Level
from main import title_font, big_font, next_button
from unit import Team

write_moratorium = False

def render_calculate_outcome(levels: List[Level], level_idx: int, max_units: int, screen: pygame.Surface) -> int:
    bonus_troops = levels[level_idx].bonus_troops
    board = levels[level_idx].board
    troops_killed = board.units_killed_by_team[Team.ORANGE]
    success = board.finished_units_by_team[Team.ORANGE] > board.finished_units_by_team[Team.APPLE]

    next_round_troops = max_units + (bonus_troops if success else 0) - troops_killed

    result_text = "SUCCESS!" if success else "FAILURE!"
    result_color = (106, 190, 48) if success else (172, 50, 50)
    result_surface = title_font.render(result_text, False, result_color)
    result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(result_surface, result_rect)

    lines = [
        f"Base Troops: {max_units}",
        f"Clear Bonus: {bonus_troops if success else 0}",
        f"Killed Troops: {-troops_killed}",
        f"Troops for Next Round: {next_round_troops}",
        "Game over!" if next_round_troops <= 0 else ""
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
    if next_round_troops > 0 and len(levels) > level_idx + 1:
        next_button.draw(screen)

    return next_round_troops