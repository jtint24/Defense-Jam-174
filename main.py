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

    while running:
        frame_count += 1
        screen.fill((255, 255, 255))

        # Render the board
        board.render(screen, current_game_state)

        # Draw the play button
        play_button.draw(screen)

        placed_units = board.get_number_of_units_by_team(Team.ORANGE)

        # Render unit counter
        counter_text = f"Units: {placed_units}/{max_units}"
        text_surface = font.render(counter_text, False, (0, 0, 0))
        screen.blit(text_surface, (20, 20))

        orange_finished_surface = font.render(f"{board.finished_units_by_team[Team.ORANGE]}", False, (0,0,0))
        apple_finished_surface = font.render(f"{board.finished_units_by_team[Team.APPLE]}", False, (0,0,0))

        screen.blit(apple_finished_surface, (20, ((SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2)))
        screen.blit(orange_finished_surface, (SCREEN_WIDTH-TILE_SIZE+10, ((SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2)))


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
                    current_game_state = GameState.EDIT_TROOPS

    pygame.quit()


if __name__ == "__main__":
    main()
