from enum import Enum
from time import time
from typing import NamedTuple, List, Optional, Self, Tuple, Set, Dict

import pygame
from pygame import MOUSEBUTTONDOWN

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from tile_images import GRASS_IMAGE, WATER_IMAGE, ORANGE_IMAGE, APPLE_IMAGE, ORANGE_TROOP_IMAGE, ORANGE_TANK_IMAGE
from ui import Button


class GameState(Enum):
    TITLE_SCREEN = 1
    EDIT_TROOPS = 2
    PLAY_TROOPS = 3
    RESULTS_SCREEN = 4


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class UnitType(Enum):
    SOLDIER = 1
    HORSE = 2
    CANNON = 3
    # TANK = 4


class Team(Enum):
    ORANGE = [ORANGE_IMAGE, ORANGE_TROOP_IMAGE, ORANGE_TANK_IMAGE]
    APPLE = [APPLE_IMAGE]


class Unit:
    def __init__(self, type: UnitType, direction: Direction, team: Team):
        self.type = type
        self.direction = direction
        self.team = team
        self.defense = 1

    def get_image(self):
        return self.team.value[self.type.value - 1]


class TileTypeData(NamedTuple):
    is_passable: bool
    image: pygame.Surface
    char_code: str


class TileType(Enum):
    GRASS = TileTypeData(True, GRASS_IMAGE, "G")
    WATER = TileTypeData(False, WATER_IMAGE, "W")

    @classmethod
    def from_str(cls, name: str):
        for tile_type in TileType:
            if tile_type.value.char_code == name:
                return tile_type


class Tile:
    def __init__(self, type: TileType, unit: Optional[Unit], is_placeable: bool = True):
        self.type = type
        self.unit = unit
        self.is_placeable = is_placeable

    def is_free(self) -> bool:
        "Returns whether the tile is clear to walk on, based on tile type and other units on it"
        return self.type.value.is_passable and self.unit is None


