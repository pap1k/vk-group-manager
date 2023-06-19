from orm import Entity, Types

class Moder(Entity):
    vkid : int = 0
    def __init__(self):
        print("Init moder")

m = Moder()