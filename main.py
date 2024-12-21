from enum import Enum
from time import time
from typing import NamedTuple, List, Optional, Self, Tuple, Set, Dict

import pygame
from pygame import MOUSEBUTTONDOWN

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from gamestate import GameState
from level import level_1
from tile_images import PLAY_IMAGE
from ui import ImageButton


pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")


def main():
    play_button = ImageButton(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, PLAY_IMAGE)
    font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 6)

    current_game_state = GameState.EDIT_TROOPS
    frame_count = 0
    running = True

    board = level_1.board

    # Maximum number of units allowed
    max_units = 2
    bonus_troops = 2  # Bonus for clearing the level
    troops_killed = 0

    while running:
        frame_count += 1
        screen.fill((255, 255, 255))

        if current_game_state == GameState.RESULTS_SCREEN:
            # Determine success or failure
            success = board.finished_units_by_team[Team.ORANGE] > board.finished_units_by_team[Team.APPLE]

            # Calculate troops for next round
            next_round_troops = max_units + (bonus_troops if success else 0) - troops_killed

            result_text = "SUCCESS!" if success else "FAILURE!"
            result_color = (0, 180, 40) if success else (255, 0, 0)
            result_surface = font.render(result_text, False, result_color)
            result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(result_surface, result_rect)

            # Labels for each calculation component
            max_units_text = f"Base Troops: {max_units}"
            clear_bonus_text = f"Clear Bonus: {bonus_troops if success else 0}"
            killed_troops_text = f"Killed Troops: {-troops_killed}"
            next_round_text = f"Troops for Next Round: {next_round_troops}"

            # Render and display each line
            y_offset = SCREEN_HEIGHT // 3
            line_spacing = 40  # Space between each line

            for i, text in enumerate([max_units_text, clear_bonus_text, killed_troops_text, next_round_text]):
                line_surface = font.render(text, False, (0, 0, 0))
                line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + i * line_spacing))
                screen.blit(line_surface, line_rect)


        else:
            # Render the board and UI during EDIT_TROOPS and PLAY_TROOPS phases
            board.render(screen, current_game_state)

            # Draw the play button
            play_button.draw(screen)

            placed_units = board.get_number_of_units_by_team(Team.ORANGE)

            # Render unit counter
            counter_text = f"Units: {placed_units}/{max_units}"
            text_surface = font.render(counter_text, False, (0, 0, 0))
            screen.blit(text_surface, (20, 20))

            # Display finished units by team
            orange_finished_surface = font.render(f"{board.finished_units_by_team[Team.ORANGE]}", False, (0, 0, 0))
            apple_finished_surface = font.render(f"{board.finished_units_by_team[Team.APPLE]}", False, (0, 0, 0))

            screen.blit(apple_finished_surface, (20, ((SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2)))
            screen.blit(orange_finished_surface,
                        (SCREEN_WIDTH - TILE_SIZE + 10, ((SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if current_game_state == GameState.EDIT_TROOPS:
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
                                placed_units += 1
                        elif tile.unit.team is Team.ORANGE:
                            tile.unit = None
                            placed_units -= 1

                    # Check if play button was clicked
                    if play_button.check_click(pos):
                        current_game_state = GameState.PLAY_TROOPS

        pygame.time.delay(20)

        # Update board during PLAY_TROOPS phase
        if current_game_state == GameState.PLAY_TROOPS:
            if frame_count % 10 == 0:
                update_change = board.update()
                if not update_change:
                    troops_killed = board.units_killed_by_team[Team.ORANGE]  # Replace with your method
                    current_game_state = GameState.RESULTS_SCREEN

    pygame.quit()


if __name__ == "__main__":
    main()
