import time
import sys
import traceback
from game.world.world import render_interior_with_camera
from game.entitys.asteroids import Asteroid

class GameEngine:
    def __init__(self, ship, player, width, height, dust_particles):
        self.ship = ship
        self.player = player
        self.width = width
        self.height = height
        self.dust_particles = dust_particles
        
        self.asteroids = [Asteroid(width, height) for _ in range(4)]
        
        self.target_tps = 10
        self.tick_interval = 1.0 / self.target_tps
        
        self.frame_count = 0
        self.tick_count = 0
        self.fps = 0
        self.tps = 0
        self.last_timer = time.time()

        self.last_move_time = 0
        self.move_cooldown = 0.08
        self.is_colliding = False

        # Sustav oštećenja / cooldown za štetu
        self.last_damage_time = 0
        self.damage_cooldown = 1.0  # 1 sekunda imuniteta između udara
        self.last_hit_flash = 0     # Za vizualni blink oklopa pri udarcu

    def check_collisions(self):
        """Vraća asteroid s kojim je došlo do sudara, ili None"""
        if not self.player.in_flight_mode:
            return None

        hull = self.ship.flight_hull
        if not hull:
            return None
            
        ship_x = self.ship.world_x
        ship_y = self.ship.world_y

        for ast in self.asteroids:
            for ast_r, row in enumerate(ast.shape):
                for ast_c, char in enumerate(row):
                    if char != " ":
                        pixel_ast_x = int(ast.x) + ast_c
                        pixel_ast_y = int(ast.y) + ast_r

                        for ship_r, s_row in enumerate(hull):
                            for ship_c, s_char in enumerate(s_row):
                                if s_char != " ":
                                    pixel_ship_x = ship_x + ship_c
                                    pixel_ship_y = ship_y + ship_r
                                    if pixel_ast_x == pixel_ship_x and pixel_ast_y == pixel_ship_y:
                                        return ast  # Vraćamo konkretan asteroid koji je udario!
        return None

    def apply_damage(self, colliding_asteroid, current_time):
        """Nanošenje štete ovisno o tieru asteroida (Tier 1 = 0 damage)"""
        if colliding_asteroid:
            tier = getattr(colliding_asteroid, 'tier', 1)
            
            # Tier 1 ne radi nikakvu štetu (samo detekcija sudara)
            if tier == 1:
                return

            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.last_damage_time = current_time
                self.last_hit_flash = current_time
                
                # Šteta raste ovisno o tieru asteroida (npr. Tier 2 = 10, Tier 3 = 15, Tier 4 = 20)
                damage_amount = tier * 5
                
                if hasattr(self.ship, 'rooms') and self.ship.rooms:
                    for room in self.ship.rooms:
                        if hasattr(room, 'hp'):
                            room.hp = max(0, room.hp - damage_amount)
                elif hasattr(self.ship, 'hp'):
                    self.ship.hp = max(0, self.ship.hp - damage_amount)

    def run(self, get_key_func):
        last_time = time.time()
        tick_accumulator = 0.0
        
        try:
            while True:
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time
                
                tick_accumulator += delta_time
                
                self.frame_count += 1
                if current_time - self.last_timer >= 1.0:
                    self.fps = self.frame_count
                    self.tps = self.tick_count
                    self.frame_count = 0
                    self.tick_count = 0
                    self.last_timer = current_time

                key = get_key_func()
                can_move = (current_time - self.last_move_time) >= self.move_cooldown

                # --- Dust ---
                for dust in self.dust_particles:
                    dust.update()
                    time.sleep(0.0002)

                # --- 10Hz TICK ---
                while tick_accumulator >= self.tick_interval:
                    tick_accumulator -= self.tick_interval
                    self.tick_count += 1
                    
                    for ast in self.asteroids:
                        ast.update()

                    colliding_ast = self.check_collisions()
                    self.is_colliding = (colliding_ast is not None)
                    
                    if self.is_colliding:
                        self.apply_damage(colliding_ast, current_time)

                if not self.player.in_flight_mode:
                    # --- INTERIOR MODE ---
                    if key:
                        if key in ["w", "s", "a", "d"] and can_move:
                            self.last_move_time = current_time
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
                                sys.stdout.write("\nTransferring to flight mode...\n")
                                sys.stdout.flush()
                                time.sleep(0.5)
                            else:
                                sys.stdout.write("\nCan't interact with item!\n")
                                sys.stdout.flush()
                                time.sleep(0.5)

                    screen_buffer = []
                    screen_buffer.append("\033[H\033[J")
                    screen_buffer.append(f"=== A CMD GAME [Interior mode] [FPS: {self.fps} | TPS: {self.tps}] ===")

                    interior_screen = render_interior_with_camera(self.ship, self.player, screen_width=40, screen_height=20)
                    screen_buffer.append(interior_screen)

                    screen_buffer.append("================================")
                    screen_buffer.append("Controles: W/A/S/D move | E interact | CTRL+C exit")

                    sys.stdout.write("\n".join(screen_buffer) + "\n")
                    sys.stdout.flush()

                else:
                    # --- FLIGHT MODE ---
                    if key:
                        if key in ["w", "s", "a", "d"] and can_move:
                            self.last_move_time = current_time
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

                    hp, total_weight, total_thrust = self.ship.get_ship_stats()

                    grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
                    
                    for dust in self.dust_particles:
                        if 0 <= dust.y < self.height and 0 <= dust.x < self.width:
                            grid[int(dust.y)][int(dust.x)] = f"{dust.color}{dust.char}"

                    for ast in self.asteroids:
                        for r_idx, row in enumerate(ast.shape):
                            for c_idx, char in enumerate(row):
                                ax = int(ast.x) + c_idx
                                ay = int(ast.y) + r_idx
                                if 0 <= ay < self.height and 0 <= ax < self.width:
                                    if char != " ":
                                        grid[ay][ax] = f"{ast.color}{char}\033[0m"
                                    else:
                                        grid[ay][ax] = " "

                    # Crveni flash oklopa pri udarcu (samo za tier > 1 ili općenito na sudar)
                    ship_color = "\033[31m" if (current_time - self.last_hit_flash < 0.3) else "\033[36m"

                    for r_idx, row in enumerate(self.ship.flight_hull):
                        for c_idx, char in enumerate(row):
                            if char != " ":
                                screen_y = self.ship.world_y + r_idx
                                screen_x = self.ship.world_x + c_idx
                                if 0 <= screen_y < self.height and 0 <= screen_x < self.width:
                                    grid[screen_y][screen_x] = f"{ship_color}{char}\033[0m"
                    

                    collision_warning = " [Colision!]" if self.is_colliding else ""

                    screen_buffer = []
                    screen_buffer.append("\033[H\033[J")
                    screen_buffer.append(f"=== A-CMD-GAME [FLIGHT MODE] [FPS: {self.fps} | TPS: {self.tps}]{collision_warning} ====================\n")
                    
                    for row in grid:
                        screen_buffer.append("".join(row))
                        
                    screen_buffer.append(f"------------------------------------------------------------")
                    screen_buffer.append(f" [POS: X:{self.ship.world_x} Y:{self.ship.world_y}] | [HP: {hp}] | [WEIGHT: {total_weight}t] | [THRUST: {total_thrust}]")
                    screen_buffer.append(f"============================================================")
                    screen_buffer.append(" Controles: W/A/S/D | Q back to ship | CTRL+C exit")

                    sys.stdout.write("\n".join(screen_buffer) + "\n")
                    sys.stdout.flush()

                time.sleep(0.001)
                    
        except KeyboardInterrupt:
            print("\nSimulation stoped")
        except Exception as e:
            print(f"\n[Error in sim]: {e}")
            traceback.print_exc()
            input("\nPres Enter to exit...")