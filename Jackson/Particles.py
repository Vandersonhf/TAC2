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
        self.move(dt)
        self.fade(dt)
        self.check_pos()
        

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
        self.move(dt)
        self.explosion_timer()
        if self.exploding:
            self.inflate(dt)
            self.fade(dt)
            
        self.check_pos()
        self.check_size()
        self.check_alpha()


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