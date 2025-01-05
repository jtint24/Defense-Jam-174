import os
from copy import deepcopy
from typing import Optional, List

import pygame
from pygame import MOUSEBUTTONDOWN, Surface

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, GENERATE_FILE, LOAD_FILE, ENABLE_EDITING
from gamestate import GameState
from level import Level, level_data
from mode_screens.dialogue_mode import get_dialogue_screen
from mode_screens.edit_mode import get_edit_screen
from mode_screens.result_mode import get_results_screen
from savedata import save_levels, load_levels, save_user_state, load_user_state
from tile_images import PLAY_IMAGE, ORANGE_BG
from title import render_title_screen
from ui import ImageButton, TextButton

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

big_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 6)
small_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 4)
title_font = pygame.font.Font("resources/fonts/CDStitleUnicaseV.ttf", 8 * 8)

pygame.display.set_caption("Warchard")

play_button = ImageButton(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, PLAY_IMAGE)
start_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Start Game", big_font)


def main():
    placed_units = 0
    levels: List[Level] = []
    clock = pygame.time.Clock()

    backup_board: Optional[Board] = None

    frame_count = 0
    running = True

    level_idx = 0

    max_units = 2
    bonus_troops = 0  # Bonus for clearing the level
    troops_killed = 0

    if GENERATE_FILE:
        save_levels("levels_converted.json", level_data)

    if LOAD_FILE:
        levels = load_levels("new_levels.json")
        if os.path.exists("save.json"):
            save = load_user_state("save.json")
            level_idx = save["Level"]
            max_units = save["Troops"]

    board = levels[level_idx].board
    level_name = levels[level_idx].name

    current_dialogue = levels[level_idx].opening_dialogue

    current_game_state = GameState.TITLE_SCREEN

    edit_screen = get_edit_screen(play_button)
    dialogue_screen = get_dialogue_screen()
    results_screen = get_results_screen(big_font)

    while running:
        frame_count += 1

        render_checkerboard_background(screen, frame_count)

        if current_game_state == GameState.TITLE_SCREEN:
            render_title_screen(screen, title_font, start_button)
        elif current_game_state == GameState.RESULTS_SCREEN:
            results_screen.draw(screen, board, current_game_state, frame_count, levels, level_idx, max_units, title_font, big_font)
        elif current_game_state == GameState.DIALOGUE:
            dialogue_screen.draw(screen, board, current_game_state, frame_count, current_dialogue, big_font)
        else:
            placed_units = board.get_number_of_units_by_team(Team.ORANGE)

            edit_screen.draw(screen, board, current_game_state, frame_count, level_name, placed_units, max_units, big_font)

        pygame.display.flip()
        key = None


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key

                if event.key == pygame.K_b and ENABLE_EDITING:
                    if backup_board is not None:
                        board = backup_board
                        current_game_state = GameState.EDIT_LEVEL
                elif event.key == pygame.K_MINUS and ENABLE_EDITING:
                    max_units -= 1
                elif event.key == pygame.K_EQUALS and ENABLE_EDITING:
                    max_units += 1
                elif event.key == pygame.K_ESCAPE:
                    if current_game_state == GameState.DIALOGUE:
                        current_game_state = GameState.EDIT_TROOPS
                        board.animations = []
                        board.update_strength_defense(frame_count)
                    elif current_game_state == GameState.EDIT_TROOPS and ENABLE_EDITING:
                        current_game_state = GameState.EDIT_LEVEL
                    elif current_game_state == GameState.EDIT_LEVEL:
                        backup_board = deepcopy(board)
                        levels[level_idx].board = board
                        save_levels("new_levels.json", levels)
                        current_game_state = GameState.EDIT_TROOPS
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if current_game_state == GameState.TITLE_SCREEN:
                    if start_button.check_click(pos):
                        current_game_state = GameState.DIALOGUE
                elif current_game_state == GameState.DIALOGUE:
                    current_dialogue = dialogue_screen.run(pos, key, board, current_dialogue, frame_count)

                    if current_dialogue is None:
                        current_game_state = GameState.EDIT_TROOPS
                        board.animations = []
                        board.update_strength_defense(frame_count)

                elif current_game_state == GameState.RESULTS_SCREEN:
                    next_round_troops = results_screen.next_round_troops

                    if next_round_troops > 0 and results_screen.next_button.check_click(pos):
                        save_user_state("save.json", {"Level": level_idx + 1, "Troops": next_round_troops})
                        level_idx += 1
                        board = levels[level_idx].board
                        level_name = levels[level_idx].name
                        max_units = next_round_troops
                        current_dialogue = levels[level_idx].opening_dialogue
                        if current_dialogue is None:
                            current_game_state = GameState.EDIT_TROOPS
                            board.animations = []
                            board.update_strength_defense(frame_count)
                        else:
                            current_game_state = GameState.DIALOGUE
                elif current_game_state == GameState.EDIT_TROOPS:
                    # Calculate row and column from click position
                    col = (pos[0] - ((SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE) // 2)) // TILE_SIZE
                    row = (pos[1] - ((SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE) // 2)) // TILE_SIZE

                    # Ensure click is within bounds
                    if 0 <= row < len(board.tiles) and 0 <= col < len(board.tiles[0]):
                        tile = board.tiles[row][col]

                        # Add or remove units based on current state
                        if tile.unit is None:
                            if placed_units < max_units - board.units_killed_by_team[Team.ORANGE] and tile.is_free() and tile.is_placeable:
                                tile.unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                        elif tile.unit.team is Team.ORANGE:
                            tile.unit = None

                    board.animations = []
                    board.update_strength_defense(frame_count)

                    # Check if play button was clicked
                    if play_button.check_click(pos):
                        board.set_initial_animations(frame_count)
                        current_game_state = GameState.PLAY_TROOPS

                elif current_game_state == GameState.EDIT_LEVEL:
                    edit_screen.run(pos, key, board)

                    # Check if play button was clicked
                    if play_button.check_click(pos):
                        frame_count += 10
                        board.update(frame_count)

                    board.animations = []
                    board.update_strength_defense(frame_count)


        clock.tick(50)

        # Update board during PLAY_TROOPS phase
        if current_game_state == GameState.PLAY_TROOPS:
            if frame_count % 15 == 0:
                update_change = board.update(frame_count)

                if not update_change:
                    troops_killed = board.units_killed_by_team[Team.ORANGE]
                    current_game_state = GameState.RESULTS_SCREEN

                elif board.updates % 10 == 0:
                    current_game_state = GameState.EDIT_TROOPS
                    board.animations = []
                    board.update_strength_defense(frame_count)


    pygame.quit()



def render_checkerboard_background(screen: Surface, frame_count: int):
    screen.fill((201, 221, 255))

    tile_image = ORANGE_BG

    # Get the screen dimensions and the tile size
    screen_width, screen_height = screen.get_size()
    tile_width, tile_height = tile_image.get_size()
    anim_length = 4*32*2
    for y in range(-screen_height//2, screen_height, tile_height):
        for x in range(-screen_width//2, screen_width, tile_width):
            if ((x // tile_width) % 4 == 0 and y // tile_width % 4 == 0) or ((x // tile_width) % 4 == 2 and y // tile_width % 4 == 2):
                screen.blit(tile_image, (x+(frame_count % anim_length)/2, y+(frame_count % anim_length)/2))


if __name__ == "__main__":
    main()

