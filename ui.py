from typing import NamedTuple, List, Optional

import pygame
from pygame import Surface
from pygame.font import Font

from board import Board
from constants import BUTTON_ACTIVE_BG, BUTTON_BG, BUTTON_TEXT_COLOR
from gamestate import GameState


class Drawable:
    def draw(self, surface):
        raise NotImplemented()


class TextToggleButton(Drawable):
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.active = False

    def draw(self, surface):
        color = BUTTON_ACTIVE_BG if self.active else BUTTON_BG
        pygame.draw.rect(surface, color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class ImageButton(Drawable):
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if False:
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 50))  # Semi-transparent white overlay
            surface.blit(overlay, self.rect.topleft)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)


class TextButton(Drawable):
    def __init__(self, x: int, y: int, width: int, height: int, label: str, font: Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = label
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        if False:
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 50))  # Semi-transparent white overlay
            surface.blit(overlay, self.rect.topleft)

    def check_click(self, pos):
        return self.rect.collidepoint(pos)


class Screen:
    def __init__(self):
        raise NotImplementedError

    def draw(self, surface: Surface, board: Board, current_game_state: GameState, frame_count: int, *args):
        pass

class HorizontalRadioSelector(Drawable):
    class RadioItem(NamedTuple):
        icon: Surface
        name: str
        key: int

    def __init__(self, items: List[RadioItem], start_x: int, start_y: int, end_x: int):
        self.items = items
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.selected_item: Optional[str] = None

    def draw(self, screen: Surface):
        draw_x = self.start_x
        draw_y = self.start_y

        for item in self.items:
            screen.blit(item.icon, (draw_x, draw_y))
            if self.selected_item == item.name:
                pygame.draw.rect(screen, (255, 100, 0), (draw_x, draw_y, 70, 70), 5)

            draw_x += 70
            if draw_x > self.end_x:
                draw_x = self.start_x
                draw_y += 70

    def run(self, pos, key):
        draw_x = self.start_x
        draw_y = self.start_y

        for item in self.items:
            if key == item.key or (draw_x <= pos.x < draw_x+70 and draw_y <= pos.y < draw_y+70):
                self.selected_item = item.name

            draw_x += 70
            if draw_x > self.end_x:
                draw_x = self.start_x
                draw_y += 70



