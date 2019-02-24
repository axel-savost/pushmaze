class Entity:
  
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.looks_like = ""

    def snap(self,tile):
        self.x = int(round(self.x / float(tile))) * tile
        self.y = int(round(self.y / float(tile))) * tile
        if not self.x % 32 == 0 or not self.y % 32 == 0:
            print("SNAPPED WRONG")

    def stop(self):
        self.hspeed = 0
        self.vspeed = 0

    def step(self):
        self.x += self.hspeed
        self.y += self.vspeed

    def is_moving(self):
        if self.hspeed == 0 and self.vspeed == 0:
            return False
        else:
            return True

    def x_after_step(self):
        return self.x + self.hspeed