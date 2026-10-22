import sys
import os
import time
from colorama import init
from game.world.world import SpaceDust
from game.entitys.player import Player
from game.entitys.ship import Ship
from game.engine import GameEngine

if os.name == "nt":
    import msvcrt
    def get_key():
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                return key.decode('utf-8').lower()
            except UnicodeDecodeError:
                return ''
        return None
else:
    import sys, select
    def get_key():
        if select.select([sys.stdin],[],[],0)[0]:
            return sys.stdin.read(1).lower()
        return None

init(autoreset=True)

def main():
    if os.name == "nt":
        os.system("cls")
        os.system("mode con cols=110 lines=43")
    else:
        os.system("clear")

    print("Loading...")
    time.sleep(0.5)

    width, height = 110, 40

    galaxy_centers = [
        (width // 4, height // 3),
        (width // 2, height // 2),
        ((width * 3) // 4, (height * 2) // 3)
    ]
    
    dust_particles = [SpaceDust(width, height, galaxy_centers) for _ in range(50)]

    ship = Ship(x=(width//2), y=(height//2))
    
    ship.add_room("ENGINE_ROOM", interior_offset=(8, 0))
    ship.add_room("SQUARE_ROOM", interior_offset=(8, 8))
    ship.add_room("SQUARE_ROOM", interior_offset=(0, 0))
    ship.add_room("ANGLED_ROOM_RIGHT_UP", interior_offset=(0, 8))

    spawn_r, spawn_c = ship.get_console_spawn_cords()
    player = Player(room_r=spawn_r, room_c=spawn_c)

    engine = GameEngine(ship, player, width, height, dust_particles)
    engine.run(get_key)

if __name__ == "__main__":
    main()