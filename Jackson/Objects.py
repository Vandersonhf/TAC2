from .Sprite import Sprite
from .Game import settings

class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.box, settings.box_mask, startx, starty)
