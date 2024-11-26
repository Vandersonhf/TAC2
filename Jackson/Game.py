import pygame
from .Settings import *
from .Player import Player, Player2
from .Objects import FixObj, AniObj, FirePit
from .Enemy import Mob1, Boss
from .Editor import Editor
from .Particles import NiceEffect
from .Server import AppServer
from .Client import AppClient
import threading

class Jackson():
    def run(self, debug:bool):
        settings.setup(debug)
                
        list = ['START GAME', 'MULTIPLAYER', 'OPTIONS', 'EDITOR', 'EXIT']
        menu = Basic_menu_all(list)
        select = menu.run()
        
        while select != 0:
            settings.multiplayer = False
            if select == 1:                        
                self.new_game()
            elif select == 2:
                settings.multiplayer = True
                list = ['HOST', 'JOIN', 'BACK']
                menu2 = Basic_menu_all(list)
                select = menu2.run()
                if select == 3:
                    select = menu.run()
                elif select == 1:
                    # server
                    settings.server = True
                    threading.Thread(target=self.server_thread).start()
                    self.new_game()       
                elif select == 2:
                    # cliente                    
                    settings.client = True
                    threading.Thread(target=self.client_thread).start()
                    self.new_game()
            elif select == 3:            
                select = menu.run()
            elif select == 4:
                pygame.mouse.set_visible(True)
                editor = Editor()
                editor.run()
                select = menu.run()
            elif select == 5:
                self.exit()
    
    def server_thread(self):
        settings.server_socket = AppServer("localhost", 5041)
        settings.server_socket.server_listen()
        
    def client_thread(self):      
        settings.client_socket = AppClient("localhost",  5041)
        settings.client_socket.connect_server()  
        settings.client_socket.receive_messages()
    
    def new_game (self):
        # Ocultando o cursor 
        pygame.mouse.set_visible(False)
        #pygame.event.pump()
        
        while True:    # laço externo do game over
            # Configurando o começo do jogo.
            #sounds
            pygame.mixer.music.load('Jackson/sound/Smooth Criminal.wav')
            pygame.mixer.music.play(-1, 0.0)
            settings.somAtivado = True      
            self.life_counter = 0
            self.life_delay = 20
            self.life_show = True
                     
            #cenario
            h = settings.map_lin*settings.tile
            w = settings.map_col*settings.tile
            self.cenario = pygame.Surface((w, h))   #wrapper for whole map
            self.cenario_rect = pygame.Rect(0, 0, w, h) 
                            
            self.ground = pygame.sprite.Group() 
            self.background = pygame.sprite.Group()
            self.items = pygame.sprite.Group()
            self.coins = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group() 
            #self.fire_pit = pygame.sprite.Group() 
            self.fire_pit = []    
            self.boss_fire_list = pygame.sprite.Group() 
            
            #load map and get boundary limits
            self.map_size = self.open_map()
            
            # aux lists
            self.loot = pygame.sprite.Group()
            self.loot.add(self.items)
            self.loot.add(self.coins)
            self.solid = pygame.sprite.Group()
            self.solid.add(self.ground)
            self.solid.add(self.items)
            self.hazard = pygame.sprite.Group()
            self.hazard.add(self.enemies) 
            
            self.player = Player(settings.WIDTH*0.1, (settings.map_lin-3)*settings.tile) 
            self.player2 = None           
            #self.player2 = None
            if settings.multiplayer:
                self.life_counter2 = 0
                self.life_delay2 = 20
                self.life_show2 = True
                self.player2 = Player2(settings.WIDTH*0.1, (settings.map_lin-3)*settings.tile)
                                    
            self.main_loop()
            
            # Parando o jogo e mostrando a tela final.            
            if len(self.enemies) == 0: 
                boom = NiceEffect()
                boom.fireworks(self.cenario, self.cenario_rect)                
                self.__menu_win__()
            else: self.__menu_last__()
    
   
    def main_loop(self):
        # main game loop
        while True:          
            settings.dt = settings.clock.tick(settings.fps) / 1000 
            # Draw loop      
            settings.screen.blit(self.cenario, self.cenario_rect) 
            
            if settings.multiplayer:
                if settings.server:                    
                    if settings.client_connected:
                        self.player2.update(self.ground, self.hazard, self.cenario_rect, self.loot)                    
                if settings.client:
                    # update cenario, players, items, etc.                   
                    self.player2.update(self.ground, self.hazard, self.cenario_rect, self.loot)
                self.draw_panel2()
                       
            #update game elements 
            self.update_game()
                                        
            # Panel      
            self.draw_panel()          
                                              
            #update screen
            pygame.display.update()
                       
            if not self.cenario_rect: return    # dead
            if len(self.enemies) == 0: return   # WIN
    
    
    def update_game(self):        
        self.hazard.add(self.boss_fire_list)
        #hazard.add(self.fire_pit)
                        
        # updates in memory 
        self.ground.update()              
        self.items.update(self.cenario_rect) 
        self.coins.update(self.cenario_rect)            
        self.enemies.update(self.solid, self.cenario_rect, self.player, self.player2, self.boss_fire_list)
        #self.fire_pit.update(self.cenario_rect)
        for p in self.fire_pit: p.update(self.cenario_rect)
        if self.boss_fire_list: self.boss_fire_list.update(self.cenario_rect, self.ground, self.items)
        self.cenario_rect = self.player.update(self.ground, self.hazard, self.cenario_rect, self.loot)
         
    
    def draw_panel2(self):
        # blit panel
        self.blit_text(f'PLAYER: Zé2', settings.fonte, settings.screen, settings.WIDTH-10, 10, pos='topright')
        settings.screen.blit(settings.coin[0], pygame.Rect(settings.WIDTH-120,90,settings.base_tile,settings.base_tile))
        self.blit_text(f':{self.player2.score}', settings.fonte, settings.screen, settings.WIDTH-80, 100, pos='topleft')             
        cor = VERDE
        if self.player2.life > 30 and self.player2.life < 70: cor = CORTEXTO2
        if self.player2.life <= 30: cor = CORTEXTO3
        # life bar        
        rect = pygame.Rect(settings.WIDTH-250, 50, 220, 24) 
        life_rect = pygame.Rect(settings.WIDTH-248, 52, int((220*self.player2.life)/self.player2.max_life)-4, 20) 
        pygame.draw.rect(settings.screen, 'white', rect)
        # blinking when low life
        if self.player2.life <= 30:
            if self.life_counter2 >= 0:
                if self.life_counter2 < self.life_delay2:
                    self.life_counter2 += 1
                else: 
                    self.life_show2 = False
                    self.life_counter2 = -1
            else:
                if self.life_counter2 > -self.life_delay2:
                    self.life_counter2 -= 1
                else:
                    self.life_show2 = True
                    self.life_counter2 = 1
        if self.life_show2: pygame.draw.rect(settings.screen, cor, life_rect) 
    
    
    def draw_panel(self):
        # blit panel
        self.blit_text(f'PLAYER: Zé', settings.fonte, settings.screen, 10, 10)
        #self.blit_text(f'Kill all enemies to win!', settings.fonte, settings.screen, 350, 90)
        #self.blit_text(f'CTRL:run,SPACE:shoot,M:on/off music',
        #                settings.fonte, settings.screen, 350, 10)
        #self.blit_text(f'ESC:exit,F5:save,F6:load',
        #                settings.fonte, settings.screen, 350, 50)
        self.blit_text(f'FPS: {int(settings.clock.get_fps())}', settings.fonte, settings.screen, 10, 150)
        settings.screen.blit(settings.coin[0], pygame.Rect(10,90,settings.base_tile,settings.base_tile))
        self.blit_text(f':{self.player.score}', settings.fonte, settings.screen, 50, 100)             
        cor = VERDE
        if self.player.life > 30 and self.player.life < 70: cor = CORTEXTO2
        if self.player.life <= 30: cor = CORTEXTO3
        # life bar        
        rect = pygame.Rect(10, 50, 220, 24) 
        life_rect = pygame.Rect(12, 52, int((220*self.player.life)/self.player.max_life)-4, 20) 
        pygame.draw.rect(settings.screen, 'white', rect)
        # blinking when low life
        if self.player.life <= 30:
            if self.life_counter >= 0:
                if self.life_counter < self.life_delay:
                    self.life_counter += 1
                else: 
                    self.life_show = False
                    self.life_counter = -1
            else:
                if self.life_counter > -self.life_delay:
                    self.life_counter -= 1
                else:
                    self.life_show = True
                    self.life_counter = 1
        if self.life_show: pygame.draw.rect(settings.screen, cor, life_rect)  
        
        
    def open_map(self):
        self.cenario.fill(BACKGROUND)
        max_x = 0   # get limits of the cenario
        max_y = 0   # y = lin
        t = settings.tile
        tile_list = [settings.objects, settings.back, settings.back2, settings.items, settings.enemies,\
                        [settings.boss[0]], settings.pit_fire]
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
                        self.coins.add(obj)  
                elif idx == 4: 
                    if item == 0:   #mob 1
                        obj = Mob1()
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)
                        self.enemies.add(obj)                      
                elif idx == 5: 
                    if item == 0:   #boss
                        obj = Boss()
                        obj.rect = pygame.Rect(gx*t, gy*t, t, t)                        
                        self.enemies.add(obj)
                elif idx == 6:      # fire pit 
                    if item == 0:
                        obj = FirePit((gx*t, gy*t),t)
                        #obj.rect = pygame.Rect(gx*t, gy*t, t, t) 
                        self.fire_pit.append(obj) 
                        #self.cenario.blit(obj.image, obj.rect.topleft)
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
        
            
    def exit(self):
        # Termina o programa.
        pygame.quit()
        exit()
          

    def blit_text(self, texto, fonte, janela, x, y, delay=0, pos='topleft', cor=CORTEXTO):
        if delay > 0:             
            if self.text_count <= delay:
                self.text_count += 1           
                self.render_text(texto, fonte, janela, x, y, pos, cor)     
            else:
                self.text_count = 0
        else: self.render_text(texto, fonte, janela, x, y, pos, cor)

    
    def render_text(self, texto, fonte, janela, x, y, pos, cor):
        objTexto = fonte.render(texto, True, cor)
        rectTexto:pygame.Rect = objTexto.get_rect()
        if pos == 'topleft': rectTexto.topleft = (x, y)
        if pos == 'topright': rectTexto.topright = (x, y)
        if pos == 'center': rectTexto.center = (x, y)
        janela.blit(objTexto, rectTexto)
        
        
    def __wait_input__(self):
         # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.exit()
                    if evento.key == pygame.K_F1:
                        return
    
       
    def __menu_last__(self):        
        pygame.mixer.music.stop()
        settings.sound_lose_game.play() 
        pos = settings.disp_size
        offset = settings.font_size
        self.blit_text(f'GAME OVER', settings.fonte, settings.screen, 
                       (pos[0]/2),(pos[1]/2)-offset, pos='center') 
        self.blit_text(f'Pressione F1 para começar.', settings.fonte, settings.screen, 
                       (pos[0]/2), (pos[1]/2)+offset, pos='center') 
        self.blit_text(f'Pressione ESC para sair.', settings.fonte, settings.screen,
                       (pos[0]/2), (pos[1]/2)+offset*2, pos='center') 
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.__wait_input__()
        settings.sound_lose_game.stop()
        
        
    def __menu_win__(self):        
        pygame.mixer.music.stop()
        settings.sound_win_game.play()         
        pos = settings.disp_size
        offset = settings.font_size
        self.blit_text(f'YOU WIN!!!', settings.fonte, settings.screen, 
                       (pos[0]/2),(pos[1]/2)-offset, pos='center') 
        self.blit_text(f'Pressione F1 para começar.', settings.fonte, settings.screen, 
                       (pos[0]/2), (pos[1]/2)+offset, pos='center') 
        self.blit_text(f'Pressione ESC para sair.', settings.fonte, settings.screen,
                       (pos[0]/2), (pos[1]/2)+offset*2, pos='center')    
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.__wait_input__()
        settings.sound_win_game.stop()
    
        
   
