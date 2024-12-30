from typing import Optional

import pygame
from pygame import MOUSEBUTTONDOWN, Surface
from pygame.font import Font

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from dialogue import opening_dialogue
from gamestate import GameState
from level import levels
from tile_images import PLAY_IMAGE, ORANGE_BG
from ui import ImageButton, TextButton
from unit import TileType

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")



def main():
    big_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 6)
    small_font = pygame.font.Font("resources/fonts/CDSBodyV2.ttf", 8 * 4)
    title_font = pygame.font.Font("resources/fonts/CDStitleUnicaseV.ttf", 8 * 8)

    play_button = ImageButton(SCREEN_WIDTH - 64, SCREEN_HEIGHT - 64, 64, 64, PLAY_IMAGE)
    next_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Next Level", big_font)  # Define next button
    start_button = TextButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Start Game", big_font)

    mode = 1

    backup_board: Optional[Board] = None

    frame_count = 0
    running = True

    level_idx = 3

    board = levels[level_idx].board
    level_name = levels[level_idx].name

    max_units = 7
    bonus_troops = 0  # Bonus for clearing the level
    troops_killed = 0
    next_round_troops = -1

    current_dialogue = levels[level_idx].opening_dialogue

    current_game_state = GameState.TITLE_SCREEN


    while running:
        frame_count += 1

        render_checkerboard_background(screen, frame_count)


        if current_game_state == GameState.TITLE_SCREEN:
            render_title_screen(screen, title_font, start_button)
        elif current_game_state == GameState.RESULTS_SCREEN:
            bonus_troops = levels[level_idx].bonus_troops
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
            if next_round_troops > 0 and len(levels) > level_idx+1:
                next_button.draw(screen)

        elif current_game_state == GameState.DIALOGUE:

            board.render(screen, frame_count, current_game_state)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(overlay, (0, 0))

            if current_dialogue is None:
                current_game_state = GameState.EDIT_TROOPS
                board.animations = []
                board.update_strength_defense(frame_count)
            else:
                current_dialogue.render(screen, big_font, frame_count)

        else:
            # Render the board and UI during EDIT_TROOPS and PLAY_TROOPS phases
            board.render(screen, current_game_state, frame_count)


            level_name_surface = big_font.render(level_name, True, (0, 0, 0))
            l_name_rect = level_name_surface.get_rect(topleft=((SCREEN_WIDTH - 14 * len(level_name)) // 2, (SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE) // 2 - 60))
            pygame.draw.rect(screen, (255, 255, 255), l_name_rect.inflate(20, 10))
            screen.blit(level_name_surface, l_name_rect)

            play_button.draw(screen)

            placed_units = board.get_number_of_units_by_team(Team.ORANGE)
            counter_text = f"Units: {placed_units}/{max_units - board.units_killed_by_team[Team.ORANGE]}"
            counter_surface = big_font.render(counter_text, True, (0, 0, 0))
            counter_rect = counter_surface.get_rect(topleft=(20, 20))
            pygame.draw.rect(screen, (255, 255, 255), counter_rect.inflate(20, 10))
            screen.blit(counter_surface, counter_rect)

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
                apple_rect = apple_finished_surface.get_rect(topleft=((SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE) // 2, team_counters_y))
                pygame.draw.rect(screen, (255, 255, 255), apple_rect.inflate(20, 10))
                screen.blit(apple_finished_surface, apple_rect)

                # Orange team's finished units
                orange_rect = orange_finished_surface.get_rect(
                    topleft=((SCREEN_WIDTH + len(board.tiles[0]) * TILE_SIZE) // 2, team_counters_y)
                )
                pygame.draw.rect(screen, (255, 255, 255), orange_rect.inflate(20, 10))
                screen.blit(orange_finished_surface, orange_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
                elif event.key == pygame.K_3:
                    mode = 3
                elif event.key == pygame.K_4:
                    mode = 4
                elif event.key == pygame.K_5:
                    mode = 5
                elif event.key == pygame.K_6:
                    mode = 6
                elif event.key == pygame.K_b:
                    if backup_board is not None:
                        board = backup_board
                        current_game_state = GameState.EDIT_LEVEL
                elif event.key == pygame.K_MINUS:
                    max_units -= 1
                elif event.key == pygame.K_EQUALS:
                    max_units += 1
                elif event.key == pygame.K_TAB:
                    if current_game_state == GameState.DIALOGUE:
                        current_dialogue = current_dialogue.next
                elif event.key == pygame.K_ESCAPE:
                    if current_game_state == GameState.DIALOGUE:
                        current_game_state = GameState.EDIT_TROOPS
                        board.animations = []
                        board.update_strength_defense(frame_count)
                    elif current_game_state == GameState.EDIT_TROOPS:
                        current_game_state = GameState.EDIT_LEVEL
                    elif current_game_state == GameState.EDIT_LEVEL:
                        backup_board = board
                        current_game_state = GameState.EDIT_TROOPS
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("Click Registered")
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

                    if play_button.check_click(pos):
                        frame_count+=10
                        board.update(frame_count)

                    board.animations = []
  
                    board.update_strength_defense(frame_count)

                    # Check if play button was clicked
                    if play_button.check_click(pos):
                        current_game_state = GameState.PLAY_TROOPS

                elif current_game_state == GameState.EDIT_LEVEL:
                    # Calculate row and column from click position
                    print("Edit mode")
                    col = (pos[0] - ((SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE) // 2)) // TILE_SIZE
                    row = (pos[1] - ((SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE) // 2)) // TILE_SIZE

                    # Ensure click is within bounds
                    print("Click Pos: " + str(col) + ", " + str(row))
                    if 0 <= row < len(board.tiles) and 0 <= col < len(board.tiles[0]):
                        tile = board.tiles[row][col]
                        print("in bounds")

                        # Add or remove units based on current state
                        if mode == 1:
                            if tile.unit is None:
                                if tile.is_free() and not tile.is_placeable:
                                    print("Adding Unit")
                                    tile.unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
                            elif tile.unit.team is Team.ORANGE:
                                tile.unit = None
                            elif tile.unit.team is Team.APPLE:
                                tile.unit = None
                        elif mode == 2:
                            if tile.type == TileType.WALL:
                                tile.type = TileType.TRAMPOLINE
                            elif tile.type == TileType.TRAMPOLINE:
                                tile.type = TileType.TRAPDOOR
                            elif tile.type == TileType.TRAPDOOR:
                                tile.type = TileType.FINISH_LINE
                            elif tile.type == TileType.FINISH_LINE:
                                tile.type = TileType.TUNNEL
                            else:
                                tile.type = TileType.WALL
                        elif mode == 3:
                            if tile.unit is not None:
                                tile.unit.rotate_cw()
                        elif mode == 4:
                            if tile.type == TileType.TRAMPOLINE:
                                tile.rotate_cw()
                        elif mode == 5:
                            if tile.type == TileType.GRASS:
                                tile.type = TileType.WATER
                            else:
                                tile.type = TileType.GRASS

                    board.animations = []
                    board.update_strength_defense(frame_count)

                    # Check if play button was clicked


        pygame.time.delay(20)

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


def render_title_screen(screen: Surface, title_font: Font, start_button: TextButton):

    # Draw the title
    title_surface = title_font.render("My Game Title", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    # Draw the start button
    start_button.draw(screen)


if __name__ == "__main__":
    main()


