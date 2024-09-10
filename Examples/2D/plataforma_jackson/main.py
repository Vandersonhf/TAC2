import pygame, numpy
from pygame.locals import *
import sys 

WIDTH = 400
HEIGHT = 300
BACKGROUND = (0, 0, 0)
background_image = 'cenario.jpg'
game_images = {}
move_delay = 7


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
         # return a width and height of an image
        self.size = self.image.get_size()               
        #self.image.set_colorkey((255,255,255)) 
        
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]        

    def update(self):
        pass

    def draw(self, screen):        
        # draw bigger image to screen at x,y position
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_image = pygame.image.load("p1_jump.png")

        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,19)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 11
        self.vsp = 0
        self.gravity = 2.8
        self.min_jumpspeed = 3
        self.delay = 0        
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]        
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.delay += 1
            if self.delay > move_delay:
                self.animation_index += 1
                self.delay = 0
        else:
            self.animation_index = 0      
        

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, boxes):
        hsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        key = pygame.key.get_pressed()
        # if user clicks on cross button, close the game 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                        event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit() 
        
        if key[pygame.K_LEFT]:
            self.facing_left = True
            if onground:
                self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            if onground:
                self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_UP] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            self.jump_animation()
            self.delay += 1
            if self.delay > move_delay:
                self.vsp += self.gravity
                self.delay = 0
            #self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, boxes)

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide


class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)

    boxes = pygame.sprite.Group()
    for bx in range(0, 400, 70):
        boxes.add(Box(bx, 300))

    boxes.add(Box(330, 230))
    boxes.add(Box(100, 70))

    while True:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        screen.fill(BACKGROUND)
        
        game_images['background'] = pygame.image.load( 
        background_image).convert_alpha() 
        cenario = game_images['background'].get_size()
        # create a 2x bigger image than self.image
        large_cenario = pygame.transform.scale(game_images['background'], (int(cenario[0]*2), int(cenario[1]*2)))
        
        screen.blit(large_cenario, (0, 0)) 
        
        
        player.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()