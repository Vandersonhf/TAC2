from .Sprite import Sprite
from .Game import settings
import pygame

class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.box, settings.box_mask, startx, starty)
                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self):
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        #self.rect_left = pygame.Rect(self.rect.topleft, (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
    
    
class Floor1(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.floor1[0], settings.floor1_mask[0], startx, starty)
                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self):
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        #self.rect_left = pygame.Rect(self.rect.topleft, (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
    