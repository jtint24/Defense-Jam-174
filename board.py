from copy import deepcopy
from typing import NamedTuple, List, Optional, Self, Tuple, Set, Dict

import pygame
from pygame import Surface

from animations import Animation, UnitMovementAnimation, StaticUnitAnimation, UnitDeathAnimation, UnitWinAnimation, \
    FlankAnimation
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from gamestate import GameState
from unit import Tile, Team, TileType, Unit, UnitType, Direction


class Board:
    def __init__(self, tiles: List[List[Tile]]):
        self.tiles = tiles
        self.finished_units_by_team = {
            team: 0
            for team in Team
        }
        self.units_killed_by_team = {
            team: 0
            for team in Team
        }
        self.animations: List[Animation] = []
        self.updates = 0

    @staticmethod
    def row_from_string(row_str: str) -> List[Tile]:
        return [
            Tile(TileType.from_str(code), None)
            for code in row_str
        ]

    @classmethod
    def from_string(cls, board_strs: List[str], editable_columns: Set[int], units: Dict[Tuple[int, int], Unit]) -> Self:
        tiles = [cls.row_from_string(row_str) for row_str in board_strs]
        for row_idx, row in enumerate(tiles):
            for col_idx, tile in enumerate(row):
                tiles[row_idx][col_idx].is_placeable = col_idx in editable_columns

        for unit_point in units:
            tiles[unit_point[0]][unit_point[1]].unit = units[unit_point]

        return Board(tiles)

    @classmethod
    def from_serialized(cls, serialized_data: List[List[Dict[str, Optional[Dict[str, int | str]] | bool | int | str | Tuple[int]]]]) -> Self:
        tiles = []
        for serial_row in serialized_data:
            tile_row = []
            for serial_tile in serial_row:
                tile_row.append(Tile.from_serialized(serial_tile))
            tiles.append(tile_row)

        return Board(tiles)


    def render(self, screen: Surface, game_state: GameState, frame: int):
        # Calculate the offsets to center the board on the screen
        offset_x = (SCREEN_WIDTH - len(self.tiles[0]) * TILE_SIZE) // 2
        offset_y = (SCREEN_HEIGHT - len(self.tiles) * TILE_SIZE) // 2

        rect = pygame.Rect(offset_x - 8, offset_y - 8, TILE_SIZE * len(self.tiles[0]) + 16, TILE_SIZE* len(self.tiles) + 16)
        pygame.draw.rect(screen, (0,0,0), rect, width=8)

        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                # Calculate the screen position of the tile
                tile_x = offset_x + col_idx * TILE_SIZE
                tile_y = offset_y + row_idx * TILE_SIZE

                # Render the tile image
                tile.render(screen, tile_x, tile_y)

                # Render the unit if present (AND it's edit mode cuz if so, no animations)
                # len(animations) == 0 is a total hack, to patch the first frame of play mode where animations haven't been populated yet
                if tile.unit is not None and (game_state != GameState.PLAY_TROOPS or len(self.animations) == 0):
                    screen.blit(tile.unit.get_image(), (tile_x, tile_y))

                # Darken tile if it is not passable or not placeable
                if game_state == GameState.EDIT_TROOPS and (not tile.type.value.is_passable or not tile.is_placeable):
                    dark_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    dark_surface.fill((0, 0, 0, 100))  # Semi-transparent black overlay
                    screen.blit(dark_surface, (tile_x, tile_y))
        for animation in self.animations:
            animation.draw(screen, frame, game_state)

    def row_to_y(self, row_idx: int):
        offset_y = (SCREEN_HEIGHT - len(self.tiles) * TILE_SIZE) // 2
        return row_idx * TILE_SIZE + offset_y

    def col_to_x(self, col_idx: int):
        offset_x = (SCREEN_WIDTH - len(self.tiles[0]) * TILE_SIZE) // 2

        return col_idx * TILE_SIZE + offset_x

    def update(self, frame: int) -> bool:
        "Returns whether the board changed during update"

        self.animations = []
        self.updates += 1

        # Start by populating new_tiles with the base tiles (not units) from the current board
        new_tiles = [
            [
                Tile(tile.type, None, tile.is_placeable, tile.health, tile.rotation, tile.destination)
                for tile in row
            ]
            for row in self.tiles

        ]

        # Then, place units in their new positions, detecting collisions where they exist

        chains, locked_units, victims = self.identify_chains()

        for chain in chains:
            for row_idx, col_idx in chain:
                self.move_unit(new_tiles, row_idx, col_idx)
                if self.get_faced_tile(row_idx, col_idx)[0].type != TileType.TRAPDOOR:
                    if new_tiles[row_idx][col_idx].type != TileType.TRAMPOLINE:
                        self.animations.append(UnitMovementAnimation(frame, self.tiles[row_idx][col_idx].unit, self.col_to_x(col_idx), self.row_to_y(row_idx)))
                    else:
                        self.animations.append(UnitMovementAnimation(frame, self.tiles[row_idx][col_idx].unit, self.col_to_x(col_idx), self.row_to_y(row_idx), self.tiles[row_idx][col_idx].unit.direction))
        for row_idx, col_idx in locked_units:
            if self.tiles[row_idx][col_idx].type != TileType.FINISH_LINE:
                new_tiles[row_idx][col_idx].unit = self.tiles[row_idx][col_idx].unit
                if self.tiles[row_idx][col_idx].type != TileType.TRAPDOOR:
                    self.animations.append(StaticUnitAnimation(frame, self.tiles[row_idx][col_idx].unit, self.col_to_x(col_idx), self.row_to_y(row_idx)))
            else:
                unit = self.tiles[row_idx][col_idx].unit
                self.finished_units_by_team[unit.team] += 1
                # Unit Win!! animation goes here
                self.animations.append(UnitWinAnimation(frame, self.tiles[row_idx][col_idx].unit, self.col_to_x(col_idx), self.row_to_y(row_idx)))

        for unit, row_idx, col_idx in victims:
            self.animations.append(UnitDeathAnimation(frame, unit, self.col_to_x(col_idx), self.row_to_y(row_idx)))

        #logic for all relevant items
        for row_idx, row in enumerate(new_tiles):
            for col_idx, tile in enumerate(row):
                if tile.unit is not None:
                    #Trampolines
                    tile.trampoline_bounce()
                    #Lava
                    if self.tiles[row_idx][col_idx].type == TileType.TRAPDOOR:
                        self.animations.append(UnitDeathAnimation(frame, tile.unit, self.col_to_x(col_idx), self.row_to_y(row_idx)))
                        self.units_killed_by_team[new_tiles[row_idx][col_idx].unit.team] += 1
                        new_tiles[row_idx][col_idx].unit = None
                    #Teleporter
                    elif self.tiles[row_idx][col_idx].type == TileType.TUNNEL:
                        dest = self.tiles[row_idx][col_idx].destination
                        print(str(dest[0])  + ' ' + str(dest[1]))
                        new_tiles[dest[0]][dest[1]].unit = tile.unit
                        tile.unit = None
                        self.animations.append(UnitWinAnimation(frame, tile.unit, self.col_to_x(col_idx), self.row_to_y(row_idx)))
                    else:
                        #Walls
                        faced_tile, faced_row, faced_col = self.get_new_faced_tile(new_tiles, row_idx, col_idx)
                        if faced_tile is not None and faced_tile.type == TileType.WALL:
                            if faced_tile.health > tile.unit.type.value:
                                faced_tile.health -= tile.unit.type.value
                            else:
                                new_tiles[faced_row][faced_col] = Tile(TileType.DEADWALL, None, faced_tile.is_placeable)
        change = self.tiles != new_tiles
        self.tiles = new_tiles

        # Now, we update each troop's strength
        self.update_strength_defense(frame)
        return change

    def update_strength_defense(self, frame: int):
        for row_idx, row in enumerate(self.tiles):
            unit_line = []
            for col_idx, tile in enumerate(row):
                if tile.unit is not None and (len(unit_line) == 0 or tile.unit.team == unit_line[0].team):
                    unit_line.append(tile.unit)
                else:
                    for unit in unit_line:
                        unit.type = UnitType(min(4, len(unit_line)))
                    if tile.unit is None:
                        unit_line = []
                    else:
                        unit_line = [tile.unit]
            for unit in unit_line:
                unit.type = UnitType(min(4, len(unit_line)))

        # ... And we update each troop's defense

        for col_idx in range(len(self.tiles[0])):
            unit_line = []
            start_row_idx = 0
            for row_idx in range(len(self.tiles)):
                tile = self.tiles[row_idx][col_idx]

                if tile.unit is not None and len(unit_line) == 0:
                    unit_line.append(tile.unit)
                    start_row_idx = row_idx
                elif tile.unit is not None and tile.unit.team == unit_line[0].team:
                    unit_line.append(tile.unit)
                else:
                    for unit in unit_line:
                        unit.defense = min(5, len(unit_line))
                    if tile.unit is not None:
                        start_row_idx = row_idx
                        if len(unit_line) > 1:
                            self.animations.append(
                                FlankAnimation(frame, self.row_to_y(start_row_idx), self.row_to_y(row_idx - 1),
                                               self.col_to_x(col_idx)))
                        unit_line = [tile.unit]
                    else:
                        if len(unit_line) > 1:
                            self.animations.append(FlankAnimation(frame,  self.row_to_y(start_row_idx), self.row_to_y(row_idx),
                                                                  self.col_to_x(col_idx)))
                        unit_line = []

            for unit in unit_line:
                unit.defense = min(5, len(unit_line))
            if len(unit_line) > 1:
                self.animations.append(FlankAnimation(frame, self.row_to_y(start_row_idx), self.row_to_y(len(self.tiles)), self.col_to_x(col_idx)))

    def resolve_conflict(self, conflict: "Conflict") -> Set[Tuple[int, int]]:
        team_damage = {team: 0 for team in Team}
        belligerent_coordinates = [c for c in conflict.belligerent_coordinates if self.tiles[c[0]][c[1]].unit is not None]
        print([c for c in conflict.belligerent_coordinates if self.tiles[c[0]][c[1]].unit is None])
        sorted_belligerents = sorted(
            belligerent_coordinates,
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

        for b_row_idx, b_col_idx in sorted_belligerents:
            if (b_row_idx, b_col_idx) not in survivors:
                unit = self.tiles[b_row_idx][b_col_idx].unit
                self.units_killed_by_team[unit.team] += 1

        return survivors

    def move_unit(self, new_tiles: List[List[Tile]], row_idx: int, col_idx: int):
        _, f_row_idx, f_col_idx = self.get_faced_tile(row_idx, col_idx)
        new_tiles[f_row_idx][f_col_idx].unit = self.tiles[row_idx][col_idx].unit

    class Conflict(NamedTuple):
        belligerent_coordinates: Set[Tuple[int, int]]

    def identify_chains(self) -> Tuple[List[List[Tuple[int, int]]], Set[Tuple[int, int]], List[Tuple[Unit, int, int]]]:
        """
        Returns a tuple with two elements.
        The first is a list of chains. Each chain has points in order of how they needed to move.
        The second is a list of units that cannot move.
        The third is a list of units that are dying this turn
        Every unit is in a chain or it cannot move.
        """
        chains_starting_points = {}
        identified_unit_points = set()
        locked_unit_points = set()
        victims = []

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

                    if faced_tile is not None and faced_tile.type.value.is_passable:
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
                    victims.append((self.tiles[b_row_idx][b_col_idx].unit, b_row_idx, b_col_idx))
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

        return list(chains_starting_points.values()), locked_unit_points, victims

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

    def get_number_of_units_by_team(self, team: Team) -> int:
        count = 0
        for row_idx, row in enumerate(self.tiles):
            for col_idx, tile in enumerate(row):
                if tile.unit is not None and tile.unit.team == team:
                    count += 1
        return count

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

    def get_new_faced_tile(self, new_tiles: List[List[Tile]], row_idx: int, col_idx: int) -> Tuple[Optional[Tile], int, int]:
        """
        Gets the tile faced by a unit at a row, col. If the tile faces the edge, gives None
        """

        facing_tile = new_tiles[row_idx][col_idx]

        if facing_tile.unit.direction == Direction.RIGHT:
            row_idx, col_idx = row_idx, col_idx + 1
        elif facing_tile.unit.direction == Direction.LEFT:
            row_idx, col_idx = row_idx, col_idx - 1
        elif facing_tile.unit.direction == Direction.UP:
            row_idx, col_idx = row_idx - 1, col_idx
        elif facing_tile.unit.direction == Direction.DOWN:
            row_idx, col_idx = row_idx + 1, col_idx

        # Add more logic for different types of units, if necessary...

        if 0 <= row_idx < len(new_tiles) and 0 <= col_idx < len(new_tiles[row_idx]):
            return new_tiles[row_idx][col_idx], row_idx, col_idx
        return None, row_idx, col_idx

    def serialize_board(self) -> List[List[Dict[str, Optional[Dict[str, int | str]] | bool | int | str | Tuple[int]]]]:
        serialized_tiles = []
        for row in self.tiles:
            serialized_row = []
            for tile in row:
                serialized_row.append(tile.serialize_tile())
            serialized_tiles.append(serialized_row)

        return serialized_tiles


    def __deepcopy__(self, memo={}):
        id_self = id(self)  # memoization avoids unnecessary recursion
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                deepcopy(self.tiles, memo))
            memo[id_self] = _copy
        return _copy
