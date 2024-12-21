import pygame

from unit import Unit, Direction
from constants import TILE_SIZE

class Animation:
    def __init__(self):
        raise NotImplemented

    def draw(self, screen: pygame.Surface, current_frame: int):
        raise NotImplemented


class UnitAnimation:
    def __init__(self, start_frame: int, unit: Unit, x: int, y: int):
        self.start_frame = start_frame
        self.x = x
        self.y = y
        self.unit = unit


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
        }[self.unit.direction]

        animation_frame = current_frame - self.start_frame

        end_x, end_y = self.x + d_x * TILE_SIZE, self.y + d_y * TILE_SIZE

        # Animation curve starts fast then accelerates down so that the unit sort of gravitates towards the center of the space
        def animation_curve(t: float):
            return (10/9) * (1 - pow(10, -t))

        if animation_frame <= 11:
            render_x = (end_x - self.x) * animation_curve(animation_frame/11) + self.x
            render_y = (end_y - self.y) * animation_curve(animation_frame/11) + self.y
        else:
            render_x = end_x
            render_y = end_y

        screen.blit(self.unit.get_image(), (render_x, render_y))
