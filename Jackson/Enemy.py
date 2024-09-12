from .Sprite import Sprite
from .Game import settings

class Enemy1(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.enemy1[0], settings.enemy1_masks[0], startx, starty)