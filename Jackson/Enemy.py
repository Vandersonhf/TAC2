from .Sprite import Sprite
from .Game import settings
from .Player import Player
from .Particles import ParticleRay
import random
import pygame

class Enemy(Sprite):
    def __init__(self, surf, mask, startx=0, starty=0):
        super().__init__(surf, mask, startx, starty)
        
        # general        
        self.gravity = 3
        self.direction_left = 1
        self.direction_down = 1
        self.offsetX = 0
        self.offsetY = 0
        self.killed = False
        
        # check each side collision
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        
        
    def update(self):     
        pass
    
        
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
    


class Mob1(Enemy):
    def __init__(self, startx=0, starty=0):
        super().__init__(settings.enemy1[0], settings.enemy1_masks[0], startx, starty)
        self.ID = 1
        
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
        self.dead_counter = 0  
        self.dead_delay = 20
        self.rect_init = None
        self.fire = False
        self.life = 10
                
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        
        
    def update(self, boxes, cenario_rect, player:Player=None, fire_list = None): 
        # keep init rect
        if not self.rect_init:
            self.rect_init = self.rect       
        #reposition of whole cenario items to screen
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left + self.offsetX - settings.warp_left
            self.rect.top = self.rect_init.top + cenario_rect.top + self.offsetY - settings.warp_top
                
        # if dead by player? or out of scenario        
        if self.life <= 0 or self.rect.bottom > cenario_rect.bottom: self.killed = True      
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
                
                # check which side hit
                self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
                self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
                self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
                self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                            (1,self.rect.bottomleft[1] - self.rect.topleft[1])) 
                
                self.onground = self.check_collision(0, 1, boxes, "UP")
                self.onceil = self.check_collision(0, -1, boxes, "DOWN")
                self.right = self.check_collision(1, 0, boxes, "LEFT")
                self.left = self.check_collision(-1, 0, boxes, "RIGHT")        
                if self.rect.left > 0 and self.rect.left < settings.WIDTH \
                            and self.rect.top > 0 and self.rect.top < settings.HEIGHT:
                    self.check_gravity() 
                if self.right: self.direction_left = 1
                if self.left: self.direction_left = -1
            
            # animate            
            self.walk_animation_index,self.walk_count = self.animation(self.walk,
                                                self.walk_masks, self.walk_delay,
                                                self.walk_animation_index, self.walk_count)            
        
        self.draw(settings.screen)
    
       
