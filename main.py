import os
from copy import deepcopy
from typing import Optional, List

import pygame
from pygame import MOUSEBUTTONDOWN, Surface

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, GENERATE_FILE, LOAD_FILE, ENABLE_EDITING
from gamestate import GameState
from level import Level, level_data
import results_screen
from savedata import save_levels, load_levels, save_user_state, load_user_state
from tile_images import PLAY_IMAGE, ORANGE_BG, GRASS_IMAGE, WATER_IMAGE, TRAMPOLINE_SLASH, GRAVESTONE_IMAGE, \
    BROKEN_GRAVESTONE_IMAGE, LAVA_IMAGE, FINISH_LINE_IMAGE, APPLE_IMAGE, ORANGE_IMAGE
from title import render_title_screen
from ui import ImageButton, TextButton, Screen, HorizontalRadioSelector
from unit import TileType, Tile

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Warchard")

big_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 6)
small_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 4)
title_font = pygame.font.Font("resources/fonts/CDStitleUnicaseV.ttf", 8 * 8)

play_button = ImageButton(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, PLAY_IMAGE)
next_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Next Level", big_font)  # Define next button
start_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Start Game", big_font)

def main():

    build_mode = 1
    placed_units = 0
    levels: List[Level] = []
    clock = pygame.time.Clock()

    backup_board: Optional[Board] = None
    backup_tile: Optional[Tile] = None

    frame_count = 0
    running = True

    level_idx = 0

    max_units = 2
    bonus_troops = 0  # Bonus for clearing the level
    troops_killed = 0
    next_round_troops = -1


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

    element_height = 6

    orange_button = ImageButton(SCREEN_WIDTH - 35 * 20, element_height, 64,
                               64, ORANGE_IMAGE)
    apple_button = ImageButton(SCREEN_WIDTH - 35 * 18, element_height, 64,
                               64, APPLE_IMAGE)

    grass_button = ImageButton(SCREEN_WIDTH - 35 * 16, element_height, 64,
                               64, GRASS_IMAGE)
    water_button = ImageButton(SCREEN_WIDTH - 35 * 14, element_height, 64,
                               64, WATER_IMAGE)
    trampoline_button = ImageButton(SCREEN_WIDTH - 35 * 12, element_height, 64,
                                     64, TRAMPOLINE_SLASH)
    wall_button = ImageButton(SCREEN_WIDTH - 35 * 10, element_height, 64,
                              64, GRAVESTONE_IMAGE)
    remains_button = ImageButton(SCREEN_WIDTH - 35 * 8, element_height,
                                 64, 64, BROKEN_GRAVESTONE_IMAGE)
    lava_button = ImageButton(SCREEN_WIDTH - 35 * 6, element_height, 64,
                              64, LAVA_IMAGE)
    finish_button = ImageButton(SCREEN_WIDTH - 35 * 4, element_height,
                                64, 64, FINISH_LINE_IMAGE)
    tunnel_button = ImageButton(SCREEN_WIDTH - 35 * 2, element_height,
                                64, 64, BROKEN_GRAVESTONE_IMAGE)

    god_mode_editor = HorizontalRadioSelector(
        [
            HorizontalRadioSelector.RadioItem(ORANGE_IMAGE, "orange", pygame.K_1),
            HorizontalRadioSelector.RadioItem(APPLE_IMAGE, "apple", pygame.K_2),
            HorizontalRadioSelector.RadioItem(GRASS_IMAGE, "grass", pygame.K_3),
            HorizontalRadioSelector.RadioItem(WATER_IMAGE, "water", pygame.K_4),
            HorizontalRadioSelector.RadioItem(TRAMPOLINE_SLASH, "trampoline", pygame.K_5),
            HorizontalRadioSelector.RadioItem(GRAVESTONE_IMAGE, "gravestone", pygame.K_6),
            HorizontalRadioSelector.RadioItem(BROKEN_GRAVESTONE_IMAGE, "remains", pygame.K_7),
            HorizontalRadioSelector.RadioItem(LAVA_IMAGE, "lava", pygame.K_8),
            HorizontalRadioSelector.RadioItem(FINISH_LINE_IMAGE, "finish line", pygame.K_9),
            HorizontalRadioSelector.RadioItem(BROKEN_GRAVESTONE_IMAGE, "teleporter", pygame.K_0),
        ],
        SCREEN_WIDTH - 700,
        6,
        SCREEN_WIDTH - 70
    )

    rotate_cw_button = ImageButton(element_height, SCREEN_HEIGHT - 70,64,64, WATER_IMAGE)
    rotate_ccw_button = ImageButton(element_height + 70, SCREEN_HEIGHT - 70, 64, 64, GRASS_IMAGE)

    edit_screen = EditScreen(
        god_mode_editor, rotate_ccw_button, rotate_cw_button
    )

    while running:
        frame_count += 1

        render_checkerboard_background(screen, frame_count)

        if current_game_state == GameState.TITLE_SCREEN:
            render_title_screen(screen, title_font, start_button)
        elif current_game_state == GameState.RESULTS_SCREEN:
            next_round_troops = results_screen.render_calculate_outcome(levels, level_idx, max_units, screen) # REFACTOR!
        elif current_game_state == GameState.DIALOGUE:
            render_dialogue(board, current_game_state, frame_count)

            if current_dialogue is None:
                current_game_state = GameState.EDIT_TROOPS
                board.animations = []
                board.update_strength_defense(frame_count)
            else:
                current_dialogue.render(screen, big_font, frame_count)
        else:
            placed_units = board.get_number_of_units_by_team(Team.ORANGE)

            edit_screen.draw(screen, board, current_game_state, frame_count, level_name, placed_units, max_units)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                element_height = 1
                if event.key == pygame.K_1:
                    build_mode = 11
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 20 - 3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_2:
                    build_mode = 0
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 18 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_3:
                    build_mode = 1
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 16 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_4:
                    build_mode = 2
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 14 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_5:
                    build_mode = 3
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 12 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_6:
                    build_mode = 4
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 10 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_7:
                    build_mode = 5
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 8 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_8:
                    build_mode = 6
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 6 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_9:
                    build_mode = 7
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 4 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_0:
                    build_mode = 8
                    edit_screen.sel_x = SCREEN_WIDTH - 35 * 2 -3
                    edit_screen.sel_y = element_height
                elif event.key == pygame.K_b and ENABLE_EDITING:
                    if backup_board is not None:
                        board = backup_board
                        current_game_state = GameState.EDIT_LEVEL
                elif event.key == pygame.K_MINUS and ENABLE_EDITING:
                    max_units -= 1
                elif event.key == pygame.K_EQUALS and ENABLE_EDITING:
                    max_units += 1
                elif event.key == pygame.K_TAB:
                    if current_game_state == GameState.DIALOGUE:
                        current_dialogue = current_dialogue.next
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
                element_height = 6
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if current_game_state == GameState.TITLE_SCREEN:
                    if start_button.check_click(pos):
                        current_game_state = GameState.DIALOGUE
                elif current_game_state == GameState.DIALOGUE:
                    if current_dialogue.is_complete(frame_count):
                        current_dialogue = current_dialogue.next
                    else:
                        current_dialogue.first_appear_frame = -10000
                    if current_dialogue is None:
                        current_game_state = GameState.EDIT_TROOPS
                        board.animations = []
                        board.update_strength_defense(frame_count)

                elif current_game_state == GameState.RESULTS_SCREEN:
                    if next_round_troops > 0 and next_button.check_click(pos):
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
                    element_height = 1
                    if grass_button.check_click(pos):
                        build_mode = 1
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 16 - 3
                        edit_screen.sel_y = element_height
                    elif water_button.check_click(pos):
                        build_mode = 2
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 14 - 3
                        edit_screen.sel_y = element_height
                    elif trampoline_button.check_click(pos):
                        build_mode = 3
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 12 - 3
                        edit_screen.sel_y = element_height
                    elif wall_button.check_click(pos):
                        build_mode = 4
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 10 - 3
                        edit_screen.sel_y = element_height
                    elif remains_button.check_click(pos):
                        build_mode = 5
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 8 - 3
                        edit_screen.sel_y = element_height
                    elif lava_button.check_click(pos):
                        build_mode = 6
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 6 - 3
                        edit_screen.sel_y = element_height
                    elif finish_button.check_click(pos):
                        build_mode = 7
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 4 - 3
                        edit_screen.sel_y = element_height
                    elif tunnel_button.check_click(pos):
                        build_mode = 8
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 2 - 3
                        edit_screen.sel_y = element_height
                    elif rotate_cw_button.check_click(pos):
                        build_mode = 9
                        edit_screen.sel_x = 1
                        edit_screen.sel_y = SCREEN_HEIGHT - 70 -5
                    elif rotate_ccw_button.check_click(pos):
                        build_mode = 10
                        edit_screen.sel_x = 71
                        edit_screen.sel_y = SCREEN_HEIGHT - 70 - 5
                    elif apple_button.check_click(pos):
                        build_mode = 0
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 18 - 3
                        edit_screen.sel_y = element_height
                    elif orange_button.check_click(pos):
                        build_mode = 11
                        edit_screen.sel_x = SCREEN_WIDTH - 35 * 20 - 3
                        edit_screen.sel_y = element_height
                    elif play_button.check_click(pos):
                        frame_count += 10
                        board.update(frame_count)
                    element_height = 6
                    # Calculate row and column from click position
                    col = (pos[0] - ((SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE) // 2)) // TILE_SIZE
                    row = (pos[1] - ((SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE) // 2)) // TILE_SIZE

                    # Ensure click is within bounds
                    print("Click Pos: " + str(col) + ", " + str(row))
                    if 0 <= row < len(board.tiles) and 0 <= col < len(board.tiles[0]):
                        tile = board.tiles[row][col]
                        # Add or remove units based on current state
                        match build_mode:
                            case 0:
                                if tile.unit is None:
                                    if tile.is_free() and not tile.is_placeable:
                                        tile.unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
                                elif tile.unit.team is Team.ORANGE:
                                    tile.unit = None
                                elif tile.unit.team is Team.APPLE:
                                    tile.unit = None
                            case 1:
                                tile.type = TileType.GRASS
                            case 2:
                                tile.type = TileType.WATER
                            case 3:
                                tile.type = TileType.TRAMPOLINE
                            case 4:
                                tile.type = TileType.WALL
                            case 5:
                                tile.type = TileType.DEADWALL
                            case 6:
                                tile.type = TileType.TRAPDOOR
                            case 7:
                                tile.type = TileType.FINISH_LINE
                            case 8:
                                if tile.type == TileType.TUNNEL:
                                    backup_tile = tile
                                elif backup_tile is not None:
                                    backup_tile.destination = (row, col)
                                    backup_tile = None
                                else:
                                    tile.type = TileType.TUNNEL
                            case 9:
                                if tile.unit is not None:
                                    tile.unit.rotate_cw()
                                elif tile.type == TileType.TRAMPOLINE:
                                    tile.rotate_cw()
                            case 10:
                                if tile.unit is not None:
                                    tile.unit.rotate_ccw()
                                elif tile.type == TileType.TRAMPOLINE:
                                    tile.rotate_ccw()
                            case 11:
                                if tile.unit is None:
                                    if tile.is_free():
                                        tile.unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                                elif tile.unit.team is Team.ORANGE:
                                    tile.unit = None
                                elif tile.unit.team is Team.APPLE:
                                    tile.unit = None

                    board.animations = []
                    board.update_strength_defense(frame_count)

                    # Check if play button was clicked

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


def render_dialogue(board, current_game_state, frame_count):
    board.render(screen, current_game_state, frame_count)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))


class EditScreen(Screen):
    def __init__(self, item_selector: HorizontalRadioSelector, rotate_ccw_button: ImageButton, rotate_cw_button: ImageButton):
        self.item_selector = item_selector
        self.rotate_ccw_button = rotate_ccw_button
        self.rotate_cw_button = rotate_cw_button

    def draw(self, screen: Surface, board: Board, current_game_state: GameState, frame_count: int,
             level_name: str, placed_units: int, max_units: int):
        # Render the board and UI during EDIT_TROOPS and PLAY_TROOPS phases

        board.render(screen, current_game_state, frame_count)
        level_name_surface = big_font.render(level_name, True, (0, 0, 0))
        l_name_rect = level_name_surface.get_rect(
            topleft=(
            (SCREEN_WIDTH - 14 * len(level_name)) // 2, (SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE) // 2 - 60))
        pygame.draw.rect(screen, (255, 255, 255), l_name_rect.inflate(20, 10))
        screen.blit(level_name_surface, l_name_rect)
        play_button.draw(screen)
        counter_text = f"Units: {placed_units}/{max_units - board.units_killed_by_team[Team.ORANGE]}"
        counter_surface = big_font.render(counter_text, True, (0, 0, 0))
        counter_rect = counter_surface.get_rect(topleft=(20, 20))
        pygame.draw.rect(screen, (255, 255, 255), counter_rect.inflate(20, 10))
        screen.blit(counter_surface, counter_rect)
        if current_game_state == GameState.EDIT_LEVEL:
            self.item_selector.draw(screen)
        else:
            # Display finished units by team
            orange_finished_surface = big_font.render(
                f"{board.finished_units_by_team[Team.ORANGE]}", True, (0, 0, 0)
            )
            apple_finished_surface = big_font.render(
                f"{board.finished_units_by_team[Team.APPLE]}", True, (0, 0, 0)
            )

            # Calculate Y-position for team counters
            team_counters_y = (SCREEN_HEIGHT + len(board.tiles) * TILE_SIZE) // 2 + 20

            # Apple team's finished units
            if current_game_state == GameState.PLAY_TROOPS:
                apple_rect = apple_finished_surface.get_rect(
                    topleft=((SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE) // 2, team_counters_y))
                pygame.draw.rect(screen, (255, 255, 255), apple_rect.inflate(20, 10))
                screen.blit(apple_finished_surface, apple_rect)

                # Orange team's finished units
                orange_rect = orange_finished_surface.get_rect(
                    topleft=((SCREEN_WIDTH + len(board.tiles[0]) * TILE_SIZE) // 2, team_counters_y)
                )
                pygame.draw.rect(screen, (255, 255, 255), orange_rect.inflate(20, 10))
                screen.blit(orange_finished_surface, orange_rect)


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


