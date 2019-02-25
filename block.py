from entity import Entity
import constants


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
        if self.x < 0 or self.x > constants.WINDOW_WIDTH-32 or self.y <0 or self.y > constants.WINDOW_HEIGHT-32:
            self.x -= self.hspeed
            self.y -= self.vspeed
            self.bounce()

    def get_pushed(self,dx,dy):
        self.hspeed = constants.INIT_BLOCK_SPEED * dx
        self.vspeed = constants.INIT_BLOCK_SPEED * dy

    def bounce(self):
            self.hspeed /= -2
            self.vspeed /= -2
            s = constants.LOWEST_BLOCK_SPEED
            
            if (self.hspeed < s and self.hspeed > -s) and (self.vspeed < s and self.vspeed > -s):
                self.stop()
                self.snap(32)
                print("Block stopped at (" + str(self.x) + "," + str(self.y) + ")")

    def crush(self):
        self.crushed += 1.0 / constants.CRUSH_TIME

    def collide_with(self,block):
        if not self.is_moving:
            return

        if not block.is_moving():
            self.bounce()
        else:
            #Swap speed
            temph = block.hspeed
            tempv = block.vspeed
            block.hspeed = self.hspeed
            block.vspeed = self.vspeed
            self.hspeed = temph
            self.vspeed = tempv
