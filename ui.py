from typing import NamedTuple, List, Optional, Tuple

import pygame
from pygame import Surface
from pygame.font import Font

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


class GameScreen:
    def __init__(self):
        raise NotImplementedError

    def draw(self, screen: Surface, game_state: GameState, *args):
        pass

    def run(self, pos: Tuple[int], event: pygame.event.Event, game_state: GameState):
        pass


class RadioButtons(Drawable):
    def __init__(self):
        self.selected_item: Optional[str] = None
        self.active = False
        raise NotImplementedError

    def run(self, pos, key):
        raise NotImplementedError


class RadioMeta(RadioButtons):
    def __init__(self, radio_buttons: List[RadioButtons]):
        self.active = False
        self.selected_item: Optional[str] = None
        self.radio_buttons = radio_buttons

    def draw(self, surface):
        for radio_button_set in self.radio_buttons:
            radio_button_set.draw(surface)

    def run(self, pos, key):
        self.active = False
        for radio_button_set in self.radio_buttons:
            radio_button_set.run(pos, key)
            if radio_button_set.active:
                self.active = True

        if len([radio_button_set for radio_button_set in self.radio_buttons if radio_button_set.selected_item is not None]) > 1:
            for radio_button_set in self.radio_buttons:
                if not radio_button_set.active:
                    radio_button_set.selected_item = None

        selected_items = [radio_button_set.selected_item for radio_button_set in self.radio_buttons if radio_button_set.selected_item is not None]
        if len(selected_items) > 0:
            self.selected_item = selected_items[0]
        else:
            self.selected_item = None


class HorizontalRadioSelector(RadioButtons):
    class RadioItem(NamedTuple):
        icon: Surface
        name: str
        key: Optional[int]

    def __init__(self, items: List[RadioItem], start_x: int, start_y: int, end_x: int):
        self.items = items
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.selected_item: Optional[str] = None
        self.active = False

    def draw(self, screen: Surface):
        draw_x = self.start_x
        draw_y = self.start_y

        for item in self.items:
            screen.blit(item.icon, (draw_x, draw_y))
            if self.selected_item == item.name:
                pygame.draw.rect(screen, (255, 100, 0), (draw_x, draw_y, 64, 64), 5)

            draw_x += 70
            if draw_x > self.end_x:
                draw_x = self.start_x
                draw_y += 70

    def run(self, pos, key):
        draw_x = self.start_x
        draw_y = self.start_y
        self.active = False

        for item in self.items:
            if (key == item.key and item.key is not None) or (pos is not None and (draw_x <= pos[0] < draw_x+70 and draw_y <= pos[1] < draw_y+70)):
                self.selected_item = item.name
                self.active = True

            draw_x += 70
            if draw_x > self.end_x:
                draw_x = self.start_x
                draw_y += 70
