from copy import deepcopy
from typing import Optional, Tuple, List

import pygame
from pygame import Surface

import constants
from board import Board
from constants import SCREEN_WIDTH, TILE_SIZE, SCREEN_HEIGHT
from gamestate import GameState
from tile_images import ORANGE_IMAGE, ROTATE_CCW_IMAGE, ROTATE_CW_IMAGE, APPLE_IMAGE, GRASS_IMAGE, WATER_IMAGE, \
    TRAMPOLINE_SLASH, GRAVESTONE_IMAGE, BROKEN_GRAVESTONE_IMAGE, LAVA_IMAGE, FINISH_LINE_IMAGE, PLAY_IMAGE
from ui import RadioButtons, GameScreen, HorizontalRadioSelector, RadioMeta, ImageButton
from unit import TileType, Team, UnitType, Direction, Unit, Tile


class EditScreen(GameScreen):
    def __init__(self, item_selector: RadioButtons, play_button: ImageButton, board_history: List[Board] = None):
        self.item_selector = item_selector
        self.backup_tile: Optional[Tile] = None
        self.play_button = play_button
        self.reset = ImageButton(SCREEN_WIDTH - 134, SCREEN_HEIGHT - 64, 64, 64, pygame.transform.flip(ROTATE_CW_IMAGE,True, False))
        self.board_history = board_history
        self.history_index: int = 0
        self.drag = False
        self.reset.rect.move(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2)

    def draw(self, screen: Surface, game_state: GameState):
        # Render the board and UI during EDIT_TROOPS and PLAY_TROOPS phases
        big_font = constants.big_font
        self.reset.draw(screen)
        dark = self.item_selector.selected_item == "placable"
        self.item_selector.draw(screen)
        self.common_draw(screen, game_state, dark)

    def run(self, pos: Tuple[int], event: pygame.event.Event, game_state: GameState):
        if event.type == pygame.KEYDOWN:
            key = event.key
            self.item_selector.run(None, key)
            if key == pygame.K_r:
                if len(self.board_history) > 0:
                    game_state.board = self.board_history[0]
                    self.board_history = []
                    self.history_index = 0
            elif key == pygame.K_COMMA:
                if len(self.board_history) > 0 and self.history_index > 0:
                    game_state.board = self.board_history[self.history_index - 1]
                    self.history_index -= 1
            elif key == pygame.K_u:
                game_state.board.add_row()
            elif key == pygame.K_i:
                game_state.board.add_col()
            elif key == pygame.K_j:
                game_state.board.del_row()
            elif key == pygame.K_k:
                game_state.board.del_col()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.item_selector.run(pos, None)
            if self.reset.check_click(pos):
                if len(self.board_history) > 0:
                    game_state.board = self.board_history[0]
                    self.board_history = []
                    self.history_index = 0
            elif self.play_button.check_click(pos):
                if self.history_index < len(self.board_history):
                    self.history_index = len(self.board_history)
                    game_state.board = self.board_history[self.history_index - 1]
                self.board_history.append(deepcopy(game_state.board))
                game_state.board.update(game_state.frame_count)
                self.history_index += 1
            # Calculate row and column from click position
            col = (pos[0] - ((SCREEN_WIDTH - len(game_state.board.tiles[0]) * TILE_SIZE) // 2)) // TILE_SIZE
            row = (pos[1] - ((SCREEN_HEIGHT - len(game_state.board.tiles) * TILE_SIZE) // 2)) // TILE_SIZE
            # Ensure click is within bounds
            print("Click Pos: " + str(col) + ", " + str(row))
            if row == len(game_state.board.tiles) and col == len(game_state.board.tiles[0]):
                self.drag = True
            elif 0 <= row < len(game_state.board.tiles) and 0 <= col < len(
                    game_state.board.tiles[0]) and not self.drag:
                tile = game_state.board.tiles[row][col]
                # Add or remove units based on current state
                match self.item_selector.selected_item:
                    case "apple":
                        if tile.unit is None:
                            if tile.is_free() and not tile.is_placeable:
                                tile.unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
                        elif tile.unit.team is Team.ORANGE:
                            tile.unit = None
                        elif tile.unit.team is Team.APPLE:
                            tile.unit = None
                    case "orange":
                        if tile.unit is None:
                            if tile.is_free():
                                tile.unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                        elif tile.unit.team is Team.ORANGE:
                            tile.unit = None
                        elif tile.unit.team is Team.APPLE:
                            tile.unit = None
                    case "grass":
                        tile.type = TileType.GRASS
                    case "water":
                        tile.type = TileType.WATER
                    case "trampoline":
                        tile.type = TileType.TRAMPOLINE
                        tile.is_placeable = False
                    case "wall":
                        tile.type = TileType.WALL
                        tile.is_placeable = False
                    case "remains":
                        tile.type = TileType.DEADWALL
                    case "lava":
                        tile.type = TileType.TRAPDOOR
                        tile.is_placeable = False
                    case "finish line":
                        tile.type = TileType.FINISH_LINE
                    case "teleporter":
                        if tile.type == TileType.TUNNEL:
                            self.backup_tile = tile
                        elif self.backup_tile is not None:
                            self.backup_tile.destination = (row, col)
                            self.backup_tile = None
                        else:
                            tile.type = TileType.TUNNEL
                    case "rotate cw":
                        if tile.unit is not None:
                            tile.unit.rotate_cw()
                        elif tile.type == TileType.TRAMPOLINE:
                            tile.rotate_cw()
                    case "rotate ccw":
                        if tile.unit is not None:
                            tile.unit.rotate_ccw()
                        elif tile.type == TileType.TRAMPOLINE:
                            tile.rotate_ccw()
                    case "placable":
                        if tile.type != TileType.WALL and tile.type != TileType.TRAMPOLINE and tile.type != TileType.WATER and tile.type != TileType.TRAPDOOR:
                            tile.is_placeable = not tile.is_placeable

        elif event.type == pygame.MOUSEBUTTONUP and self.drag:
            self.drag = False
        elif event.type == pygame.MOUSEMOTION and self.drag:
            col = (pos[0] - ((SCREEN_WIDTH - len(game_state.board.tiles[0]) * TILE_SIZE) / 2)) / TILE_SIZE
            row = (pos[1] - ((SCREEN_HEIGHT - len(game_state.board.tiles) * TILE_SIZE) / 2)) / TILE_SIZE
            print("Click Pos: " + str(col) + ", " + str(row))
            if row-0.25 > len(game_state.board.tiles):
                game_state.board.add_row()
            elif row+0.25 < len(game_state.board.tiles):
                game_state.board.del_row()
            if col-0.25 > len(game_state.board.tiles[0]):
                game_state.board.add_col()
            elif col+0.25 < len(game_state.board.tiles[0]):
                game_state.board.del_col()

    def common_draw(self, screen: Surface, game_state: GameState, dark: bool = False):
        big_font = constants.big_font
        game_state.board.render(screen, game_state.game_mode, game_state.frame_count, dark)
        level_name_surface = big_font.render(game_state.level_name, True, (0, 0, 0))
        l_name_rect = level_name_surface.get_rect(
            topleft=(
                (SCREEN_WIDTH - 14 * len(game_state.level_name)) // 2,
                (SCREEN_HEIGHT - len(game_state.board.tiles) * TILE_SIZE) // 2 - 60
            )
        )
        pygame.draw.rect(screen, (255, 255, 255), l_name_rect.inflate(20, 10))
        screen.blit(level_name_surface, l_name_rect)
        self.play_button.draw(screen)

        counter_text = f"Units: {game_state.placed_units}/{game_state.max_units - game_state.board.units_killed_by_team[Team.ORANGE]}"
        counter_surface = big_font.render(counter_text, True, (0, 0, 0))
        counter_rect = counter_surface.get_rect(topleft=(20, 20))
        pygame.draw.rect(screen, (255, 255, 255), counter_rect.inflate(20, 10))
        screen.blit(counter_surface, counter_rect)

        # Display finished units by team
        orange_finished_surface = big_font.render(
            f"{game_state.board.finished_units_by_team[Team.ORANGE]}", True, (0, 0, 0)
        )
        apple_finished_surface = big_font.render(
            f"{game_state.board.finished_units_by_team[Team.APPLE]}", True, (0, 0, 0)
        )

        # Calculate Y-position for team counters
        team_counters_y = (SCREEN_HEIGHT + len(game_state.board.tiles) * TILE_SIZE) // 2 + 20

        # Apple team's finished units
        apple_rect = apple_finished_surface.get_rect(
            topleft=((SCREEN_WIDTH - len(game_state.board.tiles[0]) * TILE_SIZE) // 2 - 10, team_counters_y))
        pygame.draw.rect(screen, (255, 255, 255), apple_rect.inflate(20, 10))
        screen.blit(apple_finished_surface, apple_rect)

        # Orange team's finished units
        orange_rect = orange_finished_surface.get_rect(
            topleft=((SCREEN_WIDTH + len(game_state.board.tiles[0]) * TILE_SIZE) // 2, team_counters_y)
        )
        pygame.draw.rect(screen, (255, 255, 255), orange_rect.inflate(20, 10))
        screen.blit(orange_finished_surface, orange_rect)

def get_edit_screen(play_button):
    god_mode_editor = RadioMeta(
        [
            HorizontalRadioSelector(
                [
                    HorizontalRadioSelector.RadioItem(ROTATE_CCW_IMAGE, "rotate ccw", None),
                    HorizontalRadioSelector.RadioItem(ROTATE_CW_IMAGE, "rotate cw", None)
                ],
                6,
                SCREEN_HEIGHT - 76,
                146
            ),
            HorizontalRadioSelector(
                [
                    HorizontalRadioSelector.RadioItem(GRASS_IMAGE,"placable", pygame.K_p),
                    HorizontalRadioSelector.RadioItem(ORANGE_IMAGE, "orange", pygame.K_1),
                    HorizontalRadioSelector.RadioItem(APPLE_IMAGE, "apple", pygame.K_2),
                    HorizontalRadioSelector.RadioItem(GRASS_IMAGE, "grass", pygame.K_3),
                    HorizontalRadioSelector.RadioItem(WATER_IMAGE, "water", pygame.K_4),
                    HorizontalRadioSelector.RadioItem(TRAMPOLINE_SLASH, "trampoline", pygame.K_5),
                    HorizontalRadioSelector.RadioItem(GRAVESTONE_IMAGE, "wall", pygame.K_6),
                    HorizontalRadioSelector.RadioItem(BROKEN_GRAVESTONE_IMAGE, "remains", pygame.K_7),
                    HorizontalRadioSelector.RadioItem(LAVA_IMAGE, "lava", pygame.K_8),
                    HorizontalRadioSelector.RadioItem(FINISH_LINE_IMAGE, "finish line", pygame.K_9),
                    HorizontalRadioSelector.RadioItem(BROKEN_GRAVESTONE_IMAGE, "teleporter", pygame.K_0),
                ],
                SCREEN_WIDTH - 770,
                6,
                SCREEN_WIDTH - 70
            )
        ]
    )

    return EditScreen(god_mode_editor, play_button, [])