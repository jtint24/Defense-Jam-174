import pygame

from constants import BUTTON_ACTIVE_BG, BUTTON_BG, BUTTON_TEXT_COLOR


class Button:
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