class Basic_menu_all():
    def __init__(self, list: list[str]):        
        # rotating icon
        self.counter = 0        
        pos = [settings.disp_size[0]*0.5-200, settings.disp_size[1]*0.5]
        self.icon1 = Menu_icon(pos)
        pos = [settings.disp_size[0]*0.5+200, settings.disp_size[1]*0.5]
        self.icon2 = Menu_icon(pos)
        self.list = list
                
        self.select = 1
        self.select_max = len(list)
        
                
    def run(self):  
        pygame.mixer.music.load('Jackson/sound/Billie Jean.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.2)
        settings.somAtivado = True  
        while True:    
            select = self.check_keys()
            if select != 0:
                pygame.mixer.music.stop() 
                return select
                    
            settings.screen.fill(BACKGROUND)            
            self.draw_background_only()
            self.select_com()
            
            self.icon1.update()
            self.icon2.update()
            
            pygame.display.update()    
                
            # limitando a 60 quadros por segundo
            settings.clock.tick(settings.fps)     
      
        
    def select_com(self):
        pos = settings.disp_size
        offset = settings.font_size
        c = 0
        for item in self.list:
            self.print_text(item, (pos[0]/2),(pos[1]/2)+offset*c, 'center')
            c += 1
       
        #draw rect        
        x = settings.disp_size[0]*0.5-150
        y = settings.disp_size[1]*0.5-(int(offset/2))+(offset*(self.select-1))
        sel_rect = pygame.Rect(x,y,300,int(offset))
        pygame.draw.rect(settings.screen, 'red', sel_rect, 1)
        
        
    def check_keys(self):
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                self.exit()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.exit()  
                if evento.key == pygame.K_RETURN:
                    return self.select
                if evento.key == pygame.K_DOWN:
                    if self.select < self.select_max:
                        self.select += 1
                        self.icon1.change_pos((self.icon1.getx(),self.icon1.gety()+50))
                        self.icon2.change_pos((self.icon2.getx(),self.icon2.gety()+50))
                if evento.key == pygame.K_UP:
                    if self.select > 1:
                        self.select -= 1
                        self.icon1.change_pos((self.icon1.getx(),self.icon1.gety()-50))
                        self.icon2.change_pos((self.icon2.getx(),self.icon2.gety()-50))
                if evento.key == pygame.K_LEFT:
                    pass
                if evento.key == pygame.K_RIGHT:
                    pass
        return 0
    
    
    def print_text(self, texto, x, y, position):
        ''' Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.'''
        objTexto = settings.fonte.render(texto, True, BRANCO)
        rectTexto = objTexto.get_rect()
        if position == 'center':
            rectTexto.center = (x, y)
        elif position == 'topLeft':
            rectTexto.topleft = (x, y)
        settings.screen.blit(objTexto, rectTexto)

    def draw_background_only(self):
        ''' Preenchendo o fundo da janela com a imagem correspondente.'''      
        # movendo o fundo
        for i in range(0, settings.tiles):
            pos_y = i * settings.background.get_height() + settings.scroll
            settings.screen.blit(settings.background, (0,-pos_y))
        
        # update scroll
        settings.scroll -= 1
        if abs(settings.scroll)  > settings.background.get_height(): 
            settings.scroll = 0
         
            
    def exit(self):
        # Termina o programa.
        pygame.quit()
        exit()
       

 

class Menu_icon():
    def __init__(self,pos:list):
        self.pos = pos
        self.size = (30,30)         
                        
        self.image = settings.box[0]
        self.image = pygame.transform.scale(self.image, self.size)
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0

    def update(self):
        self.angle += 2
        self.rotate()
        settings.screen.blit(self.image, self.rect)
        #colisao debug
        #pygame.draw.rect(settings.window,settings.COLOR_TEXT,self.rect,2)

    def rotate(self):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def change_pos(self, pos:list):
        self.pos = pos
        self.rect.center = pos
    
    def getx(self):
        return self.pos[0]
    
    def gety(self):
        return self.pos[1]
    