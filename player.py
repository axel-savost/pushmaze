from entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.looks_like = "player"
        self.hspeed=0
        self.vspeed=0

    def step(self):
        self.x += self.hspeed
        self.y += self.vspeed

    def stop(self):
        self.hspeed = 0
        self.vspeed = 0