from entity import Entity

LOWEST_SPEED = 2
INIT_SPEED = 8

class Block(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x,y)
        self.looks_like = "block"
        self.hspeed = 0
        self.vspeed = 0
        self.crushed = False

    def is_moving(self):
        if self.hspeed == 0 and self.vspeed == 0:
            return False
        else:
            return True

    def stop(self):
        self.hspeed = 0
        self.vspeed = 0
        self.x = round(self.x)
        self.y = round(self.y)


    def update(self):
        self.x += self.hspeed
        self.y += self.vspeed

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