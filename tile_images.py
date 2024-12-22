import pygame

from constants import TILE_SIZE


def get_load_image_type(type: str):
    def load_image_type(name: str) -> pygame.Surface:
        raw_img = pygame.image.load(f"resources/{type}/{name}.png")
        return pygame.transform.scale(raw_img, (TILE_SIZE, TILE_SIZE))

    return load_image_type


load_tile_image = get_load_image_type("tiles")
load_button_image = get_load_image_type("button")


def load_sprite_image(name: str) -> pygame.Surface:
    raw_img = pygame.image.load(f"resources/sprite/{name}.png")
    length, width = raw_img.get_size()
    return pygame.transform.scale(raw_img, (length*4, width*4))

def load_overlay_image(name: str) -> pygame.Surface:
    raw_img = pygame.image.load(f"resources/overlays/{name}.png")
    length, width = raw_img.get_size()
    return pygame.transform.scale(raw_img, (length*6, width*6))


GRASS_IMAGE = load_tile_image("grass")
WATER_IMAGE = load_tile_image("water")
TRAMPOLINE_BACKSLASH = load_tile_image("trampoline_backslash")
TRAMPOLINE_SLASH = load_tile_image("trampoline_slash")
FINISH_LINE_IMAGE = load_tile_image("finish_line")
GRAVESTONE_IMAGE = load_tile_image("gravestone")
BROKEN_GRAVESTONE_IMAGE = load_tile_image("broken_gravestone")
LAVA_IMAGE = load_tile_image("lava")

ORANGE_IMAGE = load_sprite_image("orange")
ORANGE_TROOP_IMAGE = load_sprite_image("orange_troop")
ORANGE_TANK_IMAGE = load_sprite_image("orange_tank")
APPLE_IMAGE = load_sprite_image("apple")

GENERAL_IMAGE = load_sprite_image("general")

PLAY_IMAGE = load_button_image("play_button")

ORANGE_BG = load_sprite_image("orange_bg")

DEFENSE_OVERLAY = load_overlay_image("defense")
OFFENSE_OVERLAY = load_overlay_image("offense")
