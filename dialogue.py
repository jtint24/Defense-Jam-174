from typing import Self, Tuple, List, Optional

import pygame
from pygame import Surface
from pygame.font import Font

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from tile_images import GENERAL_IMAGE


class Dialogue:
    def __init__(self, text: str, next: Self = None, speaker_image: Surface = None, presentation_image: Surface = None):
        self.text = text
        self.speaker_image = speaker_image
        self.next = next
        self.presentation_image = presentation_image
        self.first_appear_frame = None

    @staticmethod
    def from_list(items: List[Tuple[str, Optional[Surface], Optional[Surface]]]):
        prev = None
        first = None
        for text, sp_image, pr_image in items:
            dialogue = Dialogue(text, None, sp_image, pr_image)

            if prev is not None:
                prev.next = dialogue

            prev = dialogue
            if first is None:
                first = dialogue

        return first

    def render(self, screen: Surface, font: Font, current_frame: int, box_color: Tuple[int, int, int] = (255, 255, 255),
               text_color: Tuple[int, int, int] = (0, 0, 0), border_color: Tuple[int, int, int] = (0, 0, 0)):
        # Box dimensions
        box_height = SCREEN_HEIGHT // 4
        box_rect = pygame.Rect(0, SCREEN_HEIGHT - box_height, SCREEN_WIDTH, box_height)

        # Draw the border
        pygame.draw.rect(screen, border_color, box_rect, width=8)

        # Draw the dialogue box inside the border
        inner_box_rect = box_rect.inflate(-16, -16)
        pygame.draw.rect(screen, box_color, inner_box_rect)

        # Figure out how many chars can be shown
        if self.first_appear_frame is None:
            self.first_appear_frame = current_frame
        max_length = current_frame - self.first_appear_frame

        # Draw the text with wrapping
        max_text_width = inner_box_rect.width - 40  # Account for margins
        words = self.text[:max_length].split()
        lines = []
        current_line = []

        for word in words:
            # Check if adding the next word exceeds the maximum width
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, text_color)
            if test_surface.get_width() > max_text_width:
                # If it exceeds, store the current line and start a new one
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)

        # Add the final line
        if current_line:
            lines.append(' '.join(current_line))

        # Render each line of text
        text_y = inner_box_rect.top + 20
        line_spacing = font.get_linesize()

        for line in lines:
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(midleft=(inner_box_rect.left + 20, text_y))
            screen.blit(text_surface, text_rect)
            text_y += line_spacing

        if self.speaker_image is not None:
            sp_width, sp_height = self.speaker_image.get_size()
            speaker_x = inner_box_rect.left + 10
            speaker_y = inner_box_rect.top - sp_height - 8  # 8 = line of width
            screen.blit(self.speaker_image, (speaker_x, speaker_y))

        if self.presentation_image is not None:
            pr_width, pr_height = self.presentation_image.get_size()
            presentation_x = (SCREEN_WIDTH - pr_width) // 2
            presentation_y = (SCREEN_HEIGHT // 2 - pr_height // 2)
            screen.blit(self.presentation_image, (presentation_x, presentation_y))


opening_dialogue = Dialogue.from_list(
    [
        ("Alright, corporal! Here's the battlefield laid out for you...", GENERAL_IMAGE, None),
        ("You can see that those dastardly apples are already there.", GENERAL_IMAGE, None),
        ("Your objective? To send as many oranges across the battlefield as possible!", GENERAL_IMAGE, None),
        ("But beware! Those apples are going to try and get across too. And when our troops collide, a fight is inevitable.", GENERAL_IMAGE, None),
        ("Whoever gets more troops to the other side, wins!", GENERAL_IMAGE, None),
        ("And... I hate to tell you this, but we are outnumbered. We merely have 2 troops at our disposal, and they seem to have 3!", GENERAL_IMAGE, None),
        ("Fear not! If we position our troops strategically, we shall emerge the victors", GENERAL_IMAGE, None),
        ("Troops positioned in *vertical* *lines* will form an incredible flank! This will increase their defense astronomically!", GENERAL_IMAGE, None),
        ("The longer the flank, the greater the defense!", GENERAL_IMAGE, None),
        ("And troops positioned in *horizontal* *lines* will line up to upgrade their fighting power!", GENERAL_IMAGE, None),
        ("If our enemies form a flank, a long line of soldiers might be just the thing to break it to smithereens!", GENERAL_IMAGE, None),
        ("I think a *vertical* flank ought to dispatch these neer-do-wells right quick!", GENERAL_IMAGE, None),
    ]
)
