from .Sprite import Sprite
from .Game import settings

class Enemy1(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.enemy1[0], settings.enemy1_masks[0], startx, starty)
        
        #walk       
        self.walk = settings.enemy1
        self.walk_masks = settings.enemy1_masks
        self.dead = self.walk.pop()
        self.dead_mask = self.walk_masks.pop()
        
        self.walk_animation_index = 0
        self.walk_count = 0  
        self.walk_delay = 10        
        self.speed = 3
        self.killed = False
        self.dead_counter = 0  
        self.dead_delay = 20
        
        
    def update(self):            
        if self.killed:
            self.image = self.dead
            self.rect = self.image.get_rect(center=self.rect.center)
            self.mask = self.dead_mask            
            self.dead_counter += 1
            if self.dead_counter > self.dead_delay:
                self.dead_counter = 0
                self.kill()
        else:
            #move
            self.rect.move_ip([-self.speed,0])
            
            # animate
            self.walk_animation_index,self.walk_count = self.animation(self.walk,
                                                self.walk_masks, self.walk_delay,
                                                self.walk_animation_index, self.walk_count)
            
        
        # more to come... gravity, wall colision, etc.