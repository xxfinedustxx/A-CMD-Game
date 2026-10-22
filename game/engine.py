import time
import sys
import traceback
from game.world.world import render_interior_with_camera

class GameEngine:
    def __init__(self, ship, player, width, height, dust_particles):
        self.ship = ship
        self.player = player
        self.width = width
        self.height = height
        self.dust_particles = dust_particles
        
        # Postavke za TPS (Tick Rate) i mjerenje performansi
        self.target_tps = 10
        self.tick_interval = 1.0 / self.target_tps
        
        self.frame_count = 0
        self.tick_count = 0
        self.fps = 0
        self.tps = 0
        self.last_timer = time.time()

    def run(self, get_key_func):
        last_time = time.time()
        tick_accumulator = 0.0
        
        try:
            while True:
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time
                
                tick_accumulator += delta_time
                
                # Izračun FPS-a i TPS-a svaku 1 sekundu
                self.frame_count += 1
                if current_time - self.last_timer >= 1.0:
                    self.fps = self.frame_count
                    self.tps = self.tick_count
                    self.frame_count = 0
                    self.tick_count = 0
                    self.last_timer = current_time

                # Čitanje unosa tipki u svakom frameu (trenutna reakcija)
                key = get_key_func()

                if not self.player.in_flight_mode:
                    # --- INTERIOR MODE ---
                    if key:
                        if key == "w":
                            self.player.move(-1, 0, self.ship.interior_grid)
                        elif key == "s":
                            self.player.move(1, 0, self.ship.interior_grid)
                        elif key == "a":
                            self.player.move(0, -1, self.ship.interior_grid)
                        elif key == "d":
                            self.player.move(0, 1, self.ship.interior_grid)
                        elif key == "e":
                            if self.ship.interior_grid[self.player.r][self.player.c] == "[#]":
                                self.player.in_flight_mode = True
                                sys.stdout.write("\nPrebacivanje u flight mode...\n")
                                sys.stdout.flush()
                                time.sleep(0.5)
                            else:
                                sys.stdout.write("\nCan't interact with item!\n")
                                sys.stdout.flush()
                                time.sleep(0.5)

                    # Render unutrašnjosti
                    screen_buffer = []
                    screen_buffer.append("\033[H\033[J")
                    screen_buffer.append(f"=== A CMD GAME [Interior mode] [FPS: {self.fps} | TPS: {self.tps}] ===")

                    interior_screen = render_interior_with_camera(self.ship, self.player, screen_width=40, screen_height=20)
                    screen_buffer.append(interior_screen)

                    screen_buffer.append("================================")
                    screen_buffer.append("Kontrole: W/A/S/D kretanje | E konzola (Flight Mode) | CTRL+C izlaz")

                    sys.stdout.write("\n".join(screen_buffer) + "\n")
                    sys.stdout.flush()

                else:
                    # --- FLIGHT MODE ---
                    # Ovdje vrtimo fiziku točno na 10Hz (TPS)
                    while tick_accumulator >= self.tick_interval:
                        tick_accumulator -= self.tick_interval
                        self.tick_count += 1
                        
                        # Ažuriranje pozicije zvjezdane prašine po ticku
                        for dust in self.dust_particles:
                            dust.update()

                    # Kontrola kretanja broda tipkama
                    if key:
                        if key == "w":
                            self.ship.move_ship(0, -1, self.width, self.height)
                        elif key == "s":
                            self.ship.move_ship(0, 1, self.width, self.height)
                        elif key == "a":
                            self.ship.move_ship(-1, 0, self.width, self.height)
                        elif key == "d":
                            self.ship.move_ship(1, 0, self.width, self.height)
                        elif key == "q":
                            self.player.in_flight_mode = False
                            sys.stdout.write("\nReturn inside the ship.\n")
                            sys.stdout.flush()
                            time.sleep(0.5)

                    # Renderiranje Flight Mode-a (vrti se maksimalnom brzinom za visoki FPS)
                    hp, total_weight, total_thrust = self.ship.get_ship_stats()

                    grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
                    for dust in self.dust_particles:
                        if 0 <= dust.y < self.height and 0 <= dust.x < self.width:
                            grid[dust.y][dust.x] = f"{dust.color}{dust.char}"

                    for r_idx, row in enumerate(self.ship.flight_hull):
                        for c_idx, char in enumerate(row):
                            if char != " ":
                                screen_y = self.ship.world_y + r_idx
                                screen_x = self.ship.world_x + c_idx
                                if 0 <= screen_y < self.height and 0 <= screen_x < self.width:
                                    grid[screen_y][screen_x] = f"\033[36m{char}\033[0m"

                    sys.stdout.write("\033[H\033[J")
                    sys.stdout.write(f"=== A-CMD-GAME [FLIGHT MODE] [FPS: {self.fps} | TPS: {self.tps}] ====================\n")
                    for row in grid:
                        sys.stdout.write("".join(row) + "\n")
                        
                    sys.stdout.write(f"------------------------------------------------------------\n")
                    sys.stdout.write(f" [POS: X:{self.ship.world_x} Y:{self.ship.world_y}] | [HP: {hp}] | [TEŽINA: {total_weight}t] | [POTISAK: {total_thrust}]\n")
                    sys.stdout.write(f"============================================================\n")
                    sys.stdout.write(" Kontrole: W/A/S/D letenje | Q povratak u brod | CTRL+C izlaz\n")
                    sys.stdout.flush()

                # Minimalni sleep da ne opteretimo CPU na 100%
                time.sleep(0.001)
                    
        except KeyboardInterrupt:
            print("\nSimulation stoped")
        except Exception as e:
            print(f"\n[GREŠKA U SIMULACIJI]: {e}")
            traceback.print_exc()
            input("\nPritisni Enter za izlaz...")