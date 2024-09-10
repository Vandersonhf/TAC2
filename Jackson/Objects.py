from .Sprite import Sprite

class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("Jackson/images/box.jpg", startx, starty)
