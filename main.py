from enum import Enum
from time import time
from typing import NamedTuple, List, Optional, Self, Tuple, Set, Dict

import pygame
from pygame import MOUSEBUTTONDOWN

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from gamestate import GameState
from level import levels
from tile_images import PLAY_IMAGE
from ui import ImageButton, TextButton

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")


def main():
    big_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 6)
    play_button = ImageButton(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, PLAY_IMAGE)
    next_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Next Level", big_font)  # Define next button

    current_game_state = GameState.EDIT_TROOPS
    frame_count = 0
    running = True

    level_idx = 0

    board = levels[level_idx].board

    max_units = 2
    bonus_troops = 2  # Bonus for clearing the level
    troops_killed = 0
    next_round_troops = -1

    while running:
        frame_count += 1
        screen.fill((255, 255, 255))

        if current_game_state == GameState.RESULTS_SCREEN:
            success = board.finished_units_by_team[Team.ORANGE] > board.finished_units_by_team[Team.APPLE]

            next_round_troops = max_units + (bonus_troops if success else 0) - troops_killed

            result_text = "SUCCESS!" if success else "FAILURE!"
            result_color = (0, 180, 40) if success else (255, 0, 0)
            result_surface = big_font.render(result_text, False, result_color)
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
            if next_round_troops > 0:
                next_button.draw(screen)

        else:
            # Render the board and UI during EDIT_TROOPS and PLAY_TROOPS phases
            board.render(screen, current_game_state, frame_count)

            play_button.draw(screen)

            placed_units = board.get_number_of_units_by_team(Team.ORANGE)

            # Render unit counter
            counter_text = f"Units: {placed_units}/{max_units}"
            text_surface = big_font.render(counter_text, False, (0, 0, 0))
            screen.blit(text_surface, (20, 20))

            # Display finished units by team
            orange_finished_surface = big_font.render(f"{board.finished_units_by_team[Team.ORANGE]}", False, (0, 0, 0))
            apple_finished_surface = big_font.render(f"{board.finished_units_by_team[Team.APPLE]}", False, (0, 0, 0))

            screen.blit(apple_finished_surface, (20, ((SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2)))
            screen.blit(orange_finished_surface,
                        (SCREEN_WIDTH - TILE_SIZE + 10, ((SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if current_game_state == GameState.RESULTS_SCREEN:
                    if next_round_troops > 0 and next_button.check_click(pos):
                        board = levels[level_idx+1].board
                        level_idx += 1
                        max_units = next_round_troops
                        current_game_state = GameState.EDIT_TROOPS

                elif current_game_state == GameState.EDIT_TROOPS:
                    # Calculate row and column from click position
                    col = (pos[0] - ((SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE) // 2)) // TILE_SIZE
                    row = (pos[1] - ((SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE) // 2)) // TILE_SIZE

                    # Ensure click is within bounds
                    if 0 <= row < len(board.tiles) and 0 <= col < len(board.tiles[0]):
                        tile = board.tiles[row][col]

                        # Add or remove units based on current state
                        if tile.unit is None:
                            if placed_units < max_units and tile.is_free() and tile.is_placeable:
                                tile.unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                        elif tile.unit.team is Team.ORANGE:
                            tile.unit = None

                    # Check if play button was clicked
                    if play_button.check_click(pos):
                        current_game_state = GameState.PLAY_TROOPS

        pygame.time.delay(20)

        # Update board during PLAY_TROOPS phase
        if current_game_state == GameState.PLAY_TROOPS:
            if frame_count % 15 == 0:
                update_change = board.update(frame_count)
                if not update_change:
                    troops_killed = board.units_killed_by_team[Team.ORANGE]  # Replace with your method
                    current_game_state = GameState.RESULTS_SCREEN

    pygame.quit()


if __name__ == "__main__":
    main()
