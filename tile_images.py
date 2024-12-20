import pygame

from constants import TILE_SIZE


def get_load_image_type(type: str):
    def load_image_type(name: str) -> pygame.Surface:
        raw_img = pygame.image.load(f"resources/{type}/{name}.png")
        return pygame.transform.scale(raw_img, (TILE_SIZE, TILE_SIZE))

    return load_image_type


load_tile_image = get_load_image_type("tiles")
load_sprite_image = get_load_image_type("sprite")


GRASS_IMAGE = load_tile_image("grass")
WATER_IMAGE = load_tile_image("water")

ORANGE_IMAGE = load_sprite_image("orange")
APPLE_IMAGE = load_sprite_image("apple")
