from entity import Entity

class Player(Entity):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.looks_like = "ghost"