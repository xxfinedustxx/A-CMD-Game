import copy
from game.assets.ship_assets import (
    SQUARE_ROOM, SQUARE_ROOM_HULL,
    ENGINE_ROOM, ENGINE_ROOM_HULL
)

class Ship:
    def __init__(self, x = 0, y = 0):
        self.world_x = x
        self.world_y = y

        self.rooms = [
            {
                "type": "SQUARE_ROOM",
                "interior": copy.deepcopy(SQUARE_ROOM),
                "hull": SQUARE_ROOM_HULL,
                "offset": (0, 0)
            }
        ]

        self.nav_console_pos = (3, 4)
        self.interior_grid = []
        self._rebuild_interior_grid()

    def _rebuild_interior_grid(self):
        if not self.rooms:
            self.interior_grid = [[" "]]
            return

        min_r = min(r["offset"][0] for r in self.rooms)
        min_c = min(r["offset"][1] for r in self.rooms)
        
        max_r = max(r["offset"][0] + len(r["interior"]) for r in self.rooms)
        max_c = max(r["offset"][1] + max(len(row) for row in r["interior"]) for r in self.rooms)

        height = max_r - min_r
        width = max_c - min_c

        grid = [[" " for _ in range(width)] for _ in range(height)]

        for room in self.rooms:
            off_r, off_c = room["offset"]
            r_offset = off_r - min_r
            c_offset = off_c - min_c

            interior = room["interior"]
            for r_idx, row in enumerate(interior):
                for c_idx, char in enumerate(row):
                    if char != " ": # Ne prepisuj praznine bespotrebno
                        grid[r_offset + r_idx][c_offset + c_idx] = char

        self.interior_grid = grid

    def add_room(self, room_type, offset_r, offset_c):
        if room_type == "ENGINE_ROOM":
            interior = copy.deepcopy(ENGINE_ROOM)
            hull = ENGINE_ROOM_HULL
        else:
            interior = copy.deepcopy(SQUARE_ROOM)
            hull = SQUARE_ROOM_HULL

        self.rooms.append({
            "type": room_type,
            "interior": interior,
            "hull": hull,
            "offset": (offset_r, offset_c)
        })

        self._rebuild_interior_grid()

    def move_ship(self, dx, dy):
        self.world_x += dx
        self.world_y += dy

    def get_console_spawn_cords(self):
        console_r, console_c = self.nav_console_pos
        layout = self.interior_grid

        possible_offsets = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        for dr, dc in possible_offsets:
            nr, nc = console_r + dr, console_c + dc
            if 0 <= nr < len(layout) and 0 <= nc < len(layout[0]):
                target_tile = layout[nr][nc]
                if target_tile not in ["=#=", "===", " ║ ", "[%]", "[#]"]:
                    return (nr, nc)
        return (console_r, console_c)