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
        self.speed = 9        
        self.delay = 10
        self.index = 0
        self.counter = 0
        self.type = type
        self.rect_init = None
        self.dead = False        
        self.dead_brick = False
        self.dead_box = False
        self.depleted = depleted    # final surfaces
        self.pos = None
                               
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self, cenario_rect=None):
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
        
        if not self.dead:
            self.pos = [[-10,-10],[10,-10],[-10,-5],[10,-5]]     # RESET POS
            self.index, self.counter = self.animation(self.surfs, self.masks, self.delay,
                                                  self.index, self.counter)
        elif self.dead_brick: self.pos = self.dead_bricks_animation(self.pos)
        elif self.dead_box: self.dead_box_animation()
        
        if not self.dead_brick:            
            self.draw(settings.screen)
        
    
    def dead_box_animation(self): 
        self.counter += 1
        if self.counter < self.delay*4:
            l = self.rect.left
            t = self.rect.top-(settings.base_tile*settings.factor_tile)
            w = self.rect.width
            h = self.rect.height
            rect = pygame.Rect(l,t,w,h)
            # coin animation
            i = self.counter // self.delay  
            rect.top -= self.counter
            settings.screen.blit(settings.coin_box[i], rect)
        else: self.dead_box = False
        
    
    def dead_bricks_animation(self, pos):        
        index = 1   # image
        debris = 4  # id        
        flag = 0        
        for d in range(debris):
            if d % 2 == 0:              # left
                index = 2
                pos[d][0] -= 3         # the high it gets the small it becomes?                
            else:                       # right
                index = 1 
                pos[d][0] += 3          # function? log? square? plot? x=1->y=10, x=10->y=1 division 1/x?                
            if d < debris//2: pos[d][1] -= self.speed*2
            else: pos[d][1] -= self.speed
            image = self.depleted[index]   
            offsetX = self.rect.center[0] + pos[d][0] #+ 100//pos[d][0]
            offsetY = self.rect.center[1] + pos[d][1] 
            rect = self.image.get_rect(center=(offsetX, offsetY))
            if offsetX<0 or offsetX>settings.WIDTH or offsetY<0 or offsetY> settings.HEIGHT:
                flag += 1
            if flag<debris: settings.screen.blit(image, rect)
            else:                
                self.kill()        
        self.speed -= 0.3       # reduce here inverting signal
        return pos
        