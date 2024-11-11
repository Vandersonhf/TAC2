import pygame
import random
from .Game import settings

 
class Particle1():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.randint(-5,5)
        self.vel_y = random.randint(-5,5)
        self.time = 0
        self.gravity = 1
    
    def draw(self):
        self.time += 1
        #self.vel_y += self.gravity
        if self.time < 30:
            self.x += self.vel_x
            self.y += self.vel_y
            R = random.randint(0,255)
            G = random.randint(0,255)
            B = random.randint(0,255)
            pygame.draw.circle(settings.screen, (R,G,B), (self.x, self.y), random.randint(1,5))
                        
            
class Particle(pygame.sprite.Sprite):
    def __init__(self, 
                 groups:pygame.sprite.Group,
                 pos: list[int],
                 color:str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 200
        self.size = 4
        
        self.create_surf()
        
    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, self.color, (self.size/2, self.size/2), self.size/2)
        #pygame.draw.circle(self.image, (20,20,20), (self.size/2, self.size/2), self.size/2)
        self.rect = self.image.get_rect(center=self.pos)
        
        #radius = self.size * 2
        #settings.screen.blit(self.circle_surf(radius, (20,20,60)), 
        #                        (self.size/2-radius, self.size/2-radius), special_flags=pygame.BLEND_RGB_ADD)
    
    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        surf.set_colorkey((0,0,0))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        return surf
    
    def check_pos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > settings.WIDTH + 50 or
            self.pos[1] < -50 or
            self.pos[1] > settings.HEIGHT + 50
        ):
            self.kill()
    
    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        
    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)
    
    def check_alpha(self):
        if self.alpha <= 0: 
            self.kill()
    
    def update(self, dt):
        #settings.screen.blit(self.image, self.rect, special_flags=pygame.BLEND_RGB_ADD)
        self.move(dt)
        self.fade(dt)
        self.check_pos()
        self.check_alpha()
        
        #radius = self.size
        #settings.screen.blit(self.circle_surf(radius, (20,20,60)), 
        #                        self.pos, special_flags=pygame.BLEND_RGB_ADD)
        
        

class ExplodingParticle(Particle):
    def __init__(self, 
                 groups:pygame.sprite.Group,
                 pos: list[int],
                 color:str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups, pos, color, direction, speed)
        self.t0 = pygame.time.get_ticks()
        self.lifetime = random.randint(1000, 1200) 
        self.exploding = False
        self.size = 4
        self.max_size = 50
        self.inflate_speed = 500
        self.fade_speed = 3000
    
    def explosion_timer(self):
        if not self.exploding:
            t = pygame.time.get_ticks()
            if t - self.t0 > self.lifetime:
                self.exploding = True
        
    def inflate(self, dt):
        self.size += self.inflate_speed * dt
        self.create_surf()
    
    def check_size(self):
        if self.size > self.max_size:
            self.kill()
        
    def update(self, dt):
        #settings.screen.blit(self.image, self.rect, special_flags=pygame.BLEND_RGB_ADD)
        self.move(dt)
        self.explosion_timer()
        if self.exploding:
            self.inflate(dt)
            self.fade(dt)
            
        self.check_pos()
        self.check_size()
        self.check_alpha()


