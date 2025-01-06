from typing import Optional

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

TILE_SIZE = 64

BUTTON_BG = (200, 200, 200)
BUTTON_ACTIVE_BG = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)

ENABLE_EDITING = True
GENERATE_FILE = False
LOAD_FILE = not GENERATE_FILE

big_font: Optional[pygame.font.Font] = None
small_font: Optional[pygame.font.Font] = None
title_font: Optional[pygame.font.Font] = None