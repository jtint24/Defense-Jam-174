from pygame import Surface
from pygame.font import Font

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import TextButton


def render_title_screen(screen: Surface, title_font: Font, start_button: TextButton):
    # Draw the title
    title_surface = title_font.render("Warchard", True, (0, 0, 0))
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    # Draw the start button
    start_button.draw(screen)