class ParticleRay(pygame.sprite.Sprite):
    def __init__(self, 
                 groups:pygame.sprite.Group,
                 pos: list[int],
                 color:str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 200
        self.size = 100
        
        self.create_surf()
        
    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        R = 255
        G = 255
        B = 255
        start = int(-self.size/2)
        end = int(self.size/2)
        for y in range(start, end):
            for x in range(start, end):
                dx = abs(abs(x/2)-abs(x))
                dy = abs(abs(y/2)-abs(y))
                if dx != 0 and dy != 0:
                    if dx>dy : dt = dx/dy
                    else: dt = dy/dx
                #dt = abs(abs(x/2)-abs(x)) + abs(abs(y/2)-abs(y))        # absolute distance
                #if R != 0:
                R = 200 + dt*40
                G = 200 + dt*40
                B = 200 + dt*40
                if R>255 or R<150: 
                    R = 0            
                    G = 0
                    B = 0
                pygame.draw.circle(self.image, (R,G,B), (self.size/2+x, self.size/2+y), 1)            
        self.rect = self.image.get_rect(center=self.pos)
    
    def check_pos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > settings.WIDTH + 50 or
            self.pos[1] < -50 or
            self.pos[1] > settings.HEIGHT + 50
        ):
            self.kill()
    
    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        
    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)
    
    def check_alpha(self):
        if self.alpha <= 0: 
            self.kill()
    
    def update(self, dt):
        #self.move(dt)
        self.fade(dt)
        #self.check_pos()
        #pass


class ParticleSpark(pygame.sprite.Sprite):
    def __init__(self, 
                 groups:pygame.sprite.Group,
                 pos: list[int],
                 color:str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 300
        self.size = 100
        self.fade_count = 0
        self.fade_delay = 30
        self.inflate_speed = 100
        self.factor = 10
        
        self.create_surf()
        
    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        R = 255
        G = 255
        B = 255
        saturation = 50
        start = int(-self.size/self.factor)
        end = int(self.size/self.factor)
        for y in range(start, end):
            for x in range(start, end):
                dx = abs(abs(x/self.factor)-abs(x))
                dy = abs(abs(y/self.factor)-abs(y))                
                if dx * dy > self.size/self.factor:
                    dt_color = 255
                    #dt_color = -(255 - saturation)
                elif dx * dy == self.size/self.factor:
                    dt_color = saturation                
                else: 
                    dt_color = ((dx * dy)/(self.size/self.factor))*saturation       # gradient                
                #R = 255 - saturation + dt_color
                #G = 255 - saturation + dt_color
                #B = 255 - saturation + dt_color
                R = 255 - dt_color
                G = 255 - dt_color
                B = 255 - dt_color
                if R>255 or R<0: 
                    R = 0            
                    G = 0
                    B = 0
                pygame.draw.circle(self.image, (R,G,B), (self.size/self.factor+x, self.size/self.factor+y), 1)                 
        self.rect = self.image.get_rect(center=self.pos)
    
    def check_pos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > settings.WIDTH + 50 or
            self.pos[1] < -50 or
            self.pos[1] > settings.HEIGHT + 50
        ):
            self.kill()
    
    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos        
        
    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)
    
    def check_alpha(self):
        if self.alpha <= 0: 
            self.kill()
        
    def inflate(self, dt):
        self.size += self.inflate_speed * dt
        self.create_surf()
        
    def deflate(self, dt):
        if self.rect.size[0] > 1:            
            self.size -= self.inflate_speed * dt
            if self.rect.size[0] > 10 and self.rect.size[1] > 10:
                self.create_surf()
            else: self.kill()
    
    def check_size(self):
        if self.size < 1:
            self.kill()
    
    def update(self, dt):       
        self.move(dt)        
        self.check_pos()
        
        self.fade_count += 1
        if self.fade_count > self.fade_delay:
            self.fade(dt)
            self.check_alpha()           
            self.check_size()
       
        # light
        #radius = self.size/self.factor       
        #settings.screen.blit(self.circle_surf(radius, (20,20,160)), self.rect.topleft,
        #                special_flags=pygame.BLEND_RGB_ADD)
        
    
    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        surf.set_colorkey((0,0,0))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        return surf           
            


