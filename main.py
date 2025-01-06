import os
from copy import deepcopy
from json import JSONEncoder
from typing import List

import pygame
from pygame import MOUSEBUTTONDOWN, Surface, MOUSEBUTTONUP

import constants
from board import Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, GENERATE_FILE, LOAD_FILE, ENABLE_EDITING
from gamemode import GameMode
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

pygame.display.set_caption("Warchard")
play_button = ImageButton(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, PLAY_IMAGE)

def main():
    levels: List[Level] = []
    clock = pygame.time.Clock()

    running = True
    data_file = "new_levels.json"

    level_idx = 0
    constants.big_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 6)
    constants.small_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 4)
    constants.title_font = pygame.font.Font("resources/fonts/CDStitleUnicaseV.ttf", 8 * 8)
    game_state = GameState(None, GameMode.TITLE_SCREEN, 2, 0, 0, "", None, 0, 0)

    start_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Start Game", constants.big_font)

    def _default(self, obj):
        return getattr(obj.__class__, "serialize", _default.default)()

    _default.default = JSONEncoder().default
    JSONEncoder.default = _default

    if GENERATE_FILE:
        save_levels("levels_converted_1.json", level_data)

    if LOAD_FILE:
        levels = load_levels(data_file)
        if os.path.exists("save.json"):
            save = load_user_state("save.json")
            level_idx = save["Level"]
            game_state.max_units = save["Troops"]

    game_state.data_from_level(levels[level_idx])

    edit_screen = get_edit_screen(play_button)
    dialogue_screen = get_dialogue_screen()
    results_screen = get_results_screen(constants.big_font)
    typing = False
    type_to_level_name = False
    input_string = ""

    while running:
        game_state.frame_count += 1

        render_checkerboard_background(screen, game_state.frame_count)

        if game_state.game_mode == GameMode.TITLE_SCREEN:
            render_title_screen(screen, constants.title_font, start_button)
        elif game_state.game_mode == GameMode.RESULTS_SCREEN:
            results_screen.draw(screen, game_state,levels,level_idx)
        elif game_state.game_mode == GameMode.DIALOGUE:
            dialogue_screen.draw(screen, game_state)
        elif game_state.game_mode == GameMode.EDIT_LEVEL:
            game_state.placed_units = game_state.board.get_number_of_units_by_team(Team.ORANGE)
            edit_screen.draw(screen, game_state)
        else:
            game_state.placed_units = game_state.board.get_number_of_units_by_team(Team.ORANGE)
            edit_screen.common_draw(screen, game_state)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif typing:
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_RETURN:
                        if event.key != pygame.K_BACKSPACE:
                            input_string+=event.unicode
                        else:
                            input_string = levels[level_idx].name[:-1]
                    else:
                        typing = False
                        type_to_level_name = True
            else:
                if event.type == pygame.KEYDOWN:
                    pos = None
                    key = event.key
                    if event.key == pygame.K_MINUS and ENABLE_EDITING:
                        game_state.max_units -= 1
                    elif event.key == pygame.K_EQUALS and ENABLE_EDITING:
                        game_state.max_units += 1
                    elif event.key == pygame.K_ESCAPE:
                        if game_state.game_mode == GameMode.DIALOGUE:
                            game_state.game_mode = GameMode.EDIT_TROOPS
                            game_state.board.animations = []
                            game_state.board.update_strength_defense(game_state.frame_count)
                        elif game_state.game_mode == GameMode.EDIT_TROOPS and ENABLE_EDITING:
                            game_state.game_mode = GameMode.EDIT_LEVEL
                        elif game_state.game_mode == GameMode.EDIT_LEVEL:
                            if len(edit_screen.board_history) > 0:
                                game_state.board = edit_screen.board_history[0]
                                levels[level_idx] = game_state.data_to_level()
                                save_levels(data_file, levels)
                                edit_screen.history_index = 0
                                edit_screen.board_history = []
                            else:
                                levels[level_idx] = game_state.data_to_level()
                                save_levels(data_file, levels)
                            game_state.game_mode = GameMode.EDIT_TROOPS
                    elif key == pygame.K_RETURN:
                        if game_state.game_mode == GameMode.EDIT_LEVEL:
                            new_level = Level(deepcopy(game_state.board), "", None, 2)
                            levels.insert(level_idx+1, new_level)
                            level_idx+=1
                            game_state.data_from_level(levels[level_idx])
                            typing = True
                            input_string = ""
                            type_to_level_name = True
                    elif key == pygame.K_LEFTBRACKET or key == pygame.K_LEFT:
                        if game_state.game_mode == GameMode.EDIT_LEVEL:
                            if level_idx>0:
                                level_idx-=1
                                game_state.data_from_level(levels[level_idx])
                                save_user_state("save.json", {"Level": level_idx, "Troops": game_state.max_units})
                    elif key == pygame.K_RIGHTBRACKET or key == pygame.K_RIGHT:
                        if game_state.game_mode == GameMode.EDIT_LEVEL:
                            if level_idx<len(levels)-1:
                                level_idx+=1
                                game_state.data_from_level(levels[level_idx])
                                save_user_state("save.json", {"Level": level_idx, "Troops": game_state.max_units})
                    elif key == pygame.K_BACKSPACE:
                        if game_state.game_mode == GameMode.EDIT_LEVEL:
                            levels.pop(level_idx)
                            game_state.data_from_level(levels[level_idx])
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if game_state.game_mode == GameMode.TITLE_SCREEN:
                        if start_button.check_click(pos):
                            if game_state.current_dialogue is None:
                                game_state.game_mode = GameMode.EDIT_TROOPS
                                game_state.board.animations = []
                                game_state.board.update_strength_defense(game_state.frame_count)
                            else:
                                game_state.game_mode = GameMode.DIALOGUE
                    elif game_state.game_mode == GameMode.DIALOGUE:
                        game_state.current_dialogue = dialogue_screen.run(pos, event, game_state)

                        if game_state.current_dialogue is None:
                            game_state.game_mode = GameMode.EDIT_TROOPS
                            game_state.board.animations = []
                            game_state.board.update_strength_defense(game_state.frame_count)

                    elif game_state.game_mode == GameMode.RESULTS_SCREEN:
                        next_round_troops = results_screen.next_round_troops
                        if next_round_troops > 0 and results_screen.next_button.check_click(pos):
                            save_user_state("save.json", {"Level": level_idx + 1, "Troops": next_round_troops})
                            level_idx += 1
                            game_state.max_units = next_round_troops
                            game_state.data_from_level(levels[level_idx])
                            if game_state.current_dialogue is None:
                                game_state.game_mode = GameMode.EDIT_TROOPS
                                game_state.board.animations = []
                                game_state.board.update_strength_defense(game_state.frame_count)
                            else:
                                game_state.game_mode = GameMode.DIALOGUE
                    elif game_state.game_mode == GameMode.EDIT_TROOPS:
                        # Calculate row and column from click position
                        col = (pos[0] - ((SCREEN_WIDTH - len(game_state.board.tiles[0]) * TILE_SIZE) // 2)) // TILE_SIZE
                        row = (pos[1] - ((SCREEN_HEIGHT - len(game_state.board.tiles) * TILE_SIZE) // 2)) // TILE_SIZE

                        # Ensure click is within bounds
                        if 0 <= row < len(game_state.board.tiles) and 0 <= col < len(game_state.board.tiles[0]):
                            tile = game_state.board.tiles[row][col]

                            # Add or remove units based on current state
                            if tile.unit is None:
                                if game_state.placed_units < game_state.max_units - game_state.board.units_killed_by_team[Team.ORANGE] and tile.is_free() and tile.is_placeable:
                                    tile.unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                            elif tile.unit.team is Team.ORANGE:
                                tile.unit = None

                        game_state.board.animations = []
                        game_state.board.update_strength_defense(game_state.frame_count)

                        # Check if play button was clicked
                        if play_button.check_click(pos):
                            game_state.board.set_initial_animations(game_state.frame_count)
                            game_state.game_mode = GameMode.PLAY_TROOPS
                elif event.type == pygame.MOUSEMOTION and edit_screen.drag:
                    pos = pygame.mouse.get_pos()
                else:
                    pos = None

                if game_state.game_mode == GameMode.EDIT_LEVEL:
                    edit_screen.run(pos, event, game_state)
                    # Check if play button was clicked
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                        game_state.board.animations = []
                        game_state.board.update_strength_defense(game_state.frame_count)
        if type_to_level_name:
            game_state.level_name = input_string
        # Update board during PLAY_TROOPS phase
        if game_state.game_mode == GameMode.PLAY_TROOPS:
            if game_state.frame_count % 15 == 0:
                update_change = game_state.board.update(game_state.frame_count)

                if not update_change:
                    game_state.troops_killed = game_state.board.units_killed_by_team[Team.ORANGE]
                    game_state.game_mode = GameMode.RESULTS_SCREEN

                elif game_state.board.updates % 10 == 0:
                    game_state.game_mode = GameMode.EDIT_TROOPS
                    game_state.board.animations = []
                    game_state.board.update_strength_defense(game_state.frame_count)

        clock.tick(50)

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