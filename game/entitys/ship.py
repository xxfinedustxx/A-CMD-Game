import copy
from game.assets.ship_assets import (
    SQUARE_ROOM, SQUARE_ROOM_HULL,
    ENGINE_ROOM, ENGINE_ROOM_HULL,
    EMPTY_ROOM,
    ANGLED_ROOM_RIGHT_UP, ANGLED_ROOM_RIGHT_UP_HULL 
)

class Ship:
    def __init__(self, x = 0, y = 0):
        self.world_x = x
        self.world_y = y

        self.rooms = []
        self.nav_console_pos = (3, 4)
        
        self.interior_grid = []
        self.flight_hull = []

        self.add_room("SQUARE_ROOM", interior_offset=(0, 0))

    def add_room(self, room_type, interior_offset, auto_generated = False):
        if room_type == "ENGINE_ROOM":
            interior = copy.deepcopy(ENGINE_ROOM)
            hull = ENGINE_ROOM_HULL
        elif room_type == "EMPTY":
            interior = copy.deepcopy(EMPTY_ROOM)
            hull = []
        elif room_type == "ANGLED_ROOM_RIGHT_UP":
            interior = copy.deepcopy(ANGLED_ROOM_RIGHT_UP)
            hull = ANGLED_ROOM_RIGHT_UP_HULL
        else:
            interior = copy.deepcopy(SQUARE_ROOM)
            hull = SQUARE_ROOM_HULL

        self.rooms.append({
            "type": room_type,
            "interior": interior,
            "hull": hull,
            "interior_offset": interior_offset,
            "flight_offset": (0, 0),
            "auto_generated": auto_generated
        })

        self._rebuild_grids()

    def _rebuild_grids(self):
        if not self.rooms:
            self.interior_grid = [[" "]]
            self.flight_hull = [[" "]]
            return

        self.rooms = [r for r in self.rooms if not r.get("auto_generated", False)]

        user_rooms = list(self.rooms)
        for i in range(len(user_rooms)):
            for j in range(i + 1, len(user_rooms)):
                r1 = user_rooms[i]
                r2 = user_rooms[j]

                off1 = r1["interior_offset"]
                off2 = r2["interior_offset"]

                diff_r = off2[0] - off1[0]
                diff_c = off2[1] - off1[1]

                if abs(diff_r) == 16 and diff_c == 0:
                    mid_offset = (min(off1[0], off2[0]) + 8, off1[1])
                    path_blocked = any(
                        r["interior_offset"][1] == off1[1] and min(off1[0], off2[0]) < r["interior_offset"][0] < max(off1[0], off2[0]) for r in self.rooms
                    )
                    if not path_blocked and not any(r["interior_offset"] == mid_offset for r in self.rooms):
                        w1 = len(r1["hull"][0]) if r1["hull"] else 5
                        w2 = len(r2["hull"][0]) if r2["hull"] else 5
                        empty_width = max(w1, w2)
                        dynamic_empty_hull = [[" " for _ in range(empty_width)] for _ in range(3)]

                        self.rooms.append({
                            "type": "EMPTY",
                            "interior": copy.deepcopy(EMPTY_ROOM),
                            "hull": dynamic_empty_hull,
                            "interior_offset": mid_offset,
                            "auto_generated": True
                        })

                elif abs(diff_c) == 16 and diff_r == 0:
                    mid_offset = (off1[0], min(off1[1], off2[1]) + 8)
                    path_blocked = any(
                        r["interior_offset"][0] == off1[0] and min(off1[1], off2[1]) < r["interior_offset"][1] < max(off1[1], off2[1]) for r in self.rooms
                    )
                    if not path_blocked and not any(r["interior_offset"] == mid_offset for r in self.rooms):
                        w1 = len(r1["hull"][0]) if r1["hull"] else 5
                        w2 = len(r2["hull"][0]) if r2["hull"] else 5
                        empty_width = max(w1, w2)
                        dynamic_empty_hull = [[" " for _ in range(empty_width)] for _ in range(3)]

                        self.rooms.append({
                            "type": "EMPTY",
                            "interior": copy.deepcopy(EMPTY_ROOM),
                            "hull": dynamic_empty_hull,
                            "interior_offset": mid_offset,
                            "auto_generated": True
                        })

        # --- interior grid builder ---
        min_r = min(r["interior_offset"][0] for r in self.rooms)
        min_c = min(r["interior_offset"][1] for r in self.rooms)

        max_r_int = max(r["interior_offset"][0] + len(r["interior"]) for r in self.rooms)
        max_c_int = max(r["interior_offset"][1] + max(len(row) for row in r["interior"]) for r in self.rooms)

        int_height = max_r_int - min_r
        int_width = max_c_int - min_c
        int_grid = [["   " for _ in range(int_width)] for _ in range(int_height)]
        
        for room in self.rooms:
            if room["type"] == "EMPTY":
                continue  
                
            off_r, off_c = room["interior_offset"]
            r_offset = off_r - min_r
            c_offset = off_c - min_c

            for r_idx, row in enumerate(room["interior"]):
                for c_idx, char in enumerate(row):
                    target_r = r_offset + r_idx
                    target_c = c_offset + c_idx

                    if char not in ["=#=", "===", " ║ ", "[%]"]: 
                        int_grid[target_r][target_c] = char
        
        wall_candidates = {}

        for room in self.rooms:
            if room["type"] == "EMPTY":
                continue

            off_r, off_c = room["interior_offset"]
            r_offset = off_r - min_r
            c_offset = off_c - min_c

            for r_idx, row in enumerate(room["interior"]):
                for c_idx, char in enumerate(row):
                    if char in ["=#=", "===", " ║ ", "[%]"]:
                        target_r = r_offset + r_idx
                        target_c = c_offset + c_idx
                        
                        if (target_r, target_c) not in wall_candidates:
                            wall_candidates[(target_r, target_c)] = []

                        total_doors_in_row = sum(1 for tile in row if tile == "[%]")
                        
                        wall_candidates[(target_r, target_c)].append({
                            "char": char,
                            "doors": total_doors_in_row,
                            "room_type": room["type"]
                        })

        for pos, candidates in wall_candidates.items():
            target_r, target_c = pos
            if len(candidates) == 1:
                int_grid[target_r][target_c] = candidates[0]["char"]
            else:
                candidates.sort(key=lambda x: x["doors"], reverse=True)
                winner = candidates[0]
                runner_up = candidates[1]
                
                if winner["doors"] == runner_up["doors"]:
                    if "ENGINE_ROOM" in [winner["room_type"], runner_up["room_type"]]:
                        engine_candidate = next(c for c in candidates if c["room_type"] == "ENGINE_ROOM")
                        int_grid[target_r][target_c] = engine_candidate["char"]
                    else:
                        int_grid[target_r][target_c] = winner["char"]
                else:
                    int_grid[target_r][target_c] = winner["char"]    

        for room in self.rooms:
            if room["type"] != "EMPTY":
                continue

            off_r, off_c = room["interior_offset"]
            r_offset = off_r - min_r
            c_offset = off_c - min_c

            for r_idx, row in enumerate(room["interior"]):
                for c_idx, char in enumerate(row):
                    target_r = r_offset + r_idx
                    target_c = c_offset + c_idx

                    if int_grid[target_r][target_c] == " ":
                        int_grid[target_r][target_c] = char
        notallowed = ["   ", "=#=", "===", " ║ ", "[%]"]
        for r_idx in range(len(int_grid)):
            for c_idx in range(len(int_grid[0])):
                if int_grid[r_idx][c_idx] == "[%]":
                    # U D check
                    if 0 <= r_idx - 1 < len(int_grid) and 0 <= r_idx + 1 < len(int_grid):
                        top_tile = int_grid[r_idx - 1][c_idx]
                        bot_tile = int_grid[r_idx + 1][c_idx]
                        if top_tile not in notallowed and bot_tile not in notallowed:
                            int_grid[r_idx][c_idx] = "[ ]"
                    
                    # L R check
                    if 0 <= c_idx - 1 < len(int_grid[0]) and 0 <= c_idx + 1 < len(int_grid[0]):
                        left_tile = int_grid[r_idx][c_idx - 1]
                        right_tile = int_grid[r_idx][c_idx + 1]
                        if left_tile not in notallowed and right_tile not in notallowed:
                            int_grid[r_idx][c_idx] = "[ ]"
        self.interior_grid = int_grid

        # --- flight grid builder ---
        unique_r = sorted(list(set(r["interior_offset"][0] for r in self.rooms)))
        unique_c = sorted(list(set(r["interior_offset"][1] for r in self.rooms)))

        max_r_idx = len(unique_r) - 1

        for room in self.rooms:
            r_val, c_val = room["interior_offset"]
            
            r_idx = unique_r.index(r_val) if r_val in unique_r else 0
            c_idx = unique_c.index(c_val) if c_val in unique_c else 0

            mirrored_r_idx = max_r_idx - r_idx

            flight_r = c_idx * len(room["hull"])
            flight_c = mirrored_r_idx * 7  

            room["flight_offset"] = (flight_r, flight_c)

        f_min_r = min(r["flight_offset"][0] for r in self.rooms)
        f_min_c = min(r["flight_offset"][1] for r in self.rooms) 

        max_r_hull = max(r["flight_offset"][0] + len(r["hull"]) for r in self.rooms)
        max_c_hull = max(r["flight_offset"][1] + max(len(row) for row in r["hull"]) for r in self.rooms)

        hull_height = max_r_hull - f_min_r
        hull_width = max_c_hull - f_min_c
        hull_grid = [[" " for _ in range(hull_width)] for _ in range(hull_height)]

        for room in self.rooms:
            off_r, off_c = room["flight_offset"]
            r_offset = off_r - f_min_r
            c_offset = off_c - f_min_c
            for r_idx, row in enumerate(room["hull"]):
                for c_idx, char in enumerate(row):
                    if char != " ":
                        hull_grid[r_offset + r_idx][c_offset + c_idx] = char
                        
        self.flight_hull = hull_grid

    def move_ship(self, dx, dy):
        self.world_x += dx
        self.world_y += dy

    def get_console_spawn_cords(self):
        min_r = min(r["interior_offset"][0] for r in self.rooms) if self.rooms else 0
        min_c = min(r["interior_offset"][1] for r in self.rooms) if self.rooms else 0

        base_room = next((r for r in self.rooms if r["interior_offset"] == (0, 0)), self.rooms[0])
        
        off_r, off_c = base_room["interior_offset"]
        console_r = (off_r - min_r) + self.nav_console_pos[0]
        console_c = (off_c - min_c) + self.nav_console_pos[1]

        layout = self.interior_grid
        possible_offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dr, dc in possible_offsets:
            nr, nc = console_r + dr, console_c + dc
            if 0 <= nr < len(layout) and 0 <= nc < len(layout[0]):
                target_tile = layout[nr][nc]
                if target_tile not in ["=#=", "===", " ║ ", "[%]", "[#]"]:
                    return (nr, nc)
        return (console_r, console_c)