class NiceEffect:
    def fireworks(self, cenario, cenario_rect):
        self.particle_group = pygame.sprite.Group()
        time = 300
        count = 0
        self.x = (settings.WIDTH/2 - 300, settings.WIDTH/2, settings.WIDTH/2 + 300)
        self.y = (settings.HEIGHT/2 - 300, settings.HEIGHT/2, settings.HEIGHT/2 + 300) 
        while True:
            dt = settings.clock.tick(settings.fps) / 1000   
            count += 1
            if count>time: return
                                 
            # delay every 50 frames              
            if count % 50 == 0:
                #self.spawn_particles()
                self.spawn_exploding_particles()
            
            #background
            settings.screen.blit(cenario, cenario_rect)
            self.particle_group.draw(settings.screen)
            self.particle_group.update(dt)
            
            #update screen
            pygame.display.update()
    
    
    def spawn_particles(self):
        pos = (random.choice(self.x), random.choice(self.y))
        for _ in range(1000):
            color = random.choice(("red", "green", "blue"))
            direction = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))  
            direction = direction.normalize()  
            speed = random.randint(50, 400)          
            Particle(self.particle_group, pos, color, direction, speed)
            
    
    def spawn_exploding_particles(self):
        pos = (random.choice(self.x), random.choice(self.y))
        for _ in range(1000):
            color = random.choice(("red", "yellow", "orange"))   
            direction = pygame.math.Vector2(random.uniform(-0.2, 0.2), random.uniform(-1,0))
            direction = direction.normalize()  
            speed = random.randint(50, 400)                    
            ExplodingParticle(self.particle_group, pos, color, direction, speed)   
            
    
    def fireworks1(self, cenario, cenario_rect):
        particles = []
        time = 200
        count = 0
        while True:
            count += 1            
            if count>time: return            
            # particles            
            for _ in range(20):
                particles.append(Particle1(settings.WIDTH/2, settings.HEIGHT/3))
            for _ in range(20):
                particles.append(Particle1(settings.WIDTH/2-200, settings.HEIGHT/3+100))    
            for _ in range(20):
                particles.append(Particle1(settings.WIDTH/2+200, settings.HEIGHT/3+100))
                
            #background
            settings.screen.blit(cenario, cenario_rect)
            for p in particles:
                p.draw()
            
            #update screen
            pygame.display.flip()
            settings.clock.tick(settings.fps)
            
    
    
    def rays(self, cenario, cenario_rect):
        self.particle_group = pygame.sprite.Group()
        time = 500
        count = 0
        self.x = (settings.WIDTH/2 - 300, settings.WIDTH/2, settings.WIDTH/2 + 300)
        self.y = (settings.HEIGHT/2 - 300, settings.HEIGHT/2, settings.HEIGHT/2 + 300) 
        while True:
            dt = settings.clock.tick(settings.fps) / 1000   
            count += 1
            if count>time: return
                                 
            # delay every 50 frames              
            if count % 30 == 0:
                self.spawn_rays()
            
            #background
            settings.screen.blit(cenario, cenario_rect)
            self.particle_group.draw(settings.screen)
            self.particle_group.update(dt)
            
            #update screen
            pygame.display.update()
    
    
    def spawn_rays(self):
        pos = (random.choice(self.x), random.choice(self.y))
        #for _ in range(1000):
        #color = random.choice(("red", "green", "blue"))
        #direction = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))  
        #direction = direction.normalize()  
        #speed = random.randint(50, 400)          
        ParticleRay(self.particle_group, pos, 'white', (0,0), 0)
        
    
    def sparks(self, cenario, cenario_rect):
        self.particle_group = pygame.sprite.Group()
        time = 300
        count = 0
        self.x = (settings.WIDTH/2 - 30, settings.WIDTH/2, settings.WIDTH/2 + 30)
        self.y = (settings.HEIGHT/2 - 30, settings.HEIGHT/2, settings.HEIGHT/2 + 30) 
        while True:
            dt = settings.clock.tick(settings.fps) / 1000   
            count += 1
            if count>time: return
                                 
            # delay every 50 frames              
            if count % 30 == 0:
                self.spawn_sparks()
            
            #background
            settings.screen.blit(cenario, cenario_rect)
            #self.particle_group.draw(settings.screen)
            self.particle_group.update(dt)
            
            #update screen
            pygame.display.update()
    
    
    def spawn_sparks(self):
        pos = (random.choice(self.x), random.choice(self.y))
        #for _ in range(1000):
        #color = random.choice(("red", "green", "blue"))
        direction = pygame.math.Vector2(random.uniform(0,0), random.uniform(-1,0))  
        direction = direction.normalize()  
        #speed = random.randint(50, 400)          
        ParticleSpark(self.particle_group, pos, 'white', direction, 15)
        
    
    def light(self):
        particles = []
        time = 200
        count = 0
        #pygame.mouse.set_visible(True)
        while True:
            count += 1            
            if count>time: return                        
                
            #background
            settings.screen.fill((0,0,0))
            pygame.draw.rect(settings.screen, (50,20,120), pygame.Rect(100,100,200,80))
            pygame.event.pump()
            mx, my = pygame.mouse.get_pos()
            #print( mx, my)
            particles.append([[mx, my], [random.randint(0,20)/10-1, -5], random.randint(6,11)])
            
            for p in particles:
                p[0][0] += p[1][0]
                p[0][1] += p[1][1]
                p[2] -= 0.1
                p[1][1] += 0.15
                pygame.draw.circle(settings.screen, (255,255,255), [int(p[0][0]), int(p[0][1])], int(p[2]))
                
                radius = p[2] * 2
                settings.screen.blit(self.circle_surf(radius, (20,60,20)), 
                                     (int(p[0][0])-radius, int(p[0][1])-radius), special_flags=pygame.BLEND_RGB_ADD)
                
                if p[2] <= 0:
                    particles.remove(p)
            
            #update screen
            pygame.display.update()
            settings.clock.tick(settings.fps)
    
    
    def light2(self):
        particles = []
        time = 300
        count = 0        
        while True:
            count += 1            
            if count>time: return 
            #background
                       
            pygame.event.pump()
            #mx, my = pygame.mouse.get_pos()
            #print( mx, my)
            particles.append([[200, 200], [1, 1], 10])
            settings.screen.fill((0,0,0))
            for p in particles:
                p[0][0] += p[1][0]
                p[0][1] += p[1][1]
                p[2] -= 0.1
                #p[1][1] += 0.15
                pygame.draw.circle(settings.screen, (255,255,255), [int(p[0][0]), int(p[0][1])], int(p[2]))
                
                radius = p[2] * 2
                settings.screen.blit(self.circle_surf(radius, (20,20,60)), 
                                     (int(p[0][0])-radius, int(p[0][1])-radius), special_flags=pygame.BLEND_RGB_ADD)
                
                if p[2] <= 0:
                    particles.remove(p)
            
            #update screen
            pygame.display.update()
            settings.clock.tick(settings.fps)
    
    
    def fire(self):
        particles = []
        time = 500
        count = 0
        #pygame.mouse.set_visible(True)
        while True:
            count += 1            
            if count>time: return                        
                
            #background
            settings.screen.fill((0,0,0))
            #pygame.draw.rect(settings.screen, (50,20,120), pygame.Rect(100,100,200,80))
            #pygame.event.pump()
            #mx, my = pygame.mouse.get_pos()
            #print( mx, my)
            particles.append([[random.randint(500,550), 200], 
                              [random.randint(0,20)/10-1, -4],
                              random.randint(8,12)])
            color = random.choice(("red", "yellow", "orange"))
            for p in particles:
                p[0][0] += p[1][0]
                p[0][1] += p[1][1]
                p[2] -= 0.4
                #p[1][1] += 0.15
                pygame.draw.circle(settings.screen, color, [int(p[0][0]), int(p[0][1])], int(p[2]))
                
                radius = p[2] * 2
                settings.screen.blit(self.circle_surf(radius, (150,20,20)), 
                                     (int(p[0][0])-radius, int(p[0][1])-radius), special_flags=pygame.BLEND_RGB_ADD)
                
                if p[2] <= 0:
                    particles.remove(p)
            
            #update screen
            pygame.display.update()
            settings.clock.tick(settings.fps)
            
    
    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        surf.set_colorkey((0,0,0))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        return surf