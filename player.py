from entity import Entity

class Player(Entity):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.looks_like = "player"