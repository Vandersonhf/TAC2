from .Sprite import Sprite
from .Game import settings
import pygame


class FixObj(Sprite):
    def __init__(self, surf, mask=None, startx=0, starty=0):
        super().__init__(surf, mask, startx, starty)
                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self):
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))    
        
          
        
class AniObj(Sprite):
    def __init__(self, surfs, masks, idx, type, depleted=None, startx=0, starty=0):
        super().__init__(surfs[0], masks[0], startx, starty)
        
        self.surfs = surfs
        self.masks = masks
        self.idx = idx
        self.speed = 5
        self.delay = 10
        self.index = 0
        self.counter = 0
        self.type = type
        self.rect_init = None
        self.dead = False
        self.depleted = depleted    # final surface
                                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self, cenario_rect=None):        
        if not self.dead:
            self.index, self.counter = self.animation(self.surfs, self.masks, self.delay,
                                                  self.index, self.counter)
        if not self.rect_init:
            self.rect_init = self.rect
                                
        #reposition of whole cenario items to screen
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left
            self.rect.top = self.rect_init.top + cenario_rect.top
        
        # check which side hit
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1])) 
        
        self.draw(settings.screen)