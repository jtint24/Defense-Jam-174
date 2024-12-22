import math

import pygame

from unit import Unit, Direction
from constants import TILE_SIZE

class Animation:
    def __init__(self):
        raise NotImplemented

    def draw(self, screen: pygame.Surface, current_frame: int):
        raise NotImplemented


class UnitAnimation:
    def __init__(self, start_frame: int, unit: Unit, x: int, y: int, direction:Direction =None):
        self.start_frame = start_frame
        self.x = x
        self.y = y
        self.unit = unit
        if direction is not None:
            self.direction = direction
        else:
            self.direction = unit.direction


class StaticUnitAnimation(UnitAnimation):
    def draw(self, screen: pygame.Surface, current_frame: int):
        screen.blit(self.unit.get_image(), (self.x, self.y))


class UnitMovementAnimation(UnitAnimation):
    def draw(self, screen: pygame.Surface, current_frame: int):
        d_x, d_y = {
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0),
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
        }[self.direction]

        animation_frame = current_frame - self.start_frame

        end_x, end_y = self.x + d_x * TILE_SIZE, self.y + d_y * TILE_SIZE

        # Animation curve starts fast then accelerates down so that the unit sort of gravitates towards the center of the space
        def animation_curve(t: float):
            return (10/9) * (1 - pow(10, -t))

        # For the last 3 frames, it's just chilling in the next square over, not moving at all.
        if animation_frame <= 11:
            render_x = (end_x - self.x) * animation_curve(animation_frame/11) + self.x
            render_y = (end_y - self.y) * animation_curve(animation_frame/11) + self.y
        else:
            render_x = end_x
            render_y = end_y

        screen.blit(self.unit.get_image(), (render_x, render_y))


class UnitDeathAnimation(UnitAnimation):
    def draw(self, screen: pygame.Surface, current_frame: int):
        animation_frame = current_frame - self.start_frame

        total_frames = 15

        # Progress of the animation (0.0 to 1.0)
        t = min(animation_frame / total_frames, 1.0)

        alpha = max(0, int(255 * (1 - t)))

        angle = 2 * math.pi * t * 2
        radius = TILE_SIZE * t
        offset_x = math.cos(angle) * radius
        offset_y = math.sin(angle) * radius

        fall_offset = TILE_SIZE * t

        # Final render position
        render_x = self.x + offset_x
        render_y = self.y + offset_y + fall_offset

        unit_image = self.unit.get_image().copy()
        unit_image.set_alpha(alpha)

        # Draw the unit with applied transformations
        screen.blit(unit_image, (render_x, render_y))


class UnitWinAnimation(UnitAnimation):
    def draw(self, screen: pygame.Surface, current_frame: int):

        animation_frame = current_frame - self.start_frame

        end_x, end_y = self.x, self.y - TILE_SIZE

        total_frames = 15

        def animation_curve(t: float):
            return 1 - ((10/9) * (1 - pow(10, t-1)))

        t = min(animation_frame / total_frames, 1.0)

        alpha = max(0, int(255 * (1 - t)))

        # For the last 3 frames, it's just chilling in the next square over, not moving at all.
        render_y = (end_y - self.y) * animation_curve(animation_frame/15) + self.y

        image = self.unit.get_image().copy()
        image.set_alpha(alpha)

        screen.blit(image, (self.x, render_y))
