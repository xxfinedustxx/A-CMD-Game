class Player:
    def __init__(self, room_r = 4, room_c = 4):
        self.r = room_r
        self.c = room_c
        self.symbol = " @ "
        self.in_flight_mode = False

    def move(self, dr, dc, room_layout):
        notallowed = ["=#=","==="," ║ ","[%]","⋱⋱ "," ⋰⋰",]
        new_r = self.r + dr
        new_c = self.c + dc

        target_tile = room_layout[new_r][new_c]
        if target_tile not in notallowed:
            self.r = new_r
            self.c = new_c
            return True
        return False