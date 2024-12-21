import pygame
from pygame.font import Font

from constants import BUTTON_ACTIVE_BG, BUTTON_BG, BUTTON_TEXT_COLOR



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
