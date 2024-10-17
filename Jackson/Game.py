import pygame
from .Settings import *
from .Player import Player
from .Objects import FixObj, AniObj
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
                        
        self.background = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()        
                
        #load map and get boundary limits
        self.map_size = self.open_map()
        
        # main game loop
        while True:
            pygame.event.pump()

            # Draw loop      
            settings.screen.blit(self.cenario, self.cenario_rect)  
            self.blit_text(f'SCORE:{self.player.score}', settings.fonte, settings.screen, 10, 10)           
            #pygame.draw.rect(settings.screen, BRANCO, self.cenario_rect, 20)   #debug
                
            self.ground.update() 
            #self.background.update()  
            self.items.update(self.cenario_rect) 
            self.enemies.update(self.cenario_rect)
            # update elements in memory
            self.cenario_rect = self.player.update(self.ground, self.enemies,
                                                   self.cenario_rect, self.items)            
                                    
            #update screen
            pygame.display.flip()
            settings.clock.tick(settings.fps)
    
        
    def open_map(self):
        self.cenario.fill(BACKGROUND)
        max_x = 0   # get limits of the cenario
        max_y = 0   # y = lin
        t = settings.tile
        tile_list = [settings.objects, settings.back, settings.back2, settings.items, settings.enemies]
        map = self.get_tile_type_map(tile_list)
        try:
            with open('Jackson/save.txt','r') as save_file:                           
                gy = 0            
                for line in save_file.readlines():                    
                    gx = 0
                    for type in line.split(','):                        
                        if type.isdigit:
                            type = int(type)
                            if type > 0:
                                max_x, max_y = self.create_tile(map, type, tile_list,
                                                                gx, gy, max_x, max_y, t)                                                                                  
                        gx += 1                              
                    gy += 1                    
                return (gy*settings.tile, gx*settings.tile)
        except FileNotFoundError:
            return None
    
    
    def create_tile(self, map, type, tile_list, gx, gy, max_x, max_y, t):
        obj = None        
        for idx,val in enumerate(map):
            if type <= val:                
                if idx == 0: item = type-1 
                else: item = -(val-type-len(tile_list[idx])+1) # hard one debug 
                if idx == 0:  # first list of tiles
                    if item == 1:   #brick                        
                        obj = AniObj([settings.objects[1]], [settings.objects_mask[1]],
                                     idx, item, settings.ex_brick)
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                        self.items.add(obj)                        
                    else:   #floor
                        obj = FixObj(tile_list[idx][item])
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                        self.ground.add(obj)
                        self.cenario.blit(obj.image, obj.rect.topleft)
                elif idx == 1 or idx == 2:
                    obj = FixObj(tile_list[idx][item])
                    obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                    self.background.add(obj)
                    self.cenario.blit(obj.image, obj.rect.topleft)
                elif idx == 3: 
                    if item == 0:   #box ?
                        obj = AniObj(settings.box, settings.box_mask, idx, item, settings.box_empty)
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                        self.items.add(obj)
                    if item == 1:   #coin
                        obj = AniObj(settings.coin, settings.coin_mask, idx, item)
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                        self.items.add(obj)  
                elif idx == 4: 
                    if item == 0:   #mob 1
                        obj = Enemy1()
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                        self.enemies.add(obj)                      
                if obj: 
                    if gx > max_x : max_x = gx
                    if gy > max_y : max_y = gy
                break 
        return max_x, max_y
    
    
    def get_tile_type_map(self,lists):
        #map of tiles obj
        sum = 0       
        count = 0 
        map = []
        for list in lists:
            map.append(sum+len(list))  
            sum = map[count]
            count += 1
        return map
        
            
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


    def blit_text(self, texto, fonte, janela, x, y, delay=0, pos='topleft'):
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