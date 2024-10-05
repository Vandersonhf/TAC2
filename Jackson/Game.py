import pygame
from .Settings import *
from .Player import Player
from .Objects import Box, Floor1, FixObj
from .Enemy import Enemy1
from .Editor import Editor

class Jackson():      
    def play(self, debug:bool):  
        settings.setup(debug)
                  
        #menu
        editor = Editor()
        editor.run()
                      
        #sounds
        pygame.mixer.music.play(-1, 0.0)
        settings.somAtivado = True
        
        # Ocultando o cursor 
        pygame.mouse.set_visible(False)
                
        self.player = Player(settings.WIDTH*0.1, (settings.map_lin-3)*settings.tile)
        self.ground = pygame.sprite.Group()         
        
        #cenario
        h = settings.map_lin*settings.tile
        w = settings.map_col*settings.tile
        self.cenario = pygame.Surface((w, h))   #wrapper for whole map
        self.cenario_rect = pygame.Rect(0, 0, w, h) 
        
        #load map and get boundary limits
        self.map_size = self.open_map()
                
        self.enemies = pygame.sprite.Group()
        
        # main game loop
        while True:
            pygame.event.pump()

            # Draw loop            
            settings.screen.blit(self.cenario, self.cenario_rect)             
                             
            # update elements in memory
            self.cenario_rect = self.player.update(self.ground, self.enemies,
                                                   self.cenario_rect, self.map_size)
            #pygame.draw.rect(settings.screen, BRANCO, self.cenario_rect, 20)   #debug
            self.ground.update()            
            #enemies.update()
                      
            self.player.draw(settings.screen)
                        
            #update screen
            pygame.display.flip()
            settings.clock.tick(settings.fps)
    
        
    def open_map(self):
        self.cenario.fill(BACKGROUND)
        max_x = 0   # get limits of the cenario
        max_y = 0   # y = lin
        try:
            with open('Jackson/save.txt','r') as save_file:                           
                gy = 0            
                for line in save_file.readlines():                    
                    gx = 0
                    for type in line.split(','):                        
                        if type.isdigit:
                            type = int(type)
                            if type > 0:
                                floor = FixObj(settings.objects[type-1], settings.objects_mask[type-1])
                                t = settings.tile
                                floor.rect = pygame.Rect(gx*t, gy*t, t, t) 
                                self.ground.add(floor) 
                                self.cenario.blit(floor.image, floor.rect.topleft)  
                                if gx > max_x : max_x = gx
                                if gy > max_y : max_y = gy                                                   
                            gx += 1                              
                    gy += 1                    
                return (gy*settings.tile, gx*settings.tile)
        except FileNotFoundError:
            return None
    
            
    def terminar(self):
        # Termina o programa.
        pygame.quit()
        exit()
        
    def aguardarEntrada(self):
        # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    Jackson.terminar()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        Jackson.terminar()
                    return

    def colocarTexto(self, texto, fonte, janela, x, y, delay=0, pos='topleft'):
        if delay > 0:             
            if self.text_count <= delay:
                self.text_count += 1           
                self.render_text(texto, fonte, janela, x, y, pos)     
            else:
                self.text_count = 0
        else: self.render_text(texto, fonte, janela, x, y, pos)

    
    def render_text(self, texto, fonte, janela, x, y, pos='topleft'):
        objTexto = fonte.render(texto, True, CORTEXTO)
        rectTexto:pygame.Rect = objTexto.get_rect()
        if pos == 'topleft': rectTexto.topleft = (x, y)
        if pos == 'center': rectTexto.center = (x, y)
        janela.blit(objTexto, rectTexto)