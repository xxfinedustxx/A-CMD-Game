import random
from game.assets.asteroid_assets import ASTEROID_TYPES

class Asteroid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.type_key = random.choice(list(ASTEROID_TYPES.keys()))
        self.data = ASTEROID_TYPES[self.type_key]
        
        self.name = self.data["name"]
        self.max_hp = self.data["hp"]
        self.hp = self.max_hp
        self.color = self.data["color"]
        self.shape = self.data["shape"]
        self.drops = self.data["drops"]
        
        self.reset()

    def reset(self):

        h_height = len(self.shape)
        h_width = len(self.shape[0]) if self.shape else 1

        self.x = float(self.width)
        self.y = float(random.randint(0, max(0, self.height - h_height)))
        
        self.vx = random.uniform(-0.6, -0.2)
        self.vy = random.uniform(-0.05, 0.05)  

    def update(self):
        self.x += self.vx
        self.y += self.vy

        h_width = len(self.shape[0]) if self.shape else 1

        if self.x + h_width < 0 or self.y >= self.height or self.y + len(self.shape) < 0:
            self.type_key = random.choice(list(ASTEROID_TYPES.keys()))
            self.data = ASTEROID_TYPES[self.type_key]
            self.name = self.data["name"]
            self.max_hp = self.data["hp"]
            self.hp = self.max_hp
            self.color = self.data["color"]
            self.shape = self.data["shape"]
            self.drops = self.data["drops"]
            self.reset()