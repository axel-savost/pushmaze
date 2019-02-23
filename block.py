from entity import Entity

LOWEST_SPEED = 2
INIT_SPEED = 8
CRUSH_TIME = 32

class Block(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x,y)
        self.looks_like = "block"
        self.crushed = 0.0
        self.power = ""


    def update(self):
        if self.is_moving():
            self.step()

        if self.crushed > 0:
            self.crush()
        if self.x < 0 or self.x > 640-32 or self.y <0 or self.y > 480-32:
            self.x -= self.hspeed
            self.y -= self.vspeed
            self.bounce()

    def get_pushed(self,dx,dy):
        self.hspeed = INIT_SPEED * dx
        self.vspeed = INIT_SPEED * dy

    def bounce(self):
            self.hspeed /= -2
            self.vspeed /= -2
            if (self.hspeed < LOWEST_SPEED and self.hspeed > -LOWEST_SPEED) and (self.vspeed < LOWEST_SPEED and self.vspeed > -LOWEST_SPEED):
                self.stop()
                self.snap(32)
                print("Block stopped at (" + str(self.x) + "," + str(self.y) + ")")

    def crush(self):
        self.crushed += 1.0 / CRUSH_TIME