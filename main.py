import sys
import os
import time
from colorama import init
from game.world.world import SpaceDust
from game.world.world import render_interior_with_camera
from game.entitys.player import Player
from game.entitys.ship import Ship

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
    
    ship.add_room("ENGINE_ROOM",interior_offset=(8, 8))
    ship.add_room("SQUARE_ROOM",interior_offset =(0,0))
    ship.add_room("SQUARE_ROOM",interior_offset=(0,8))
    ship.add_room("SQUARE_ROOM",interior_offset=(0,16))

    spawn_r, spawn_c = ship.get_console_spawn_cords()
    player = Player(room_r=spawn_r, room_c=spawn_c)

    try:
        last_action_time = 0
        interior_cooldown = 0.15  
        flight_cooldown = 0.005    
        frame = 0
        
        while True:
            
            key = get_key()
            current_time = time.time()

            
            active_cooldown = flight_cooldown if player.in_flight_mode else interior_cooldown

            can_act = False
            if key and (current_time - last_action_time >= active_cooldown):
                can_act = True
                last_action_time = current_time

            if not player.in_flight_mode:
                # --- INTERIOR MODE ---
                screen_buffer = []
                
                
                screen_buffer.append("\033[H\033[J")
                
                screen_buffer.append(f"=== A CMD GAME [Interior mode] [FRAME: {frame}] ===")

                interior_screen = render_interior_with_camera(ship, player, screen_width=40, screen_height=20)
                screen_buffer.append(interior_screen)

                screen_buffer.append("================================")
                screen_buffer.append("Kontrole: W/A/S/D kretanje | E konzola (Flight Mode) | CTRL+C izlaz")

                sys.stdout.write("\n".join(screen_buffer) + "\n")
                sys.stdout.flush()

                if can_act:
                    if key == "w":
                        player.move(-1, 0, ship.interior_grid)
                    elif key == "s":
                        player.move(1, 0, ship.interior_grid)
                    elif key == "a":
                        player.move(0, -1, ship.interior_grid)
                    elif key == "d":
                        player.move(0, 1, ship.interior_grid)
                    elif key == "e":
                        if ship.interior_grid[player.r][player.c] == "[#]":
                            player.in_flight_mode = True
                            sys.stdout.write("\nPrebacivanje u flight mode...\n")
                            sys.stdout.flush()
                            time.sleep(0.5)
                        else:
                            sys.stdout.write("\nCan't interact with item!\n")
                            sys.stdout.flush()
                            time.sleep(0.5)

                time.sleep(0.05) 

            else:
                # --- FLIGHT MODE ---
                grid = [[" " for _ in range(width)] for _ in range(height)]

                # Make dust
                for dust in dust_particles:
                    dust.update()
                    if 0 <= dust.y < height and 0 <= dust.x < width:
                        grid[dust.y][dust.x] = f"{dust.color}{dust.char}"

                # Make ship over the dust

                for r_idx, row in enumerate(ship.flight_hull):
                    for c_idx, char in enumerate(row):
                        if char != " ":
                            screen_y = ship.world_y + r_idx
                            screen_x = ship.world_x + c_idx

                            if 0 <= screen_y < height and 0 <= screen_x < width:
                                grid[screen_y][screen_x] = f"\033[36m{char}\033[0m"

                # Screen output
                sys.stdout.write("\033[H\033[J")
                sys.stdout.write(f"=== A-CMD-GAME [FLIGHT MODE] [FRAME: {frame}] ====================\n")
                for row in grid:
                    sys.stdout.write("".join(row) + "\n")
                    
                sys.stdout.write("============================================================\n")
                sys.stdout.write("Kontrole: W/A/S/D letenje | Q povratak u brod | CTRL+C izlaz\n")
                sys.stdout.flush()

                
                if can_act:
                    if key == "w":
                        ship.move_ship(0, -1)  
                    elif key == "s":
                        ship.move_ship(0, 1)   
                    elif key == "a":
                        ship.move_ship(-1, 0)  
                    elif key == "d":
                        ship.move_ship(1, 0)   
                    elif key == "q":
                        player.in_flight_mode = False
                        sys.stdout.write("\nReturn inside the ship.\n")
                        sys.stdout.flush()
                        time.sleep(0.5)

                frame += 1
                time.sleep(0.02)
            
    except KeyboardInterrupt:
        print("\nSimulation stoped")

if __name__ == "__main__":
    main()