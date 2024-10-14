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
        self.speed = 3
        self.offsetX = 0
        self.killed = False
        self.dead_counter = 0  
        self.dead_delay = 20
        self.rect_init = None
        
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        
        
    def update(self, cenario_rect):     
        if not self.rect_init:
            self.rect_init = self.rect       
        #reposition of whole cenario items to screen
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left + self.offsetX
            self.rect.top = self.rect_init.top + cenario_rect.top
                            
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
            #move  #self.rect.move_ip([-self.speed,0])
            self.offsetX -= self.speed
            
            # animate            
            self.walk_animation_index,self.walk_count = self.animation(self.walk,
                                                self.walk_masks, self.walk_delay,
                                                self.walk_animation_index, self.walk_count)
            
        self.draw(settings.screen)
        # more to come... gravity, wall colision, etc.