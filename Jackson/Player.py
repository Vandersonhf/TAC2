import pygame, numpy
from .Sprite import Sprite
from pygame.locals import *
from .Game import settings
import sys

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.player_stand[0], settings.player_stand_masks[0], startx, starty)
        
        # jump
        self.jump_cycle = settings.player_jump
        self.jump_cycle_masks = settings.player_jump_masks
        self.jump_cycle_flip = settings.player_jump_flip
        self.jump_cycle_flip_masks = settings.player_jump_flip_masks
        
        #stand
        self.stand_cycle = settings.player_stand
        self.stand_cycle_masks = settings.player_stand_masks
        self.stand_cycle_flip = settings.player_stand_flip
        self.stand_cycle_flip_masks = settings.player_stand_flip_masks
        
        #walk       
        self.walk_cycle = settings.player_walk
        self.walk_cycle_masks = settings.player_walk_masks
        self.walk_cycle_flip = settings.player_walk_flip
        self.walk_cycle_flip_masks = settings.player_walk_flip_masks
        
        #attack
        self.atk_cycle = settings.player_atk
        self.atk_cycle_masks = settings.player_atk_masks
        self.atk_cycle_flip = settings.player_atk_flip
        self.atk_cycle_flip_masks = settings.player_atk_flip_masks
                        
        # index for changing image
        self.walk_animation_index = 0
        self.jump_animation_index = 0
        self.stand_animation_index = 0        
        
        # counter for delay
        self.walk_count = 0 
        self.jump_count = 0 
        self.stand_count = 0         
        
        self.facing_left = False
        self.onground = False
        #limits of player movement - change camera
        self.rect_up = pygame.Rect((0,settings.HEIGHT*0.9), (settings.WIDTH,1))
        self.rect_down = pygame.Rect((0,settings.HEIGHT*0.3), (settings.WIDTH,1))
        self.rect_left = pygame.Rect((settings.WIDTH*0.5,0), (1,settings.HEIGHT))
        self.rect_right = pygame.Rect((settings.WIDTH*0.1,0), (1,settings.HEIGHT))

        self.speed = 5
        self.jumpspeed = 14
        self.vsp = 0        # vertical speed
        self.hsp = 0
        self.gravity = 2.8
        self.min_jumpspeed = 3   
        self.walk_delay = 7
        self.stand_delay = 15  
        self.idle = 15
        self.count_idle = 0        
        self.prev_key = pygame.key.get_pressed()
        
        # fire
        self.fire = Fire()
                

    def update(self, boxes, enemies, cenario_rect:pygame.Rect, map_size):
        self.hsp = 0    # horizontal speed               
        self.onground = self.check_collision(0, 1, boxes, "UP")
        
        #gravity
        self.check_gravity()        
        self.check_keys(boxes)
        
        #collide enemy
        self.collide_enemy(enemies)
        self.fire_enemy(enemies) 
        
        # movement - player 
        self.move(self.hsp, self.vsp, boxes) 
        
        #move cenario when off virtual camera limits - check right side
        if self.rect.right > self.rect_left.left and cenario_rect.right > settings.WIDTH: 
            dx = self.rect.right - self.rect_left.left
            self.move(-dx, 0, boxes)             
            cenario_rect.move_ip([-dx, 0])
            if cenario_rect.right < settings.WIDTH:
                cenario_rect.move_ip([dx, 0])
                dx = cenario_rect.right - settings.WIDTH
                cenario_rect.move_ip([-dx, 0])
            for box in boxes:
                box.rect.move_ip([-dx, 0])                
        # check left side
        if self.rect.left < self.rect_right.right and cenario_rect.left < 0:
            dx = self.rect.left - self.rect_right.right
            self.move(-dx, 0, boxes)             
            cenario_rect.move_ip([-dx, 0])
            if cenario_rect.left > 0:   # need to calc the diff between speed and move
                cenario_rect.move_ip([dx, 0])
                dx = cenario_rect.left
                cenario_rect.move_ip([-dx, 0])
            for box in boxes:
                box.rect.move_ip([-dx, 0])  
        # check top side
        if self.rect.top < self.rect_down.bottom and cenario_rect.top < 0:            
            dy = self.rect.top - self.rect_down.bottom
            self.move(0, -dy, boxes)            
            cenario_rect.move_ip([0, -dy])
            if cenario_rect.top > 0:
                cenario_rect.move_ip([0, dy])
                dy = cenario_rect.top
                cenario_rect.move_ip([0, -dy])
            for box in boxes:
                box.rect.move_ip([0, -dy]) 
        # check bottom side - virtual limit + can go down using map?
        if (self.rect.bottom > self.rect_up.top and cenario_rect.bottom > settings.HEIGHT):
            dy = self.rect.bottom - self.rect_up.top                       
            self.move(0, -dy, boxes)
            cenario_rect.move_ip([0, -dy])
            if cenario_rect.bottom < settings.HEIGHT:   # overstep into cenario - fix
                cenario_rect.move_ip([0, dy])                
                dy = cenario_rect.bottom - settings.HEIGHT
                cenario_rect.move_ip([0, -dy])
            for box in boxes:
                box.rect.move_ip([0, -dy])
                        
        #all sides- dont go out of screen
        right = self.rect.right > settings.WIDTH
        left = self.rect.left < 0
        up = self.rect.top < 0
        down = self.rect.bottom > settings.HEIGHT
        if right or left: 
            self.rect.move_ip([-self.hsp, 0])
        if up or down: 
            self.rect.move_ip([0, -self.vsp])        
        return cenario_rect       
            
       
    def check_gravity(self):
        # gravity
        if self.vsp < 20 and not self.onground:  # 9.8 rounded up
            if self.facing_left: 
                self.jump_animation(self.jump_cycle_flip, self.jump_cycle_flip_masks, self.vsp) 
            else:
                self.jump_animation(self.jump_cycle, self.jump_cycle_masks, self.vsp)
            self.walk_count += 1
            if self.walk_count > self.walk_delay:
                self.vsp += self.gravity
                self.walk_count = 0
        if self.onground and self.vsp > 0:
            self.vsp = 0
                         
    
    def collide_enemy(self, enemies:pygame.sprite.Group):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                offset = (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
                collide = self.mask.overlap(enemy.mask, offset) 
                if collide:
                    #push player
                    if self.rect.collidepoint((enemy.rect.left, enemy.rect.centery)):                        
                        self.hsp = -int(self.jumpspeed)
                    else:
                        #stomp
                        if self.rect.collidepoint((enemy.rect.centerx, enemy.rect.top)):                        
                            self.vsp = -int(self.jumpspeed-self.speed)
                            enemy.killed = True
                            settings.play_sound(settings.sound_stomp)
                    
    
    def fire_enemy(self, enemies:pygame.sprite.Group):
        for enemy in enemies:
            if self.fire.rect.colliderect(enemy.rect):
                offset = (enemy.rect.x - self.fire.rect.x, enemy.rect.y - self.fire.rect.y)
                collide = self.fire.mask.overlap(enemy.mask, offset) 
                if collide:
                    enemy.kill()                      


    def check_keys(self, grounds):
        """check keys"""
        key = pygame.key.get_pressed()
        # if user clicks on cross button, close the game 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                        event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit()         
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.count_idle = 0
            if self.onground:
                self.walk_animation(self.walk_cycle_flip, self.walk_cycle_flip_masks, self.walk_delay)
            self.hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.count_idle = 0
            if self.onground:
                self.walk_animation(self.walk_cycle, self.walk_cycle_masks,self.walk_delay)
            self.hsp = self.speed                       
        elif self.vsp == 0 and self.hsp == 0:                                     
            #DANCE!!!
            self.count_idle += 1
            if self.count_idle > self.idle:
                #self.vsp = 0    # dont move on box edges               
                if self.facing_left:
                    self.stand_animation(self.stand_cycle_flip, self.stand_cycle_flip_masks, self.stand_delay)                    
                else:                    
                    self.stand_animation(self.stand_cycle, self.stand_cycle_masks,self.stand_delay)
        
        # fire
        if key[pygame.K_SPACE] and self.onground and self.hsp == 0:            
            self.count_idle = 0           
            if not self.facing_left:
                self.image = self.atk_cycle[0]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = self.atk_cycle_masks[0]
                x = self.rect.right + 30
                y = self.rect.centery
                self.fire.set(x,y)  
                self.fire.fire_animation()              
            else:
                self.image = self.atk_cycle_flip[0]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = self.atk_cycle_flip_masks[0]
                x = self.rect.left - 30
                y = self.rect.centery
                self.fire.set(x,y)        
                self.fire.fire_animation(flip=True)
                     
        #jump
        if key[pygame.K_UP] and self.onground:
            self.count_idle = 0
            self.vsp = -self.jumpspeed
            settings.play_sound(settings.sound_jump)

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        self.prev_key = key

    
    def move(self, x, y, boxes):
        dx = x
        dy = y    
        while self.check_collision(dx, dy, boxes, "LEFT"):
            dx -= 1
        while self.check_collision(dx, dy, boxes, "RIGHT"):
            dx += 1
        while self.check_collision(dx, dy, boxes, "UP"):            
            dy -= 1
        while self.check_collision(dx, dy, boxes, "DOWN"):
            dy += 1
        self.rect.move_ip([dx, dy])
        return dx, dy
                        
    
    def check_collision(self, x, y, grounds, side=None):    
        '''side="UP"|"DOWN"|"LEFT"|"RIGHT"'''
        collide = None
        rect = None        
        self.rect.move_ip([x, y])                       
        for ground in grounds:              
            if self.rect.colliderect(ground):
                if not side: rect = ground.rect
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
         
    
    def walk_animation(self, images:list, masks:list, delay:int):
        '''Enter with surface list and its masks
        plus max delay to change surface
        '''    
        self.walk_animation_index, self.walk_count = self.animation(images,
                masks, delay, self.walk_animation_index, self.walk_count)
          
    
    def stand_animation(self, images:list, masks:list, delay:int):
        '''Enter with surface list and its masks
        plus max delay to change surface 
        '''    
        # for fun
        light = settings.dance[0]
        rect = light.get_rect()
        rect.bottom = self.rect.bottom +30
        rect.centerx = self.rect.centerx
        settings.screen.blit(light, rect)
        #dance 
        self.stand_animation_index, self.stand_count = self.animation(images,
                masks, delay, self.stand_animation_index, self.stand_count)
          
    
    def jump_animation(self, images:list, masks:list, speed:int):
        '''Enter with surface list and its masks
        plus max delay to change surface 
        ''' 
        index = self.jump_animation_index 
                
        if speed > 0: index = 2
        else: index = 0
        
        # change img and mask after delay        
        self.image = images[index]           
        self.rect = self.image.get_rect(center=self.rect.center)        
        self.mask = masks[index]   
        
        self.jump_animation_index = index
        
        
        
class Fire(Sprite):
    """Firing while holding key"""
    def __init__(self, startx=0, starty=0):
        super().__init__(settings.fire[0], settings.fire_masks[0], startx, starty)
        
        self.fire = settings.fire
        self.fire_masks = settings.fire_masks
        self.fire_flip = settings.fire_flip
        self.fire_flip_masks = settings.fire_flip_masks
        
        self.fire_animation_index = 0
        self.fire_count = 0  
        self.fire_delay = 20
        self.fire_sound_counter = 0 
                    
    
    def set(self, x, y):
        self.rect.center = [x, y]  
        
    
    def fire_animation(self, flip=False):
        '''Enter with surface list and its masks
        plus max delay to change surface
        '''
        if flip:
            self.fire_animation_index,self.fire_count = self.animation(self.fire_flip,
                                            self.fire_flip_masks, self.fire_delay,
                                            self.fire_animation_index, self.fire_count)
        else:
            self.fire_animation_index, self.fire_count = self.animation(self.fire,
                                            self.fire_masks, self.fire_delay,
                                            self.fire_animation_index, self.fire_count)
        #play sound - start of cycle        
        if self.fire_sound_counter == 0:
            settings.play_sound(settings.sound_fire)
        self.fire_sound_counter += 1
        if self.fire_sound_counter > self.fire_delay*len(self.fire):
            self.fire_sound_counter = 0 
        #draw
        self.draw(settings.screen)