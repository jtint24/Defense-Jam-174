import pygame
from pygame import MOUSEBUTTONDOWN

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from dialogue import opening_dialogue
from gamestate import GameState
from level import levels
from tile_images import PLAY_IMAGE
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
    mode = 1

    current_game_state = GameState.EDIT_TROOPS
    frame_count = 0
    running = True

    level_idx = 0

    board = levels[level_idx].board

    max_units = 2
    bonus_troops = 0  # Bonus for clearing the level
    troops_killed = 0
    next_round_troops = -1

    current_dialogue = opening_dialogue

    current_game_state = GameState.DIALOGUE

    while running:
        frame_count += 1
        screen.fill((255, 255, 255))

        if current_game_state == GameState.RESULTS_SCREEN:
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

            current_dialogue.render(screen, big_font, frame_count)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    print("yippie")
                elif event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
                elif event.key == pygame.K_3:
                    mode = 3
                elif event.key == pygame.K_4:
                    mode = 4
                elif event.key == pygame.K_TAB:
                    if current_game_state == GameState.DIALOGUE:
                        current_dialogue = current_dialogue.next
                elif event.key == pygame.K_ESCAPE:
                    if current_game_state == GameState.DIALOGUE:
                        current_game_state = GameState.EDIT_TROOPS
                    elif current_game_state == GameState.EDIT_TROOPS:
                        current_game_state = GameState.EDIT_LEVEL
                    elif current_game_state == GameState.EDIT_LEVEL:
                        current_game_state = GameState.EDIT_TROOPS
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("Click Registered")
                if current_game_state == GameState.DIALOGUE:
                    if current_dialogue.is_complete(frame_count):
                        current_dialogue = current_dialogue.next
                    if current_dialogue is None:
                        current_game_state = GameState.EDIT_TROOPS
                elif current_game_state == GameState.RESULTS_SCREEN:

                    if next_round_troops > 0 and next_button.check_click(pos):
                        level_idx += 1
                        board = levels[level_idx].board
                        max_units = next_round_troops
                        current_dialogue = levels[level_idx].opening_dialogue
                        if current_dialogue is None:
                            current_game_state = GameState.EDIT_TROOPS
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
                            if placed_units < max_units and tile.is_free() and tile.is_placeable:
                                tile.unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                        elif tile.unit.team is Team.ORANGE:
                            tile.unit = None

                    board.update_strenth_defense(frame_count)

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
                                if  tile.is_free() and not tile.is_placeable:
                                    print("Adding Unit")
                                    tile.unit = Unit(UnitType.SOLDIER, Direction.UP, Team.APPLE)
                            elif tile.unit.team is Team.ORANGE:
                                tile.unit = None
                            elif tile.unit.team is Team.APPLE:
                                tile.unit = None
                        elif mode == 2:
                            if tile.type == TileType.GRASS:
                                tile.type = TileType.WATER
                            elif tile.type == TileType.WATER:
                                tile.type = TileType.GRASS
                        elif mode == 3:
                            if tile.unit is not None:
                                tile.unit.rotate_cw()
                        elif mode == 4:
                            if tile.type == TileType.TRAMPOLINE:
                                tile.rotate_cw()



                    board.update_strenth_defense(frame_count)

                    # Check if play button was clicked


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
