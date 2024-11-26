import pygame
from .Sprite import Sprite
from pygame.locals import *
from .Game import settings
from .SQL import sql_request, sql_update
from .Particles import ParticleSpark
import random, math, sys

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
        self.rect_right = pygame.Rect((settings.WIDTH*0.3,0), (1,settings.HEIGHT))

        self.speed = 5
        self.jumpspeed = 14
        self.vsp = 0        # vertical speed
        self.hsp = 0
        self.gravity = 4
        self.min_jumpspeed = 3   
        self.walk_delay = 12
        self.stand_delay = 12  
        self.idle = 20
        self.count_idle = 0        
        self.prev_key = pygame.key.get_pressed()
        self.orbs = pygame.sprite.Group() 
        self.orb_counter = 0
        self.orb_delay = 40
        
        #score
        self.score = 0
        self.life = 100
        self.max_life = 100
        self.hit = False
        self.hit_counter = 0
        self.hit_delay = 50
        self.text_count = 0
        self.message = ""
        
        # speak
        self.speak_delay = 100
        self.speak_count = 0
        
        # player count
        if settings.multiplayer and settings.server:
            self.nb = Number(self.rect.centerx, self.rect.top - 40, 50,50, '1')
        if settings.multiplayer and settings.client:   
            self.nb = Number(self.rect.centerx, self.rect.top - 40, 50,50, '2')
            

    def update(self, boxes, enemies, cenario_rect:pygame.Rect, items):               
        #old_pos = cenario_rect
        self.hsp = 0    # horizontal speed               
        self.onground = self.check_collision(0, 1, boxes, "UP")
        self.onceil = self.check_collision(0, -1, boxes, "DOWN")
        
        #gravity and keys
        self.check_gravity()   
        # check movement - initial and orbs 
        left = self.rect.left-cenario_rect.left 
        top = self.rect.top-cenario_rect.top+20 
        ini_pos = [left, top]
        cenario_rect = self.check_keys(pygame.Rect(ini_pos,(self.rect.width, self.rect.height)), cenario_rect)
        self.orbs.update(cenario_rect)
        
        #collide enemy, items, etc
        dead = self.collide_enemy(enemies)
        if self.rect.bottom + self.vsp > cenario_rect.bottom: dead = True
        if dead: 
            self.draw(settings.screen)
            return False
        self.fire_enemy(enemies, boxes, items) 
        box = self.collide_item(items)
        if len(box) > 0: boxes.add(box)
        
        # movement - player 
        self.adjust_move(self.hsp, self.vsp, boxes)
        cenario_rect = self.check_virtual_hard_limits(cenario_rect, boxes)
        self.draw(settings.screen)
        
        # speak update
        if self.speak_count != 0:
            self.speak_count += 1
            if self.speak_count < self.speak_delay:
                self.sp.update(self.rect.right, self.rect.top)
            else: self.speak_count = 0
        
        # multiplayer
        if settings.multiplayer:
            self.nb.update(self.rect.centerx, self.rect.top - 40)              
        
        return cenario_rect
    
    
    def speak(self, text):
        self.sp = Speak(self.rect.left, self.rect.bottom, 100,60,text)
        self.speak_count += 1
    
    
    def collide_item(self, items):
        box = []
        for item in items:
            if abs(self.rect.top - item.rect.top) < 100:
                # BRICK
                if item.idx == 0 and item.type == 1:
                    if not item.dead:
                        if self.rect.colliderect(item.rect):
                            box.append(item)
                        self.rect.move_ip([self.hsp, self.vsp])
                        if item.rect.collidepoint((self.rect.centerx, self.rect.top)) and self.vsp < 0:
                        #if self.rect.collidepoint((item.rect.centerx, item.rect.bottom)) and self.vsp < 0:
                            settings.sound_break.play()
                            item.image = item.depleted[0]
                            item.dead = True
                            item.dead_brick = True
                            self.vsp = 0
                            try: 
                                box.index(item)
                                box.remove(item)
                            except ValueError: pass
                        self.rect.move_ip([-self.hsp, -self.vsp])
                # BOX                     
                if item.idx == 3 and item.type == 0:
                    self.rect.move_ip([self.hsp, self.vsp])
                    if self.rect.colliderect(item.rect):
                        box.append(item)   
                    if not item.dead:            
                        if self.rect.collidepoint((item.rect.centerx, item.rect.bottom)) and self.vsp < 0:
                            settings.sound_bump.play()
                            item.image = item.depleted[0]
                            item.dead = True 
                            self.vsp = 0 
                            # check prize
                            select = 1
                            if self.life < self.max_life:
                               select = random.randint(1,2)
                            if select == 1: 
                                # appear prize - coin
                                settings.sound_coin.play()
                                self.score += 1
                                item.dead_box = True
                                if settings.multiplayer and settings.client_connected:
                                    message = f'{self.score}' 
                                    self.create_message('score'+settings.sep, message)
                            elif select == 2: 
                                # appear prize - star
                                settings.sound_life.play()
                                self.life += 10
                                item.star = True
                                item.dead_box = True
                                if settings.multiplayer and settings.client_connected:
                                    message = f'{self.life}' 
                                    self.create_message('life'+settings.sep, message)
                    self.rect.move_ip([-self.hsp, -self.vsp])                  
                # COIN
                if item.idx == 3 and item.type == 1:
                    if self.rect.colliderect(item.rect):
                        settings.sound_coin.play()
                        self.score += 1
                        item.kill()
                        if settings.multiplayer and settings.client:
                            message = f'{self.score}' 
                            self.create_message('score'+settings.sep, message)
        return box
    
    
    def check_virtual_hard_limits(self, cenario_rect, boxes):
        top = cenario_rect.top
        left = cenario_rect.left    
        #move cenario when off virtual camera limits - check right side
        if self.rect.right > self.rect_left.left and cenario_rect.right > settings.WIDTH: 
            dx = self.rect.right - self.rect_left.left
            self.adjust_move(-dx, 0, boxes)             
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
            self.adjust_move(-dx, 0, boxes)             
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
            self.adjust_move(0, -dy, boxes)            
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
            self.adjust_move(0, -dy, boxes)
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
        if self.onceil:
            self.vsp = self.gravity
                         
    
    def collide_enemy(self, enemies:pygame.sprite.Group):
        # hit animation
        if self.hit:
            self.hit_counter += 1
            if self.hit_counter < self.hit_delay//2: self.image = settings.dead[2]
            else: self.image = settings.dead[1]
            self.rect = self.image.get_rect(center=self.rect.center)
            if self.hit_counter > self.hit_delay:
                self.hit = False
        else:   # check enemy collision   
            for enemy in enemies:
                if not enemy.killed and abs(self.rect.top - enemy.rect.top) < 100:
                    if self.rect.colliderect(enemy.rect):
                        offset = (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
                        collide = self.mask.overlap(enemy.mask, offset) 
                        if collide and not self.hit:
                            #hit player                        
                            if self.rect.collidepoint((enemy.rect.left, enemy.rect.centery)) or \
                                self.rect.collidepoint((enemy.rect.right, enemy.rect.centery)):                        
                                #self.hsp = -int(self.jumpspeed)    # kick
                                self.life -= 10 
                                if self.life <=0:
                                    self.life = 0
                                    self.image = settings.dead[0]
                                    self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
                                    settings.sound_dead.play()
                                    return True
                                else:
                                    settings.sound_hit.play()                                
                                    self.hit = True
                                    self.hit_counter = 0
                                if settings.multiplayer and settings.client_connected:
                                    message = f'{self.life}' 
                                    self.create_message('life|', message)
                            else:
                                #stomp kill
                                if not self.hit and enemy.ID == 1:
                                    if self.rect.collidepoint((enemy.rect.centerx, enemy.rect.top)):                        
                                        self.vsp = -int(self.jumpspeed-self.speed)
                                        enemy.killed = True
                                        settings.play_sound(settings.sound_stomp)
                    
    
    def fire_enemy(self, enemies:pygame.sprite.Group, boxes, items):
        # hit items
        for item in items:            
            for orb in self.orbs:
                if abs(orb.rect.top - item.rect.top) < 100:
                    if item.idx == 3 and item.type == 1:    # not coin
                        pass
                    else:
                        if orb.rect.colliderect(item.rect):
                            orb.kill()
        # hit box
        for box in boxes:
            for orb in self.orbs:
                if abs(orb.rect.top - box.rect.top) < 100:
                    if orb.rect.colliderect(box.rect):
                        orb.kill()
        # hit enemy
        for enemy in enemies:
            for orb in self.orbs:
                if not enemy.killed and abs(orb.rect.top - enemy.rect.top) < 100:
                    if orb.rect.colliderect(enemy.rect):
                        offset = (enemy.rect.x - orb.rect.x, enemy.rect.y - orb.rect.y)
                        collide = orb.mask.overlap(enemy.mask, offset) 
                        if collide:
                            orb.kill()
                            enemy.life -= 20
        
        
    def check_keys(self, ini_rect, cenario_rect):
        """check keys"""
        key = pygame.key.get_pressed()
        # if user clicks on cross button, close the game 
        for event in pygame.event.get():
            # handle one press
            if event.type == QUIT or (event.type == KEYDOWN and
                                        event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit()  
            # pause/start music  
            if (event.type == KEYDOWN and event.key == K_m):
                if settings.somAtivado: 
                    pygame.mixer.music.stop()
                    settings.somAtivado = False
                else: 
                    pygame.mixer.music.play(-1, 0.0)
                    pygame.mixer.music.set_volume(0.2)
                    settings.somAtivado = True  
            #change side - even when down
            if (event.type == KEYDOWN and event.key == K_LEFT):
                self.facing_left = True
                self.count_idle = 0  
                if settings.multiplayer and settings.client:
                    message = '' 
                    self.create_message('face_left'+settings.sep, message)
            if (event.type == KEYDOWN and event.key == K_RIGHT):
                self.facing_left = False
                self.count_idle = 0    
                if settings.multiplayer and settings.client:
                    message = '' 
                    self.create_message('face_right'+settings.sep, message)                         
            # shoot orb
            if (event.type == KEYDOWN and event.key == K_SPACE): 
                self.count_idle = 0 
                if self.orb_counter > self.orb_delay:
                    self.orb_counter = 0               
                #play sound - start of cycle        
                if self.orb_counter == 0:                    
                    fire = FireOrb(ini_rect)
                    if self.facing_left: 
                        self.image = self.atk_cycle_flip[0]
                        self.rect = self.image.get_rect(center=self.rect.center)
                        self.mask = self.atk_cycle_flip_masks[0]                        
                        fire.direction_left = 1
                    else: 
                        self.image = self.atk_cycle[0]
                        self.rect = self.image.get_rect(center=self.rect.center)
                        self.mask = self.atk_cycle_masks[0]
                        fire.direction_left = -1                   
                    self.orbs.add(fire)
                    settings.play_sound(settings.sound_fire)
                    # socket message
                    if settings.multiplayer and settings.client_connected:
                        message = '' 
                        self.create_message('shoot'+settings.sep, message)
            # save game
            if (event.type == KEYDOWN and event.key == K_F5): 
                    sql_update(self.score, self.life)
                    self.text_count = 1     # check count outside for loop
                    self.message = "Game Saved!!!"
                    '''save = f"{self.score},{self.life}"
                    self.text_count += 1
                    with open("save.txt", "w") as arq:                        
                        arq.write(save)''' 
            # load game
            if (event.type == KEYDOWN and event.key == K_F6):
                    dados = sql_request() 
                    self.score = dados[0]
                    self.life = dados[1]
                    self.text_count = 1
                    self.message = "Game Load success!"
                    '''with open("save.txt", "r") as arq:
                        dados = arq.read()
                        val = dados.split(",")
                        self.score = int(val[0])
                        self.life = int(val[1])'''        
        # update fire counter            
        if self.orb_counter <= self.orb_delay: self.orb_counter += 1                                                   
        #get down - handle press hold
        if key[pygame.K_DOWN] and self.onground:
            self.count_idle = 0
            self.hsp = 0
            if self.facing_left: self.image = settings.dead_flip[1]
            else: self.image = settings.dead[1]
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            if settings.multiplayer and settings.client:
                    message = '' 
                    self.create_message('down'+settings.sep, message) 
        elif key[pygame.K_LEFT]:
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
            if self.count_idle == 0: 
                settings.particle_group.empty()
            self.count_idle += 1
            if self.count_idle > self.idle:                
                self.vsp = 0    # dont move on box edges               
                if self.facing_left:
                    self.stand_animation(self.stand_cycle_flip, self.stand_cycle_flip_masks, self.stand_delay)                    
                else:                    
                    self.stand_animation(self.stand_cycle, self.stand_cycle_masks,self.stand_delay)
            # shine  
            if self.count_idle % 20 == 0: 
                pos = (self.rect.center[0] + random.randint(0,100), self.rect.center[1] + random.randint(-100,100))    
                #direction = pygame.math.Vector2(random.uniform(0,0), random.uniform(-1,0))  
                #direction = direction.normalize()
                direction = pygame.math.Vector2(-5,0)    
                ParticleSpark(settings.particle_group, pos, 'white', direction, 15)
            settings.particle_group.draw(settings.screen)
            settings.particle_group.update(settings.dt)
                             
        #jump
        if key[pygame.K_UP] and self.onground:
            self.count_idle = 0
            self.vsp = -self.jumpspeed
            settings.play_sound(settings.sound_jump)
            
        #run
        if key[pygame.K_LCTRL] and self.onground:
            self.count_idle = 0
            self.hsp = self.hsp * 1.5
                                
        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed            
        self.prev_key = key
        
        # texto save game - avoid running too many times inside event for loop
        if self.text_count > 0:
            self.blit_text(f'{self.message}', settings.fonte, settings.screen, 
                              settings.WIDTH/2, settings.HEIGHT*0.2,
                                100, 'center')
        
        # socket message - move
        if settings.multiplayer and settings.client_connected:
            if self.vsp != 0 or self.hsp != 0:
                message = str(self.rect.center[0])+settings.sep+str(self.rect.center[1])+settings.sep+\
                            str(cenario_rect.left)+settings.sep+str(cenario_rect.top)
                self.create_message('move'+settings.sep, message)
                  
        return cenario_rect
    
    def create_message(self, code, message):
        # socket messages
        if settings.multiplayer:
            if settings.client:                  
                m = code+message+settings.sep
                while len(m) < settings.size:
                    m += '*'              
                #print("Enviando mensagem ",m)
                settings.client_socket.send_message(m)
            if settings.server:
                m = code+message+settings.sep
                while len(m) < settings.size:
                    m += '*'              
                #print("Enviando mensagem ",m)
                settings.server_socket.send_message(m)
    

    def blit_text(self, texto, fonte, janela, x, y, delay=0, pos='topleft'):
        if delay > 0:             
            if self.text_count <= delay:
                self.text_count += 1           
                self.render_text(texto, fonte, janela, x, y, pos)     
            else:
                self.text_count = 0
        else: self.render_text(texto, fonte, janela, x, y, pos)


    def render_text(self, texto, fonte, janela, x, y, pos='topleft'):
        objTexto = fonte.render(texto, True, settings.CORTEXTO)
        rectTexto:pygame.Rect = objTexto.get_rect()
        if pos == 'topleft': rectTexto.topleft = (x, y)
        if pos == 'center': rectTexto.center = (x, y)
        janela.blit(objTexto, rectTexto)
        
            
    def adjust_move(self, x, y, boxes):
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
        rect.bottom = self.rect.bottom + 30
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
        else: index = 1
        
        # change img and mask after delay        
        self.image = images[index]           
        self.rect = self.image.get_rect(center=self.rect.center)        
        self.mask = masks[index]   
        
        self.jump_animation_index = index
       
  

class FireOrb(Sprite):
    """Firing while holding key"""
    def __init__(self, rect, startx=0, starty=0):
        super().__init__(settings.orb[0], settings.orb_masks[0], startx, starty)
        
        self.orb = settings.orb
        self.orb_masks = settings.orb_masks
                
        self.orb_animation_index = 0
        self.orb_count = 0  
        self.orb_delay = 2       
        self.rect_init = rect
        self.offsetX = 0
        self.offsetY = 0
        self.direction_left = 1 
        self.hsp = 10
                    
    
    def update(self, cenario_rect):               
        #reposition of whole cenario items to screen
        if cenario_rect:
            self.rect.left = self.rect_init.left + cenario_rect.left + self.offsetX 
            self.rect.top = self.rect_init.top + cenario_rect.top
        self.offsetX -= self.hsp * self.direction_left        
        self.fire_animation()
                
                
    def fire_animation(self):
        '''Enter with surface list and its masks
        plus max delay to change surface
        '''        
        self.orb_animation_index, self.orb_count = self.animation(self.orb,
                                            self.orb_masks, self.orb_delay,
                                            self.orb_animation_index, self.orb_count)
               
        #draw
        self.draw(settings.screen)
        
        
        
class Speak(): 
    def __init__(self, x, y, w, h, text='', font=24, color=(0,0,0)):        
        self.w = w
        self.h = h
        
        # Create a surface 
        self.surf = pygame.Surface((w, h))
        self.surf.set_colorkey((0,0,0))
        
        # Create a font object
        font = pygame.font.Font(None, font)
        
        # Render text
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect(center=(self.surf.get_width()/2,
                                                    self.surf.get_height()/2-10))

        # Create a pygame.Rect object 
        self.rect = pygame.Rect(x, y, w, h)  # Adjust the position as needed
        
        
    def update(self, x, y):
        self.rect.bottomleft = (x,y)
        # draw text balloon
        pygame.draw.rect(self.surf, "white", (0, 0, self.w, self.h-10), border_radius=10)                
        pygame.draw.polygon(self.surf, "white", [(10,self.h-10),(5,self.h),(15,self.h-10),(10,self.h-10)]) 
        
        # Show the text
        self.surf.blit(self.text, self.text_rect)
        
        # Draw on the screen
        settings.screen.blit(self.surf, (self.rect.x, self.rect.y))
        


class Number(): 
    def __init__(self, x, y, w, h, text='', font=24, color=(255,255,255)):        
        self.w = w
        self.h = h
        
        # Create a surface 
        self.surf = pygame.Surface((w, h))
        self.surf.set_colorkey((0,0,0))
        
        # Create a font object
        font = pygame.font.Font(None, font)
        
        # Render text
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect(center=(self.surf.get_width()/2,
                                                    self.surf.get_height()/2))

        # Create a pygame.Rect object 
        self.rect = pygame.Rect(x, y, w, h)  # Adjust the position as needed
        
        
    def update(self, x, y):
        self.rect.midtop = (x,y)
        # draw text balloon
        #pygame.draw.rect(self.surf, "white", (0, 0, self.w, self.h-10), border_radius=10)                
        #pygame.draw.polygon(self.surf, "white", [(10,self.h-10),(5,self.h),(15,self.h-10),(10,self.h-10)]) 
        
        # Show the text
        self.surf.blit(self.text, self.text_rect)
        
        # Draw on the screen
        settings.screen.blit(self.surf, (self.rect.x, self.rect.y))
                
        
        
class Player2(Player):
    def __init__(self, startx, starty):
        super().__init__(startx, starty)
        
        self.old_cenario = None
            
        # player count
        if settings.multiplayer and settings.server:
            self.nb = Number(self.rect.centerx, self.rect.top - 40, 50,50, '2')
        if settings.multiplayer and settings.client:   
            self.nb = Number(self.rect.centerx, self.rect.top - 40, 50,50, '1')
       

    def update(self, boxes, enemies, cenario_rect:pygame.Rect, items):
        dtop = 0
        dleft = 0
        # correction position
        if self.old_cenario:
            if self.old_cenario[0] != cenario_rect.top or \
                self.old_cenario[1] != cenario_rect.left:
                    dtop = self.old_cenario[0] - cenario_rect.top
                    dleft = self.old_cenario[1] - cenario_rect.left
                    self.rect.top -= dtop
                    self.rect.left -= dleft
        self.old_cenario = (cenario_rect.top, cenario_rect.left)
        
        self.hsp = 0    # horizontal speed               
        self.onground = self.check_collision(0, 1, boxes, "UP")
        self.onceil = self.check_collision(0, -1, boxes, "DOWN")
        
        #gravity and keys
        self.check_gravity()   
        # check movement - initial and orbs 
        left = self.rect.left-cenario_rect.left + settings.warp_left
        top = self.rect.top-cenario_rect.top+20 + settings.warp_top
        ini_pos = [left, top]        
        self.check_p2(pygame.Rect(ini_pos,(self.rect.width, self.rect.height)))
        self.orbs.update(cenario_rect)
        
        #collide enemy, items, etc
        #dead = self.collide_enemy(enemies)
        #if self.rect.bottom + self.vsp > cenario_rect.bottom: dead = True
        #if dead: 
        #    self.draw(settings.screen)
        #    return False
        #self.fire_enemy(enemies, boxes, items) 
        #box = self.collide_item(items)
        #if len(box) > 0: boxes.add(box)
        
        # movement - player 
        self.adjust_move(self.hsp, self.vsp, boxes)
        
        
        # read message buffer
        if len(settings.buffer_in)>0:
            message:str = settings.buffer_in.pop(0)
            #print(message)
            message_list = message.split(settings.sep)
            # code 001 - move       
            old_center = (self.rect.center[0], self.rect.center[1])                   
            if message_list[0] == 'move':
                self.count_idle = 0
                #print(message, message_list)
                #print("p2 ", cenario_rect, self.rect.center)
                p2x = int(message_list[1])
                p2y = int(message_list[2])
                cenario_left = int(message_list[3])
                cenario_top = int(message_list[4])
                # diff between cenario rects
                dx = cenario_rect.left - cenario_left
                dy = cenario_rect.top - cenario_top                
                self.rect.center = (p2x + dx, p2y + dy)
                # right
                if self.rect.center[0] > old_center[0]:
                    settings.event_p2.append('right')
                # left
                if self.rect.center[0] < old_center[0]:
                    settings.event_p2.append('left')
                # fix jump animation
                if self.rect.center[1] < old_center[1]:
                    self.vsp = 0
            # code 002 - shoot
            if message_list[0] == 'shoot':
                settings.event_p2.append('shoot')
            if message_list[0] == 'face_left':
                settings.event_p2.append('face_left')
            if message_list[0] == 'face_right':
                settings.event_p2.append('face_right')             
            if message_list[0] == 'down':
                settings.event_p2.append('down')   
            if message_list[0] == 'life':
                self.life = int(message_list[1])
            if message_list[0] == 'score':
                self.score = int(message_list[1])
                      
        
        # multiplayer
        self.nb.update(self.rect.centerx, self.rect.top - 40)
          
        self.draw(settings.screen)
     
    
    def check_p2(self, ini_rect):
        """check player 2 message events"""        
        #for event in pygame.event.get():
        for event in settings.event_p2: 
            #change side - even when down
            if (event == "face_left"):
                self.facing_left = True
                self.count_idle = 0  
            if (event == "face_right"):
                self.facing_left = False
                self.count_idle = 0                     
            # shoot orb
            if (event == "shoot"):
                #print("SHOOT")
                self.count_idle = 0                                   
                fire = FireOrb(ini_rect)
                if self.facing_left: 
                    self.image = self.atk_cycle_flip[0]
                    self.rect = self.image.get_rect(center=self.rect.center)
                    self.mask = self.atk_cycle_flip_masks[0]                        
                    fire.direction_left = 1
                else: 
                    self.image = self.atk_cycle[0]
                    self.rect = self.image.get_rect(center=self.rect.center)
                    self.mask = self.atk_cycle_masks[0]
                    fire.direction_left = -1                   
                self.orbs.add(fire)
                settings.play_sound(settings.sound_fire) 
                #print("done") 
            #get down - handle press hold
            if (event == "down") and self.onground:
                self.count_idle = 0
                #self.hsp = 0
                if self.facing_left: self.image = settings.dead_flip[1]
                else: self.image = settings.dead[1]
                self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            elif (event == "left"):
                self.facing_left = True
                self.count_idle = 0
                if self.onground:
                    self.walk_animation(self.walk_cycle_flip, self.walk_cycle_flip_masks, self.walk_delay)
                #self.hsp = -self.speed
            elif (event == "right"):
                self.facing_left = False
                self.count_idle = 0
                if self.onground:
                    self.walk_animation(self.walk_cycle, self.walk_cycle_masks,self.walk_delay)
                #self.hsp = self.speed             
            #jump
            if (event == "up") and self.onground:
                self.count_idle = 0
                #self.vsp = -self.jumpspeed
                settings.play_sound(settings.sound_jump)
            # variable height jumping
            if (event == "jump"):
                if self.vsp < -self.min_jumpspeed:
                    self.vsp = -self.min_jumpspeed   
        #empty event list
        settings.event_p2 = []
        
        if self.vsp == 0 and self.hsp == 0:            
            #DANCE!!! 
            if self.count_idle == 0: 
                settings.particle_group.empty()
            self.count_idle += 1
            if self.count_idle > self.idle:                
                self.vsp = 0    # dont move on box edges               
                if self.facing_left:
                    self.stand_animation(self.stand_cycle_flip, self.stand_cycle_flip_masks, self.stand_delay)                    
                else:                    
                    self.stand_animation(self.stand_cycle, self.stand_cycle_masks,self.stand_delay)
            # shine  
            if self.count_idle % 20 == 0: 
                pos = (self.rect.center[0] + random.randint(0,100), self.rect.center[1] + random.randint(-100,100))
                direction = pygame.math.Vector2(-5,0)    
                ParticleSpark(settings.particle_group, pos, 'white', direction, 15)
            settings.particle_group.draw(settings.screen)
            settings.particle_group.update(settings.dt)
                             
        
    
   