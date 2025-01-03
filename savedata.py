import json
from typing import Dict

from level import Level


def load_levels(filename: str) -> list:
    levels = []
    with open(filename, 'r') as json_file:
        levels_serialized = json.load(json_file)
        for level_serial in levels_serialized.values():
            levels.append(Level.from_serialized(level_serial))
    return levels

def save_levels(filename: str, levels: list) -> None:
    mega_dict = {}
    for level_id, level in enumerate(levels):
        mega_dict["Level " + str(level_id + 1)] = level.serialize()

    json_data = json.dumps(mega_dict)
    with open(filename, "w") as json_file:
        json_file.write(json_data)

def save_user_state(filename: str, data: Dict[str, int]) -> None:
    json_data = json.dumps(data)
    with open(filename, "w") as json_file:
        json_file.write(json_data)

def load_user_state(filename: str) -> Dict[str, int]:
    with open(filename, 'r') as json_file:
         return json.load(json_file)