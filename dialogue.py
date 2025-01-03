from enum import Enum
from typing import Self, Tuple, List, Optional, NamedTuple, Dict

import pygame
from pygame import Surface
from pygame.font import Font

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from tile_images import GENERAL_IMAGE, DEFENSE_OVERLAY, OFFENSE_OVERLAY, GENERAL_APPLE_IMAGE


class DialogueImageData(NamedTuple):
    image: Surface
    name: str

class DialogueImage(Enum):
    GENERAL_ORANGE = DialogueImageData(GENERAL_IMAGE, 'GENERAL_ORANGE')
    GENERAL_APPLE = DialogueImageData(GENERAL_APPLE_IMAGE, 'GENERAL_APPLE')

    @classmethod
    def from_str(cls, sname: str):
        for image_type in DialogueImage:
            if image_type.value.name == sname:
                return image_type

class DialogueOverlayImage(Enum):
    OFFENSE_OVERLAY = DialogueImageData(OFFENSE_OVERLAY, 'OFFENSE_OVERLAY')
    DEFENSE_OVERLAY = DialogueImageData(DEFENSE_OVERLAY, 'DEFENSE_OVERLAY')

    @classmethod
    def from_str(cls, sname: str):
        for image_type in DialogueOverlayImage:
            if image_type.value.name == sname:
                return image_type

class Dialogue:
    def __init__(self, text: str, next: Self = None, speaker_image: DialogueImage = None, presentation_image: DialogueImage= None):
        self.text = text
        self.speaker_image = speaker_image
        self.next = next
        self.presentation_image = presentation_image
        self.first_appear_frame = None

    @staticmethod
    def from_list(items: List[Tuple[str, Optional[DialogueImage], Optional[DialogueOverlayImage]]]):
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

    def is_complete(self, frame_count: int):
        if self.first_appear_frame is None:
            return False
        return (frame_count - self.first_appear_frame) >= len(self.text)

    def render(self, screen: Surface, font: Font, current_frame: int, box_color: Tuple[int, int, int] = (255, 255, 255),
               text_color: Tuple[int, int, int] = (0, 0, 0), border_color: Tuple[int, int, int] = (0, 0, 0),
               highlight_color: Tuple[int, int, int] = (255, 165, 0)):  # Orange
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

        # Prepare text to render
        visible_text = self.text[:max_length]

        # Split words, handling wrapping and highlighting
        max_text_width = inner_box_rect.width - 40  # Account for margins
        words = visible_text.split()
        lines = []
        current_line = []
        current_line_width = 0

        for word in words:
            test_surface = font.render(word, True, text_color)
            test_width = test_surface.get_width()

            if current_line_width + test_width > max_text_width:
                # Wrap to a new line
                lines.append(current_line)
                current_line = []
                current_line_width = 0

            current_line.append(word)
            current_line_width += test_width + font.size(" ")[0]  # Add space width

        # Add the last line
        if current_line:
            lines.append(current_line)

        # Render each line of text with highlighting
        text_y = inner_box_rect.top + 20
        line_spacing = font.get_linesize()

        for line in lines:
            text_x = inner_box_rect.left + 20
            for word in line:
                if word.startswith('^'):
                    highlight_surface = font.render(word[1:], True, highlight_color)
                    screen.blit(highlight_surface, (text_x, text_y))
                    text_x += highlight_surface.get_width() + font.size(" ")[0]  # Add space width
                else:
                    # Render regular word
                    text_surface = font.render(word, True, text_color)
                    screen.blit(text_surface, (text_x, text_y))
                    text_x += text_surface.get_width() + font.size(" ")[0]  # Add space width

            text_y += line_spacing

        # Render speaker image, if available
        if self.speaker_image is not None:
            sp_width, sp_height = self.speaker_image.value.image.get_size()
            speaker_x = inner_box_rect.left + 10
            speaker_y = inner_box_rect.top - sp_height - 8  # 8 = line of width
            screen.blit(self.speaker_image.value.image, (speaker_x, speaker_y))

        # Render presentation image, if available
        if self.presentation_image is not None:
            pr_width, pr_height = self.presentation_image.value.image.get_size()
            presentation_x = (SCREEN_WIDTH - pr_width) // 2
            presentation_y = (SCREEN_HEIGHT // 2 - 3 * pr_height // 4)
            screen.blit(self.presentation_image.value.image, (presentation_x, presentation_y))

    def serialize(self) -> List[Dict[str, Optional[str]]]:
        dialogue_dict = []
        i = self
        while i is not None:
            dialogue_dict.append({"Text": i.text,"Speaker Image": i.speaker_image.value.name if i.speaker_image is not None else None, "Overlay Image": i.presentation_image.value.name if i.presentation_image is not None else None})
            i = i.next
        return dialogue_dict

    @classmethod
    def from_serialized(cls, dialogue_dict: List[Dict[str, Optional[str]]]) -> Self:
        dialogue_list = []
        for dict in dialogue_dict:
            dialogue_list.append((dict["Text"], DialogueImage.from_str(dict["Speaker Image"]) , DialogueOverlayImage.from_str(dict["Overlay Image"])))
        return Dialogue.from_list(dialogue_list)

opening_dialogue = Dialogue.from_list(
    [

        ("Alright, corporal! Here's the battlefield laid out for you...", DialogueImage.GENERAL_ORANGE, None),
        ("You can see that those dastardly apples are already there.", DialogueImage.GENERAL_ORANGE, None),
        ("Your objective? To send as many oranges across the battlefield as possible!", DialogueImage.GENERAL_ORANGE, None),
        ("But beware! Those apples are going to try and get across too. And when our troops collide, a fight is inevitable.", DialogueImage.GENERAL_ORANGE, None),
        ("Whoever gets more troops to the other side, wins!", DialogueImage.GENERAL_ORANGE, None),
        ("And... I hate to tell you this, but we are outnumbered. We merely have 2 troops at our disposal, and they seem to have 3!", DialogueImage.GENERAL_ORANGE, None),
        ("Fear not! If we position our troops strategically, we shall emerge the victors!", DialogueImage.GENERAL_ORANGE, None),
        ("Troops positioned in ^vertical ^lines will form an incredible flank! This will increase their defense astronomically!", DialogueImage.GENERAL_ORANGE, DialogueOverlayImage.DEFENSE_OVERLAY),
        ("The longer the flank, the greater the defense!", DialogueImage.GENERAL_ORANGE, None),
        ("And troops positioned in ^horizontal ^lines will line up to upgrade their fighting power, transforming into yet more advanced soldiers!", DialogueImage.GENERAL_ORANGE, DialogueOverlayImage.OFFENSE_OVERLAY),
        ("If our enemies form a flank, a long line of soldiers might be just the thing to break it to smithereens!", DialogueImage.GENERAL_ORANGE, DialogueOverlayImage.OFFENSE_OVERLAY),
        ("I think a ^vertical flank ought to dispatch these neer-do-wells right quick!", DialogueImage.GENERAL_ORANGE, None),
        ("Alright, simply click to place your troops, and remember, think strategically!", DialogueImage.GENERAL_ORANGE, None),
        ("Once you've thought everything through, press the play button to lead the charge!", DialogueImage.GENERAL_ORANGE, None),
    ]
)
