import pygame
from .Settings import *

class Editor():
    def run(self):
        #init          
        self.W = settings.WIDTH
        self.H = settings.HEIGHT
        self.grid_max_x = int(self.W*0.8)
        self.grid_max_y = int(self.H*0.95)
        self.grid_start_x = int(self.W*0.05)
        self.grid_start_y = int(self.H*0.1)
        self.tile_size = settings.tile
        self.grid_w = ((self.grid_max_x - self.grid_start_x) // self.tile_size) * self.tile_size    
        self.grid_h = ((self.grid_max_y - self.grid_start_y) // self.tile_size) * self.tile_size
        self.map_lin = settings.map_lin
        self.map_col = settings.map_col
        
        self.tile_list = settings.objects + settings.back + settings.back2 + settings.items + settings.enemies
        self.total_size = len(self.tile_list)
        
        self.text_count = 0     # count time on text appear
        self.tile_pal = []      # tile pallete
        self.setup_map_grid() 
        self.select_lin = 0       # selected tile
        self.select_col = 0          
        #grid - map screen        
        self.grid_anchor = [0,0]       # main fix point for scrolling        
        self.update_grid()
        
        #buttons
        self.b1 = Button(self.grid_max_x+10,self.grid_max_y,150,50,"Save map")   
        self.b2 = Button(self.W-160,self.grid_max_y,150,50,"Exit")  
        self.b3 = Button(10,self.grid_max_y,150,50,"Back") 
        self.b_right = Button(self.grid_w+40,self.H/2,50,50,">>")  
        self.b_left = Button(self.grid_start_x-60,self.H/2,50,50,"<<")    
        self.b_up1 = Button(self.grid_max_x/2,self.grid_start_y-60,50,50,"^")
        self.b_down1 = Button(self.grid_max_x/2,self.grid_h+20,50,50,"v")
                       
        # main editor loop
        while True:
            pygame.event.pump()
            settings.screen.fill(BACKGROUND)
            
            self.draw()            
            if not self.handle_events(): return
             
            #update buttons
            self.b1.update()
            self.b2.update()
            self.b3.update()
            self.b_right.update()
            self.b_left.update()
            self.b_up1.update()
            self.b_down1.update()
                                
            #update screen
            pygame.display.flip()
            settings.clock.tick(settings.fps)
    
    
    def setup_map_grid(self):
        #create map
        matrix = []
        for lin in range(self.map_lin):
            l = [] 
            for col in range(self.map_col):
                tile = Tile()
                l.append(tile)
            matrix.append(l)      
        self.map = self.open_map(matrix)     # load map
                         
    
    def update_grid(self):
        self.grid = []
        pos_lin = 0
        for gy in range(self.grid_start_y,self.grid_h+1,self.tile_size):        
            l = []      
            pos_col = 0      
            for gx in range(self.grid_start_x,self.grid_w+1,self.tile_size):
                rect = pygame.Rect(gx,gy,self.tile_size,self.tile_size)
                type = self.map[pos_lin+self.grid_anchor[0]][pos_col+self.grid_anchor[1]].type 
                surf = None                
                if type > 0:
                    surf = self.tile_list[type-1]               
                tile = Tile(surf, rect, type)
                l.append(tile)
                pos_col += 1
            self.grid.append(l) 
            pos_lin += 1
    
    
    def draw(self):
        # Draw loop  
        pygame.draw.line(settings.screen, BRANCO, (self.grid_max_x,0),(self.grid_max_x,self.H))
        self.blit_text(f'SIZE:{self.map_lin}x{self.map_col} tiles', settings.fonte, settings.screen, 10, 10)
        self.blit_text(f'RESOLUTION:{self.W}x{self.H}', settings.fonte, settings.screen, 400, 10)
        self.blit_text(f'TILE:{settings.tile} px', settings.fonte, settings.screen, 10, 50)
        self.blit_text(f'GRID:{len(self.grid)}x{len(self.grid[0])}', settings.fonte, settings.screen, 200, 50)  
        self.blit_text(f'ANCHOR:{self.grid_anchor}', settings.fonte, settings.screen, 400, 50)
        for g_lin in range(len(self.grid)):                
            for g_col in range(len(self.grid[0])):
                tile:Tile = self.grid[g_lin][g_col]
                block:pygame.Rect = tile.rect
                pygame.draw.rect(settings.screen, BRANCO, block,1)
                if tile.surf:
                    settings.screen.blit(tile.surf, tile.rect.topleft)                
        self.draw_pallete()
    
    
    def draw_pallete(self):   
        #blit matrix
        x = self.W*0.81     # initial position
        y = self.H*0.2
        t = self.tile_size
        self.tile_pal = self.get_pallete(x,y,t)  
        for lin in range(len(self.tile_pal)):
            for col in range(len(self.tile_pal[lin])):
                pygame.draw.rect(settings.screen, BRANCO,(x-1,y-1,t+2,t+2),1)
                settings.screen.blit(self.tile_pal[lin][col].surf, (x,y))
                x += settings.tile + 3
            y += settings.tile + 3
            x = self.W*0.81

        # draw elements - pallette
        x = self.grid_max_x+10
        self.blit_text(f'SELECT:', settings.fonte, settings.screen, x, 10)
        x = int((self.W-self.grid_max_x)/2) + self.grid_max_x
        pygame.draw.rect(settings.screen, BRANCO,(x-5,self.grid_start_y-5,
                                                  self.tile_size+10,self.tile_size+10),5)        
        settings.screen.blit(self.tile_pal[self.select_lin][self.select_col].surf, (x,self.grid_start_y))
                
    
    def get_pallete(self, x, y, t): 
        #draw list of tiles - get tile per line
        x_fit = int((self.W*0.99 - self.W*0.81) // settings.tile)
        y_fit = int((self.H*0.8 - self.H*0.2) // settings.tile)        
        tile_pal = []
        count_tile = 0        
        x_init = x        
        for _ in range(y_fit):
            line = []
            for __ in range(x_fit):
                if count_tile < self.total_size:  
                    surf = self.tile_list[count_tile]
                    rect = pygame.Rect(x,y,t,t)
                    tile = Tile(surf, rect, count_tile+1)                    
                    line.append(tile)                    
                    count_tile += 1
                else: 
                    tile_pal.append(line)
                    return tile_pal
                x += settings.tile + 3
            y += settings.tile + 3
            x = x_init
            tile_pal.append(line)
        return tile_pal
                
        
    def handle_events(self):
        # pick up element fill cenario
        press3 = pygame.mouse.get_pressed()[0]
        press4 = pygame.mouse.get_pressed()[2]
        for event in pygame.event.get():
            press1 = event.type == pygame.MOUSEBUTTONDOWN
            press2 = event.type == pygame.MOUSEMOTION            
            if (press1 or press2) and press3:
                self.editor_check_collision_fill()
            if (press1 or press2) and press4:
                self.editor_check_collision_erase()     
            if press1 and event.button == 1:
                # Call the on_mouse_button_down() function
                if self.b1.button_rect.collidepoint(event.pos):
                    self.save_map()
                    self.text_count += 1
                if self.b2.button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                if self.b3.button_rect.collidepoint(event.pos):
                    return 0
                for lin in range(len(self.tile_pal)):
                    for col in range(len(self.tile_pal[lin])):
                        if self.tile_pal[lin][col].rect.collidepoint(event.pos):
                            self.select_lin = lin
                            self.select_col = col
        # check map control    
        key = pygame.key.get_pressed()
        if (self.b_right.button_rect.collidepoint(pygame.mouse.get_pos()) and press3) or key[pygame.K_RIGHT]:            
            if self.grid_anchor[1] < self.map_col - len(self.grid[0]):
                self.grid_anchor[1] += 1        
                self.update_grid()
        if (self.b_left.button_rect.collidepoint(pygame.mouse.get_pos()) and press3) or key[pygame.K_LEFT]:
            if self.grid_anchor[1] > 0: 
                self.grid_anchor[1] -= 1        
                self.update_grid()
        if (self.b_up1.button_rect.collidepoint(pygame.mouse.get_pos()) and press3) or key[pygame.K_UP]:
            if self.grid_anchor[0] > 0: 
                self.grid_anchor[0] -= 1        
                self.update_grid()
        if (self.b_down1.button_rect.collidepoint(pygame.mouse.get_pos()) and press3) or key[pygame.K_DOWN]:            
            if self.grid_anchor[0] < self.map_lin - len(self.grid): 
                self.grid_anchor[0] += 1        
                self.update_grid()
        if self.text_count > 0:
            self.blit_text(f'Map Saved!', settings.fonte, settings.screen, 
                              self.grid_max_x+10, self.grid_max_y-50, 100)
        return 1
        
    
    def open_map(self, map:list):
        try:
            with open('Jackson/save.txt','r') as save_file:                           
                gy = 0            
                for line in save_file.readlines():                    
                    gx = 0
                    for type in line.split(','):                        
                        if type.isdigit:
                            tile:Tile = map[gy][gx]
                            tile.set_type(int(type))
                            gx += 1                            
                    gy += 1
                return map
        except FileNotFoundError:
            return map           
    
    
    def save_map(self):
        map_file = ''
        for g_lin in range(len(self.map)):
            for g_col in range(len(self.map[0])):
                tile:Tile = self.map[g_lin][g_col]
                map_file += str(tile.type) + ','     # type of tile - have to map
            map_file = map_file[:-1]
            map_file += '\n'
        with open('Jackson/save.txt','w') as save_file:            
            save_file.write(map_file)
        
    
    def editor_check_collision_fill (self):        
        for g_lin in range(len(self.grid)):
            for g_col in range(len(self.grid[0])):
                tile:Tile = self.grid[g_lin][g_col]
                block:pygame.Rect = tile.rect
                if block.collidepoint(pygame.mouse.get_pos()):
                    sel_tile = self.tile_pal[self.select_lin][self.select_col]
                    settings.screen.blit(sel_tile.surf, block.topleft)
                    tile.set_type(sel_tile.type)
                    tile.surf = sel_tile.surf
                    #update map                    
                    tile = self.map[g_lin+self.grid_anchor[0]][g_col+self.grid_anchor[1]]  # from map to grid
                    tile.type = sel_tile.type
                
                     
    def editor_check_collision_erase (self):  
        for g_lin in range(len(self.grid)):
            for g_col in range(len(self.grid[0])):
                tile:Tile = self.grid[g_lin][g_col]
                block:pygame.Rect = tile.rect
                if block.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(settings.screen, BACKGROUND,self.grid[g_lin][g_col])
                    tile.set_type(0)
                    tile.surf = None
                    #update map                    
                    tile = self.map[g_lin+self.grid_anchor[0]][g_col+self.grid_anchor[1]]  # from map to grid
                    tile.type = 0
                    
    
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
     
     
class Button():    
    
    def __init__(self, x, y, w, h, text='', font=24, color=(0,0,0)):        
        self.w = w
        self.h = h
        
        # Create a surface for the button
        self.button_surface = pygame.Surface((w, h))
        
        # Create a font object
        font = pygame.font.Font(None, font)
        
        # Render text on the button
        self.text = font.render(text, True, color)
        self.text_rect = self.text.get_rect(center=(self.button_surface.get_width()/2,
                                                    self.button_surface.get_height()/2))

        # Create a pygame.Rect object that represents the button's boundaries
        self.button_rect = pygame.Rect(x, y, w, h)  # Adjust the position as needed
        
        
    def update(self):
        # Check if the mouse is over the button. This will create the button hover effect
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.button_surface, VERDE, (1, 1, self.w-2, self.h-2))
        else:
            pygame.draw.rect(self.button_surface, PRETO, (0, 0, self.w, self.h))
            pygame.draw.rect(self.button_surface, BRANCO, (1, 1, self.w-2, self.h-2))               
        
        # Show the button text
        self.button_surface.blit(self.text, self.text_rect)
        
        # Draw the button on the screen
        settings.screen.blit(self.button_surface, (self.button_rect.x, self.button_rect.y))
                
        
class Tile():
    def __init__(self, surf:pygame.Surface=None, rect:pygame.Rect=None, type:int=0):        
        self.surf = surf
        self.type = type
        self.rect = rect
        
    def set_type(self, type):
        self.type = type