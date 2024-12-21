from enum import Enum
from time import time
from typing import NamedTuple, List, Optional, Self, Tuple, Set, Dict

import pygame
from pygame import MOUSEBUTTONDOWN

from board import Board, Unit, Direction, Team, UnitType
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from gamestate import GameState
from tile_images import PLAY_IMAGE
from ui import ImageButton


pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")

def main():
    board = Board.from_string(
        [
            "GGWWWGG",
            "GGGGGGG",
            "GGGGGGG",
        ],
        editable_columns={0, 1}
    )

    board.tiles[1][0].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
    board.tiles[0][1].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
    board.tiles[1][1].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
    board.tiles[0][4].unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
    board.tiles[1][4].unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
    board.tiles[2][4].unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)

    play_button = ImageButton(520, 400, 64, 64, PLAY_IMAGE)

    current_game_state = GameState.EDIT_TROOPS
    frame_count = 0
    running = True

    while running:
        frame_count += 1
        screen.fill((255, 255, 255))

        # Render the board
        board.render(screen, current_game_state)

        play_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if current_game_state == GameState.EDIT_TROOPS:
                    col = (pos[0] - (SCREEN_WIDTH - len(board.tiles[0]) * TILE_SIZE)) // TILE_SIZE + 1
                    row = (pos[1] - (SCREEN_HEIGHT - len(board.tiles) * TILE_SIZE)) // TILE_SIZE
                    if row < len(board.tiles) and col < len(board.tiles[0]):
                        tile = board.tiles[row][col]
                        if tile.unit is None:
                            if board.tiles[row][col].is_free() and board.tiles[row][col].is_placeable:
                                board.tiles[row][col].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                        elif tile.unit.team is Team.ORANGE:
                            board.tiles[row][col].unit = None

                    if play_button.check_click(pos):
                        current_game_state = GameState.PLAY_TROOPS


        pygame.time.delay(20)

        if current_game_state == GameState.PLAY_TROOPS:
            if frame_count % 10 == 0:
                board.update()

    pygame.quit()


if __name__ == "__main__":
    main()
