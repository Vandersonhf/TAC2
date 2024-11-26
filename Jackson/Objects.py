from .Sprite import Sprite
from .Game import settings
import pygame, random


class FirePit():
    def __init__(self, pos:list[int], size:int):        
        self.particles = []
        self.pos = pos
        self.size = size
        self.rect_init = None
        self.count = 0
        self.delay = 2
    
    def update(self, cenario_rect=None): 
        self.count += 1
        x = self.pos[0] + cenario_rect.left
        y = self.pos[1] + cenario_rect.top
        #if self.count >= self.delay:                       
            # check movement in screen only - see ahead?
        if x > -100 and x < settings.WIDTH+100 \
                and y > -100 and y < settings.HEIGHT+100:
            self.particles.append([[random.randint(x, x+self.size), y],  # pos
                                    [random.randint(0,20)/10-1, -4],    # vel
                                    random.randint(8,12)])            # size
            #self.count = 0
        color = random.choice(("red", "yellow", "orange"))
        for p in self.particles:
            p[0][0] += p[1][0]   # vel 
            p[0][1] += p[1][1] 
            p[2] -= 0.4
            dx = int(p[0][0])
            dy = int(p[0][1]) + settings.tile
            pygame.draw.circle(settings.screen, color, [dx, dy], int(p[2]))
            
            # light
            radius = p[2] * 2
            settings.screen.blit(self.circle_surf(radius, (150,20,20)), 
                                    (dx-radius, dy-radius), special_flags=pygame.BLEND_RGB_ADD)
            
            if p[2] <= 0:
                self.particles.remove(p)
    
    
    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        surf.set_colorkey((0,0,0))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        return surf
        
        

class FixObj(Sprite):
    def __init__(self, surf, mask=None, startx=0, starty=0):
        super().__init__(surf, mask, startx, starty)
                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))

    def update(self):
        # if in screen update
        #if settings.screen.get_rect().colliderect(self.rect):        
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                    (1,self.rect.bottomleft[1] - self.rect.topleft[1]))    
        
          
        
class AniObj(Sprite):
    def __init__(self, surfs, masks, idx, type, depleted=None, startx=0, starty=0):
        super().__init__(surfs[0], masks[0], startx, starty)
        
        self.id = settings.item_id
        settings.item_id += 1
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
        self.star = False
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
            self.rect.left = self.rect_init.left + cenario_rect.left - settings.warp_left
            self.rect.top = self.rect_init.top + cenario_rect.top - settings.warp_top
        
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
            if self.star: settings.screen.blit(settings.star[i], rect)
            else: settings.screen.blit(settings.coin_box[i], rect)  
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
        