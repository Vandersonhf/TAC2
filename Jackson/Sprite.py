import pygame

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