class Board:
    def __init__(self, tiles: List[List[Tile]]):
        self.tiles = tiles

    @staticmethod
    def to_dimensions(width: int, height: int):
        return Board([[Tile()]])

    @staticmethod
    def row_from_string(row_str: str) -> List[Tile]:
        return [
            Tile(TileType.from_str(code), None)
            for code in row_str
        ]

    @classmethod
    def from_string(cls, board_strs: List[str]) -> Self:
        return Board([cls.row_from_string(row_str) for row_str in board_strs])

    def render(self, game_state: GameState):
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                # Render the tile image
                screen.blit(tile.type.value.image, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

                # Render the unit if present
                if tile.unit is not None:
                    screen.blit(tile.unit.get_image(), (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

                # Darken tile if it is not passable or not placeable
                if game_state == GameState.EDIT_TROOPS and (not tile.type.value.is_passable or not tile.is_placeable):
                    dark_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    dark_surface.fill((0, 0, 0, 100))  # Semi-transparent black overlay
                    screen.blit(dark_surface, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

    def update(self):
        # Start by populating new_tiles with the base tiles (not units) from the current board
        new_tiles = [
            [
                Tile(tile.type, None)
                for tile in row
            ]
            for row in self.tiles
        ]

        # Then, place units in their new positions, detecting collisions where they exist

        chains, locked_units = self.identify_chains()

        for chain in chains:
            for row_idx, col_idx in chain:
                self.move_unit(new_tiles, row_idx, col_idx)
        for row_idx, col_idx in locked_units:
            new_tiles[row_idx][col_idx].unit = self.tiles[row_idx][col_idx].unit

        self.tiles = new_tiles

        # Now, we update each troop's strength

        for row_idx, row in enumerate(self.tiles):
            unit_line = []
            for col_idx, tile in enumerate(row):

                if tile.unit is not None and (len(unit_line) == 0 or tile.unit.team == unit_line[0].team):
                    unit_line.append(tile.unit)
                else:
                    for unit in unit_line:
                        unit.type = UnitType(min(3, len(unit_line)))
                    unit_line = []
            for unit in unit_line:
                unit.type = UnitType(min(3, len(unit_line)))

        # And we update each troop's defense

        for col_idx in range(len(self.tiles[0])):
            unit_line = []
            for row_idx in range(len(self.tiles)):
                tile = self.tiles[row_idx][col_idx]

                if tile.unit is not None and (len(unit_line) == 0 or tile.unit.team == unit_line[0].team):
                    unit_line.append(tile.unit)
                else:
                    for unit in unit_line:
                        unit.defense = min(5, len(unit_line))
                    unit_line = []
            for unit in unit_line:
                unit.defense = min(5, len(unit_line))

    def resolve_conflict(self, conflict: "Conflict") -> Set[Tuple[int, int]]:
        team_damage = {team: 0 for team in Team}

        sorted_belligerents = sorted(
            conflict.belligerent_coordinates,
            key=lambda coordinate: self.tiles[coordinate[0]][coordinate[1]].unit.defense,
            reverse=True
        )

        for b_row_idx, b_col_idx in sorted_belligerents:
            unit = self.tiles[b_row_idx][b_col_idx].unit
            for team in Team:
                if team != unit.team:
                    team_damage[team] += unit.type.value

        # print(team_damage)

        survivors = set()
        weakest_unit_coordinates = []
        weakest_unit_damage = -1

        for b_row_idx, b_col_idx in sorted_belligerents:

            unit = self.tiles[b_row_idx][b_col_idx].unit

            # print("remaining damage", team_damage[unit.team])

            # print("unit team", unit.team, "unit defense", unit.defense, "unit class", unit.type.value)

            exact_damage = team_damage[unit.team] / unit.defense
            # print("exact damage", exact_damage)
            damage = team_damage[unit.team] // unit.defense

            team_damage[unit.team] -= unit.defense
            team_damage[unit.team] = max(team_damage[unit.team], 0)

            if exact_damage > weakest_unit_damage:
                weakest_unit_coordinates = [(b_row_idx, b_col_idx)]
                weakest_unit_damage = exact_damage
            elif exact_damage == weakest_unit_damage:
                weakest_unit_coordinates.append((b_row_idx, b_col_idx))

            if damage == 0:
                survivors.add((b_row_idx, b_col_idx))

        if len(survivors) == len(sorted_belligerents):
            survivors.difference_update(weakest_unit_coordinates)

        return survivors

    def move_unit(self, new_tiles: List[List[Tile]], row_idx: int, col_idx: int):
        _, f_row_idx, f_col_idx = self.get_faced_tile(row_idx, col_idx)
        new_tiles[f_row_idx][f_col_idx].unit = self.tiles[row_idx][col_idx].unit

    class Conflict(NamedTuple):
        belligerent_coordinates: Set[Tuple[int, int]]

    def identify_chains(self) -> Tuple[List[List[Tuple[int, int]]], Set[Tuple[int, int]]]:
        """
        Returns a tuple with two elements.
        The first is a list of chains. Each chain has points in order of how they needed to move.
        The second is a list of units that cannot move.
        The third is a list of units that are heading for conflict
        Every unit is in a chain or it cannot move.
        """
        chains_starting_points = {}
        identified_unit_points = set()
        locked_unit_points = set()

        stuck_unit_points = set()

        # Start by identifying units that are about to head into conflict

        squares_claimed_by_team: Dict[Team, Dict[Tuple[int, int], List[Tuple[int, int]]]] = {
            Team.ORANGE: {},
            Team.APPLE: {}
        }  # Format is team -> claimed_square -> claimed_by_squares

        conflicts = {}
        same_team_conflicts = {}

        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                if tile.unit is not None:
                    faced_tile, f_row_idx, f_col_idx = self.get_faced_tile(row_idx, col_idx)

                    if faced_tile is not None:
                        for team in squares_claimed_by_team:
                            if (f_row_idx, f_col_idx) in squares_claimed_by_team[team]:
                                other_claimants = squares_claimed_by_team[team][(f_row_idx, f_col_idx)]
                                if team != tile.unit.team:
                                    if (f_row_idx, f_col_idx) not in conflicts:
                                        conflicts[(f_row_idx, f_col_idx)] = self.Conflict(set())
                                    conflicts[(f_row_idx, f_col_idx)].belligerent_coordinates.add((row_idx, col_idx))
                                    conflicts[(f_row_idx, f_col_idx)].belligerent_coordinates.update(other_claimants)
                                else:
                                    if (f_row_idx, f_col_idx) not in same_team_conflicts:
                                        same_team_conflicts[(f_row_idx, f_col_idx)] = self.Conflict(set())
                                    same_team_conflicts[(f_row_idx, f_col_idx)].belligerent_coordinates.add(
                                        (row_idx, col_idx))
                                    same_team_conflicts[(f_row_idx, f_col_idx)].belligerent_coordinates.update(
                                        other_claimants)
                        if (f_row_idx, f_col_idx) not in squares_claimed_by_team[tile.unit.team]:
                            squares_claimed_by_team[tile.unit.team][(f_row_idx, f_col_idx)] = []

                        squares_claimed_by_team[tile.unit.team][(f_row_idx, f_col_idx)].append((row_idx, col_idx))

        # For the same-team conflicts, we need to play traffic cop and decide which one goes first.
        # Rule (arbitrary) is that the one with the highest row_idx goes first, then one with highest col_idx
        for conflict_point in same_team_conflicts:
            conflict = same_team_conflicts[conflict_point]
            print("belligerent points", conflict.belligerent_coordinates)

            ok_to_move = max(conflict.belligerent_coordinates)
            stuck_unit_points.update(
                [b_point for b_point in conflict.belligerent_coordinates if b_point != ok_to_move]
            )
            print("stuck points", stuck_unit_points)

        # Now we still need to find squares where two enemy units are moving past one another but not directly onto the same square

        for team in squares_claimed_by_team:
            for claimed_square in squares_claimed_by_team[team]:
                claimants = squares_claimed_by_team[team][claimed_square]
                for claimant in claimants:
                    passing_conflict = self.get_passing_conflict(claimant, claimed_square, squares_claimed_by_team)
                    if passing_conflict is not None:
                        # Check if the passing conflict needs to be combined with an existing one
                        combined_with_conflict = False
                        for belligerent_point in passing_conflict.belligerent_coordinates:
                            if belligerent_point in conflicts:
                                conflicts[belligerent_point].belligerent_coordinates.update(
                                    passing_conflict.belligerent_coordinates)
                                combined_with_conflict = True
                                break
                        if not combined_with_conflict:
                            conflicts[claimed_square] = passing_conflict

        # Resolve all conflicts

        for _, conflict in conflicts.items():
            survivor_coordinates = self.resolve_conflict(conflict)
            for b_row_idx, b_col_idx in conflict.belligerent_coordinates:
                if (b_row_idx, b_col_idx) not in survivor_coordinates:
                    self.tiles[b_row_idx][b_col_idx].unit = None

        # Iterate over all units on the board, finding each ones' chain.

        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                if (row_idx, col_idx) in identified_unit_points:
                    continue
                if tile.unit is not None:
                    chain = self.extract_chain(row_idx, col_idx, stuck_unit_points)
                    if chain is not None:
                        identified_unit_points.update(chain)

                        # Remove any smaller subchains that were identified earlier
                        chains_to_remove = set()
                        for starting_point in chains_starting_points:
                            if starting_point in chain:
                                chains_to_remove.add(starting_point)

                        for chain_to_remove in chains_to_remove:
                            chains_starting_points.pop(chain_to_remove)

                        chains_starting_points[(row_idx, col_idx)] = chain
                    else:
                        locked_unit_points.add((row_idx, col_idx))

        return list(chains_starting_points.values()), locked_unit_points

    def get_passing_conflict(self, opponent: Tuple[int, int], opp_claimed_square: Tuple[int, int],
                             squares_claimed_by_team: Dict[str, Dict[Tuple[int, int], List[Tuple[int, int]]]]) -> \
    Optional[Conflict]:
        for team in squares_claimed_by_team:
            for claimed_square in squares_claimed_by_team[team]:
                if claimed_square == opponent and opp_claimed_square in squares_claimed_by_team[team][claimed_square]:
                    return self.Conflict({opponent, opp_claimed_square})
        return None

    def extract_chain(self, row_idx: int, col_idx: int, stuck_unit_points=None,
                      visited_points: Set[Tuple[int, int]] = None) -> Optional[List[Tuple[int, int]]]:
        """
        Returns a chain of units that must move in order, starting from the specified row_idx, col_idx.
        Returns None if the unit cannot move
        """

        if stuck_unit_points is None:
            stuck_unit_points = set()
        if visited_points is None:
            visited_points = set()

        if (row_idx, col_idx) in stuck_unit_points or (row_idx, col_idx) in visited_points:
            return None

        faced_tile, f_row_idx, f_col_idx = self.get_faced_tile(row_idx, col_idx)

        if faced_tile is None or not faced_tile.type.value.is_passable:
            return None
        if faced_tile.is_free():
            return [(row_idx, col_idx)]

        # If the faced tile is occupied by a unit that is also free to move next turn, we can move to it

        chain = self.extract_chain(f_row_idx, f_col_idx, stuck_unit_points, visited_points.union({(row_idx, col_idx)}))
        if chain is not None:
            return chain + [(row_idx, col_idx)]
        else:
            return None

    def get_faced_tile(self, row_idx: int, col_idx: int) -> Tuple[Optional[Tile], int, int]:
        """
        Gets the tile faced by a unit at a row, col. If the tile faces the edge, gives None
        """

        facing_tile = self.tiles[row_idx][col_idx]

        if facing_tile.unit.direction == Direction.RIGHT:
            row_idx, col_idx = row_idx, col_idx + 1
        elif facing_tile.unit.direction == Direction.LEFT:
            row_idx, col_idx = row_idx, col_idx - 1
        elif facing_tile.unit.direction == Direction.UP:
            row_idx, col_idx = row_idx - 1, col_idx
        elif facing_tile.unit.direction == Direction.DOWN:
            row_idx, col_idx = row_idx + 1, col_idx

        # Add more logic for different types of units, if necessary...

        if 0 <= row_idx < len(self.tiles) and 0 <= col_idx < len(self.tiles[row_idx]):
            return self.tiles[row_idx][col_idx], row_idx, col_idx
        return None, row_idx, col_idx


pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Board")


class InteractMode(Enum):
    ADD_MODE = 1
    ERASE_MODE = 2


def main():
    board = Board.from_string(
        [
            "GGWWWGG",
            "GGGGGGG",
            "GGGGGGG",
        ]
    )

    board.tiles[1][0].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
    board.tiles[0][1].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
    board.tiles[1][1].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
    board.tiles[0][4].unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
    board.tiles[1][4].unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)
    board.tiles[2][4].unit = Unit(UnitType.SOLDIER, Direction.LEFT, Team.APPLE)

    add_button = Button(400, 400, 50, 30, "Add", InteractMode.ADD_MODE)
    erase_button = Button(460, 400, 50, 30, "Erase", InteractMode.ERASE_MODE)

    # Start in add mode
    current_interact_mode = InteractMode.ADD_MODE
    current_game_state = GameState.EDIT_TROOPS

    running = True
    while running:
        screen.fill((255, 255, 255))

        # Render the board
        board.render(current_game_state)

        # Render buttons
        add_button.active = current_interact_mode == InteractMode.ADD_MODE
        erase_button.active = current_interact_mode == InteractMode.ERASE_MODE
        add_button.draw(screen)
        erase_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check for button clicks
                if add_button.check_click(pos):
                    current_interact_mode = InteractMode.ADD_MODE
                elif erase_button.check_click(pos):
                    current_interact_mode = InteractMode.ERASE_MODE
                else:
                    # Handle board clicks
                    col = pos[0] // TILE_SIZE
                    row = pos[1] // TILE_SIZE
                    if row < len(board.tiles) and col < len(board.tiles[0]):
                        if current_interact_mode == InteractMode.ADD_MODE:
                            if board.tiles[row][col].is_free() and board.tiles[row][col].is_placeable:
                                board.tiles[row][col].unit = Unit(UnitType.SOLDIER, Direction.RIGHT, Team.ORANGE)
                        elif current_interact_mode == InteractMode.ERASE_MODE:
                            board.tiles[row][col].unit = None

        pygame.time.delay(20)

        if current_game_state == GameState.PLAY_TROOPS:
            board.update()

    pygame.quit()


if __name__ == "__main__":
    main()
