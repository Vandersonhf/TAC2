import pygame
from .Game import settings

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image:pygame.Surface, mask:pygame.Mask, startx:int, starty:int):
        '''General sprite for all objects
            Starting image and position x,y
        '''
        super().__init__()
        
        self.image:pygame.Surface = image
        self.mask:pygame.Mask = mask
         # return a width and height of an image
        self.size = self.image.get_size()               
        #self.image.set_colorkey((255,255,255)) 
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [startx, starty]  
        

    def update(self):
        pass

    def draw(self, screen):        
        # draw bigger image to screen at x,y position
        screen.blit(self.image, self.rect)
        
        #mask debug       
        if settings.debug: screen.blit(self.mask.to_surface(), self.rect)
    
       
    def animation(self, images:list, masks:list, delay:int, index:int, counter:int, inflate:int=0):
        # change img and mask after delay        
        self.image = images[index]           
        self.rect = self.image.get_rect(center=self.rect.center)  
        #self.rect = self.image.get_rect(midbottom=self.rect.midbottom)      
        self.mask = masks[index] 
        # inflate image + or -        
        if inflate != 0 and self.rect.size[0] > 1:
            old = self.rect.center
            self.rect = self.rect.inflate(inflate, inflate)
            self.rect.center = old            
            self.image = pygame.transform.scale(self.image, self.rect.size)               
        # counting in circle  
        counter += 1
        if index < len(images)-1:            
            if counter > delay:                
                index += 1
                counter = 0
        else:
            if counter > delay:                
                index = 0
                counter = 0 
        return index, counter 
    