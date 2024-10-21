from .Sprite import Sprite
from .Game import settings
import pygame

class Enemy1(Sprite):
    def __init__(self, startx=0, starty=0):
        super().__init__(settings.enemy1[0], settings.enemy1_masks[0], startx, starty)
        
        #walk       
        self.walk = settings.enemy1
        self.walk_masks = settings.enemy1_masks
        self.dead = settings.enemy1_dead[0]
        self.dead_mask = settings.enemy1_dead_masks[0]
        
        self.walk_animation_index = 0
        self.walk_count = 0  
        self.walk_delay = 10  
        self.vsp = 0
        self.hsp = 3
        self.gravity = 3
        self.direction_left = 1
        self.direction_down = 1
        self.offsetX = 0
        self.offsetY = 0
        self.killed = False
        self.dead_counter = 0  
        self.dead_delay = 20
        self.rect_init = None
        
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        
        
    def update(self, boxes, cenario_rect):     
        if not self.rect_init:
            self.rect_init = self.rect       
        #reposition of whole cenario items to screen
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left + self.offsetX
            self.rect.top = self.rect_init.top + cenario_rect.top + self.offsetY
                                        
        # check which side hit
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1])) 
        
        # if dead by player?        
        if self.killed:
            self.image = self.dead
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = self.dead_mask            
            self.dead_counter += 1
            if self.dead_counter > self.dead_delay:
                self.dead_counter = 0
                self.kill()
        else:
            # check movement in screen only - see ahead?
            if self.rect.left > -100 and self.rect.left < settings.WIDTH+100 \
                    and self.rect.top > -100 and self.rect.top < settings.HEIGHT+100:
                diffX = self.hsp * self.direction_left
                diffY = self.vsp * self.direction_down                
                X, Y = self.adjust_move(diffX,diffY,boxes)
                self.offsetX -= X 
                self.offsetY += Y 
            
            # animate            
            self.walk_animation_index,self.walk_count = self.animation(self.walk,
                                                self.walk_masks, self.walk_delay,
                                                self.walk_animation_index, self.walk_count)
        
        self.onground = self.check_collision(0, 1, boxes, "UP")
        self.onceil = self.check_collision(0, -1, boxes, "DOWN")
        self.right = self.check_collision(1, 0, boxes, "LEFT")
        self.left = self.check_collision(-1, 0, boxes, "RIGHT")        
        if self.rect.left > 0 and self.rect.left < settings.WIDTH \
                    and self.rect.top > 0 and self.rect.top < settings.HEIGHT:
            self.check_gravity() 
        if self.right: self.direction_left = 1
        if self.left: self.direction_left = -1
         
        self.draw(settings.screen)
    
        
    def adjust_move(self, x, y, boxes):
        dx = x
        dy = y  
        while self.check_collision(dx, dy, boxes, "UP"):            
            dy -= 1
        while self.check_collision(dx, dy, boxes, "DOWN"):
            dy += 1        
        return dx, dy
    
    
    def check_gravity(self):
        # gravity
        if self.vsp < 20 and not self.onground:  # 9.8 rounded up            
            self.walk_count += 1
            if self.walk_count > self.walk_delay:
                self.vsp += self.gravity
                self.walk_count = 0
        if self.onground and self.vsp > 0:
            self.vsp = 0
        if self.onceil:
            self.vsp = self.gravity
                           
    
    def check_collision(self, x, y, grounds, side=None):    
        '''side="UP"|"DOWN"|"LEFT"|"RIGHT"'''
        collide = None
        rect = None        
        self.rect.move_ip([x, y])                       
        for ground in grounds:              
            if self.rect.colliderect(ground.rect):
                #if not side: rect = ground.rect
                if side == "UP": rect = ground.rect_up     
                if side == "DOWN": rect = ground.rect_down
                if side == "LEFT": rect = ground.rect_left
                if side == "RIGHT": rect = ground.rect_right           
                collide = self.collide_mask_rect(self, rect)           
                if collide: break 
        self.rect.move_ip([-x, -y])        
        return collide
    
    
    def collide_mask_rect(self, left, right):
        xoffset = right[0] - left.rect[0]
        yoffset = right[1] - left.rect[1]
        try:
            leftmask = left.mask
        except AttributeError:
            leftmask = pygame.mask.Mask(left.size, True)
        try:
            rightmask = right.mask
        except AttributeError:
            rightmask = pygame.mask.Mask(right.size, True)
        return leftmask.overlap(rightmask, (xoffset, yoffset)) 