class Boss(Enemy):
    def __init__(self, startx=0, starty=0):
        super().__init__(settings.boss[0], settings.boss_masks[0], startx, starty)
        self.ID = 2
        
        #walk       
        self.walk = settings.boss
        self.walk_masks = settings.boss_masks
        self.walk_flip = settings.boss_flip
        self.walk_flip_masks = settings.boss_flip_masks
        
        self.walk_animation_index = 0
        self.walk_count = 0  
        self.walk_delay = 10          
        self.vsp = 0
        self.hsp = -1        
        self.rect_init = None
        self.fire = True
        self.fire_delay = 100
        self.fire_counter = 0
        self.life = 100
        self.max_life = 100
        self.side = "left"
        self.last_rect = None
        self.done_dead = False
        self.dead_counter = 0
        self.dead_delay = 100
        self.particle_group = None
        
        self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
        self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
        self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                     (1,self.rect.bottomleft[1] - self.rect.topleft[1]))
        self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
        
        
    def update(self, boxes, cenario_rect, player:Player=None, fire_list = None): 
        # point of origin
        if not self.rect_init:
            self.rect_init = self.rect              
         
        #reposition of whole cenario items to screen
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left + self.offsetX - settings.warp_left
            self.rect.top = self.rect_init.top + cenario_rect.top + self.offsetY - settings.warp_top
           
        # if dead by player? or out of scenario
        if self.life <= 0 or self.rect.bottom > cenario_rect.bottom: 
            self.life = 100 # reset - once
            settings.play_sound(settings.sound_boss_dead)
            self.killed = True      
        if self.killed:
            # ray - dead
            if self.dead_counter == 30:
                self.particle_group = pygame.sprite.Group()
                pos = (self.rect.center[0], self.rect.center[1])    
                direction = pygame.math.Vector2(0, 0) 
                ParticleRay(self.particle_group, pos, 'white', direction, 0)
            if self.particle_group:
                self.particle_group.draw(settings.screen)
                self.particle_group.update(settings.dt)
            _,self.dead_counter = self.animation([self.image],[self.mask], self.dead_delay,
                                                0, self.dead_counter, -1)
            if self.dead_counter >= self.dead_delay: 
                settings.play_sound(settings.sound_win)
                player.speak("Wohoou!!!")                
                self.kill()         
        else:  
            # check facing side          
            if self.rect.center[0] > player.rect.center[0]: self.side = "left"
            else: self.side = "right"
                 
            # check movement in screen only - see ahead?
            if self.rect.left > -settings.WIDTH and self.rect.left < settings.WIDTH*2 \
                    and self.rect.top > -settings.HEIGHT and self.rect.top < settings.HEIGHT*2: 
                # walk
                diffX = self.hsp 
                diffY = self.vsp                 
                X, Y = self.adjust_move(diffX,diffY,boxes)
                self.offsetX += X 
                self.offsetY += Y 
                
                # check which side hit
                self.rect_up = pygame.Rect(self.rect.topleft, (self.rect.topright[0] - self.rect.topleft[0],1))
                self.rect_down = pygame.Rect(self.rect.bottomleft, (self.rect.bottomright[0] - self.rect.bottomleft[0],1))
                self.rect_right = pygame.Rect(self.rect.topright, (1,self.rect.bottomright[1] - self.rect.topright[1]))
                self.rect_left = pygame.Rect((self.rect.topleft[0], self.rect.topleft[1]),
                                            (1,self.rect.bottomleft[1] - self.rect.topleft[1]))         
                                       
                # shoot create
                self.fire_counter += 1
                if self.fire_counter > self.fire_delay:
                    rand = random.randint(-1,1)     # random low, mid or up fire
                    offset = (self.rect.height/3) * rand
                    rect = pygame.Rect(self.rect_init)                
                    self.vsp = -10         # boss jumping oh yeah         
                    if self.side == "left":                     
                        rect.center = [self.rect_init.midleft[0] + self.offsetX,
                                    self.rect_init.midleft[1] + offset + self.offsetY]
                        fire = Fire(rect)
                        fire.side = 1
                    elif self.side == "right": 
                        rect.center = [self.rect_init.midright[0] + self.offsetX,
                                    self.rect_init.midright[1] + offset + self.offsetY]
                        fire = Fire(rect)
                        fire.side = -1
                    fire_list.add(fire)
                    fire.shoot()
                    self.fire_counter = 0 
                                       
                # draw life bar
                rect = pygame.Rect(self.rect.left, self.rect.top-15, self.rect.width, 13)  
                life_rect = pygame.Rect(self.rect.left+2, self.rect.top-13,
                                        int((self.rect.width*self.life)/self.max_life)-4, 8)      
                pygame.draw.rect(settings.screen, 'gray', rect)
                pygame.draw.rect(settings.screen, 'red', life_rect) 
                              
            # animate     
            if self.side == 'left':       
                self.walk_animation_index,self.walk_count = self.animation(self.walk,
                                                self.walk_masks, self.walk_delay,
                                                self.walk_animation_index, self.walk_count)
                self.hsp = -1
            elif self.side == 'right':
                self.walk_animation_index,self.walk_count = self.animation(self.walk_flip,
                                                self.walk_flip_masks, self.walk_delay,
                                                self.walk_animation_index, self.walk_count)
                self.hsp = 1  
            
            #check if is close enough
            if abs(self.rect.center[0] - player.rect.center[0]) < 50: self.hsp = 0  
            self.onground = self.check_collision(0, 1, boxes, "UP")
            self.onceil = self.check_collision(0, -1, boxes, "DOWN")  
            self.check_gravity()             
        
        self.draw(settings.screen)
        
        
class Fire(Enemy):    
    def __init__(self, rect, startx=0, starty=0):
        super().__init__(settings.boss_fire[0], settings.boss_fire_masks[0], startx, starty)
        self.ID = 3
        
        self.fire = settings.boss_fire
        self.fire_masks = settings.boss_fire_masks
        self.fire_flip = settings.boss_fire_flip
        self.fire_flip_masks = settings.boss_fire_flip_masks
        
        self.fire_animation_index = 0
        self.fire_count = 0  
        self.fire_delay = 20
        self.rect_init = rect       
        self.hsp = 7        
        self.side = 1
        self.life = 10
   
   
    def shoot(self):
        settings.sound_boss_fire.play()
        
           
    def update(self, cenario_rect, boxes, items): 
        # alive?
        if self.life <= 0: self.kill()
        
        # hit items
        for item in items:
            if item.idx == 3 and item.type == 1:
                pass    # not coin
            else:            
                if self.rect.colliderect(item.rect):
                    self.kill()
        # hit box
        for box in boxes:            
            if self.rect.colliderect(box.rect):
                self.kill()
        
        # gogogo
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left + self.offsetX 
            self.rect.top = self.rect_init.top + cenario_rect.top 
        
        # fly
        diffX = self.hsp * self.side 
        self.offsetX -= diffX
                       
        self.draw(settings.screen)
        
        # clear
        if self.rect.right < -settings.WIDTH or self.rect.left > settings.WIDTH*2: self.kill() 
        
        # animate            
        self.fire_animation_index,self.fire_count = self.animation(self.fire,
                                            self.fire_masks, self.fire_delay,
                                            self.fire_animation_index, self.fire_count)