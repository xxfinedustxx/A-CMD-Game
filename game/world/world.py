import random
from colorama import Fore, Style

class SpaceDust:
    def __init__(self, screen_width, screen_height, galaxy_centers):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        center_x, center_y = random.choice(galaxy_centers)
        self.x = int(random.gauss(center_x, screen_width / 6)) % screen_width
        self.y = int(random.gauss(center_y, screen_height / 4)) % screen_height
        
        rand_val = random.random()
        if rand_val < 0.5:
            self.char = "."
            self.speed = 0.4
        elif rand_val < 0.8:
            self.char = ","
            self.speed = 0.8
        elif rand_val < 0.95:
            self.char = ":"
            self.speed = 1.2
        else:
            self.char = "*"
            self.speed = 1.8
            
        stellar_palette = [
            Fore.WHITE,
            Style.BRIGHT + Fore.WHITE,
            Fore.LIGHTYELLOW_EX,
            Style.RESET_ALL
        ]
        
        self.color = random.choices(
            stellar_palette, 
            weights=[50, 30, 10, 10], 
            k=1
        )[0]
        
        self.x_progress = 0.0

    def update(self, ship_dx=0.5):
        self.x_progress -= self.speed + ship_dx
        
        if self.x_progress <= -1.0:
            self.x -= 1
            self.x_progress = 0.0
            
        # Wrapping rubova ekrana
        if self.x < 0:
            self.x = self.screen_width - 1
        elif self.x >= self.screen_width:
            self.x = 0

def render_interior_with_camera(ship, player, screen_width = 15, screen_height = 11):

    center_screem_r = screen_height // 2
    center_screem_c = screen_width // 2

    layout = ship.interior_grid
    rendered_rows = [ ]

    for sr in range(screen_height):
        row_str = ""
        for sc in range(screen_width):

            world_r = player.r + (sr - center_screem_r)
            world_c = player.c + (sc - center_screem_c)

            if world_r == player.r and world_c == player.c:
                row_str += player.symbol
            elif 0 <= world_r < len(layout) and 0 <= world_c < len(layout[0]):
                row_str += layout[world_r][world_c]
            else:
                row_str += "   "
        rendered_rows.append(row_str)
    return "\n".join(rendered_rows)



