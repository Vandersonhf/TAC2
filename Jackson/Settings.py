import pygame

BACKGROUND = (50, 100, 200)

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CORTEXTO = (255, 255, 255) # cor do texto (branca)
CORTEXTO2 = (255, 150, 50) # cor do texto (laranja)
CORTEXTO3 = (255, 0, 0) # cor do texto (vermelho)

class Settings:
    '''Configure initial settings for Jackson'''
    def setup(self, debug:bool):        
        self.debug = debug
        pygame.init()
        #self.WIDTH, self.HEIGHT = pygame.display.get_desktop_sizes()[0]
        self.WIDTH, self.HEIGHT = (700,600)
        self.disp_size = (self.WIDTH, self.HEIGHT)
        self.screen = pygame.display.set_mode(self.disp_size)
        #pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.particle_group = pygame.sprite.Group()
                
        # Configurando a fonte.        
        self.font_size = 48 
        self.fonte = pygame.font.Font(None, self.font_size)
        self.CORTEXTO = (255, 255, 255)
        
        #game globals        
        self.fps = 60
        self.base_tile = 16
        self.factor_tile = 3    #change the scale as your will :)
        self.tile = self.base_tile * self.factor_tile        
        self.map_lin = 100
        self.map_col = 300
        self.client = False
        self.server = False
        self.client_socket = None
        self.server_socket = None
        self.multiplayer = False        
        self.buffer_in = []
        self.buffer_in_max = 100
        #self.buffer_out = []
        #self.buffer_out_max = 100
        self.event_p2 = []
        self.size = 30
        self.sep = '|'
        self.client_connected = False
        
        # warp XY        
        self.warp_left = 0
        self.warp_top = 0
        
        # moving background
        self.scroll = 0
        self.tiles = 2
        
        #load resources
        self.load_images()
        self.load_sounds()
     
    
    def load_images(self):
        """loading surfaces for sprites"""   
        # objects to collide
        full = pygame.image.load('Jackson/images/bg-1-1-cutout.png').convert_alpha()
        left = [0,3235,768,832,448,464,448,464,2192,976,976,992,992,1008,1008]        
        top = [176,139,416,368,144,144,160,160,128,384,400,384,400,384,400]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.objects, self.objects_mask = self.cut_sub_surface(full, left, top, w, h, self.factor_tile)
        
        #background        
        self.background = pygame.image.load('Jackson/images/back.jpg').convert_alpha()
        self.background = pygame.transform.scale(self.background,(self.WIDTH,self.HEIGHT))
        
        # objects that not collide - background
        left = [136,152,136,151,456,455,664,680,696,257,272,1568,1584,272,287]        
        top = [16,16,32,32,16,32,160,160,160,160,160,160,160,145,160]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.back, self.back_mask = self.cut_sub_surface(full, left, top, w, h, self.factor_tile)
        
        # objects that not collide - background2
        back2 = pygame.image.load('Jackson/images/bg-trees-cutout.png').convert_alpha()
        left = [208,208,208,208]        
        top = [160,176,192,200]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.back2, self.back2_mask = self.cut_sub_surface(back2, left, top, w, h, self.factor_tile)
                
        # items
        full_items = pygame.image.load('Jackson/images/items-objects.png').convert_alpha()
        left = [0,0]
        top = [64,81]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.items, self.items_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
          
        # fire pit
        left = [96]
        top = [144]
        w = [16] * len(left)
        h = [16] * len(left)
        self.pit_fire, self.pit_fire_masks = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)  
          
        #boss fire
        left = [100,100]
        top = [128,137]
        w = [24] * len(left)
        h = [7] * len(left)
        self.boss_fire, self.boss_fire_masks = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        self.boss_fire_flip, self.boss_fire_flip_masks = self.get_flipped(self.boss_fire)  
                
        # items - coins        
        left = [0,16,32,48]
        top = [81] * len(left)
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.coin, self.coin_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
        # items - star        
        left = [0,16,32,48]
        top = [48] * len(left)
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.star, self.star_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
        # items - coin out of box
        left = [0,16,32,48]
        top = [96] * len(left)
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.coin_box, self.coin_box_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
        # items - box ?        
        left = [0,16,32,48]
        top = [64,64,64,64]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.box, self.box_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
        # items - dead brick        
        left = [64,64,64]
        top = [0,16,32]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.ex_brick, self.ex_brick_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
        # items - dead box
        full_blocks = pygame.image.load('Jackson/images/blocks.png').convert_alpha()
        left = [128]
        top = [112]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.box_empty, self.box_empty_mask = self.cut_sub_surface(full_blocks, left, top, w, h, self.factor_tile)
                       
        # get light dance
        full = pygame.image.load('Jackson/images/full-cutout.png').convert_alpha()
        left = [1609]
        top = [1704]
        w = [74]
        h = [223] 
        self.dance, self.dance_mask = self.cut_sub_surface(full, left, top, w, h, self.factor_tile/2)
        
        # dead jackson and hit
        left = [419,152,298]
        top = [799,792,792]
        w = [61,33,33]
        h = [43,48,48] 
        self.dead, self.dead_mask = self.cut_sub_surface(full, left, top, w, h, self.factor_tile/2)
        self.dead_flip, self.dead_flip_masks = self.get_flipped(self.dead)
        
        # attack - fire
        left = [262,297,358]
        top = [1105] * len(left)
        w = [30,56,56]
        h = [32] * len(w) 
        self.fire, self.fire_masks = self.cut_sub_surface(full, left, top, w, h, self.factor_tile/2)
        self.fire_flip, self.fire_flip_masks = self.get_flipped(self.fire)
        
        # orb                                   # old with all - creating orb
        left = [1081,1126,1167]                 #left = [983,1001,1027,1053,1081,1126,1167]
        top = [509,507,506]                     #top = [513,509,509,509,509,507,506]
        w = [41,37,41]                          #w = [13,22,22,24,41,37,41]
        h = [23,28,28]                          #h = [16,22,23,24,23,28,28] 
        self.orb, self.orb_masks = self.cut_sub_surface(full, left, top, w, h, self.factor_tile/2)
         
        #enemies - pallete
        enemy_all = pygame.image.load('Jackson/images/mobs-cutout.png').convert_alpha()        
        left = [238]
        top = [186] * len(left)
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.enemies, self.enemies_masks = self.cut_sub_surface(enemy_all, left, top, w, h, self.factor_tile)
        
        #enemies - 1
        #enemy_all = pygame.image.load('Jackson/images/mobs-cutout.png').convert_alpha()        
        left = [238,257]
        top = [186] * len(left)
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.enemy1, self.enemy1_masks = self.cut_sub_surface(enemy_all, left, top, w, h, self.factor_tile)
        
        #enemy1 dead
        left = [219]
        top = [186] * len(left)
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.enemy1_dead, self.enemy1_dead_masks = self.cut_sub_surface(enemy_all, left, top, w, h, self.factor_tile)
        
        # boss
        left = [257,292,327,362]
        top = [367] * len(left)
        w = [self.base_tile*2] * len(left)
        h = [self.base_tile*2] * len(left)
        self.boss_flip, self.boss_flip_masks = self.cut_sub_surface(enemy_all, left, top, w, h, self.factor_tile)
        self.boss, self.boss_masks = self.get_flipped(self.boss_flip)
                       
        player_all = pygame.image.load('Jackson/images/jackson_align-cutout.png').convert_alpha()
        #attack
        left = [1]
        top = [20] 
        w = [41] 
        h = [60] 
        self.player_atk, self.player_atk_masks = self.cut_sub_surface(player_all, left, top, w, h, self.factor_tile/2)
        self.player_atk_flip, self.player_atk_flip_masks = self.get_flipped(self.player_atk)        
        
        # walk animation - load them all just once before execution        
        left = [1+i for i in range(0,200,35)]
        top = [400] * len(left)        
        w = [32] * len(left)
        h = [60] * len(w)
        self.player_walk, self.player_walk_masks = self.cut_sub_surface(player_all, left, top, w, h, self.factor_tile/2)
        self.player_walk_flip, self.player_walk_flip_masks = self.get_flipped(self.player_walk)
        
        #jump animation        
        left = [1+i for i in range(0,100,35)]
        top = [480] * len(left)
        w = [32] * len(left)
        h = [60] * len(w)
        self.player_jump, self.player_jump_masks = self.cut_sub_surface(player_all, left, top, w, h, self.factor_tile/2)
        self.player_jump_flip, self.player_jump_flip_masks = self.get_flipped(self.player_jump)
        
        #stand animation        
        left = [1+i for i in range(0,270,35)]
        top = [560] * len(left)
        w = [32] * len(left)
        h = [60] * len(w)        
        self.player_stand, self.player_stand_masks = self.cut_sub_surface(player_all, left, top, w, h, self.factor_tile/2)
        self.player_stand_flip, self.player_stand_flip_masks = self.get_flipped(self.player_stand)
        

    def load_sounds(self):
        self.sound_fire = pygame.mixer.Sound('Jackson/sound/Uh.wav')
        self.sound_fire.set_volume(0.03)
        self.sound_life = pygame.mixer.Sound('Jackson/sound/1up.wav')
        self.sound_life.set_volume(0.2)
        self.sound_win = pygame.mixer.Sound('Jackson/sound/Wohoou.wav')
        self.sound_win.set_volume(0.2)
        self.sound_win_game = pygame.mixer.Sound('Jackson/sound/Beat It.wav')
        self.sound_win_game.set_volume(0.1)
        self.sound_lose_game = pygame.mixer.Sound('Jackson/sound/Another Part Of Me.wav')
        self.sound_lose_game.set_volume(0.1)
        self.sound_stomp = pygame.mixer.Sound('Jackson/sound/stomp.wav')
        self.sound_stomp.set_volume(0.1)
        self.sound_jump = pygame.mixer.Sound('Jackson/sound/jump.wav')
        self.sound_jump.set_volume(0.1)
        self.sound_coin = pygame.mixer.Sound('Jackson/sound/coin.wav')
        self.sound_coin.set_volume(0.3)
        self.sound_break = pygame.mixer.Sound('Jackson/sound/break.mp3')
        self.sound_break.set_volume(0.5)
        self.sound_bump = pygame.mixer.Sound('Jackson/sound/bump.wav')
        self.sound_bump.set_volume(0.3)
        self.sound_hit = pygame.mixer.Sound('Jackson/sound/Ooh.wav')
        self.sound_hit.set_volume(0.4)
        self.sound_dead = pygame.mixer.Sound('Jackson/sound/Wow.wav')
        self.sound_dead.set_volume(0.3)
        self.sound_boss_fire = pygame.mixer.Sound('Jackson/sound/firebreath.wav')
        self.sound_boss_fire.set_volume(0.3)
        self.sound_boss_dead = pygame.mixer.Sound('Jackson/sound/Uaaaaaaaaah.wav')
        self.sound_boss_dead.set_volume(0.6)
        #pygame.mixer.music.load('Jackson/sound/Smooth Criminal.wav')
        #pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.2)
        self.somAtivado = False
        self.nr_channels = pygame.mixer.get_num_channels()
        self.channel = 1  # reserving channel 0 for prioritized sounds
    
    
    def play_sound(self, sound, channel=None):
        # plays a game sound on the next channel (all channels used in order).
        # if channel not specified, sounds will be missed as sometimes all channels are busy 
        # - rotates through channels.
        if channel is None:
            ch = pygame.mixer.Channel(self.channel)
            self.channel += 1  # move to next channel
            if self.channel == self.nr_channels:
                self.channel = 1
        else:
            ch = pygame.mixer.Channel(channel)
        ch.play(sound)
        
        
    def get_flipped(self, surfaces:list):
        list = []
        mask_list = []
        for image in surfaces:
            surf = pygame.transform.flip(image, True, False)
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
    
    def cut_sub_surface(self, surface:pygame.Surface, left, top, w, h, scale, angle=0, full_screen=False):
        """faz algo..."""
        list = []
        mask_list = []
        if not (len(left) == len(top) == len(w) == len(h)):
            if self.debug: print('Subsurface empty list!!!')
            return list, mask_list      
        for i in range(len(left)):
            surf = surface.subsurface((left[i],top[i]),(w[i],h[i]))            
            surf = pygame.transform.rotozoom(surf,angle,scale)
            if full_screen:
                surf = pygame.transform.scale(surf,(self.WIDTH,self.HEIGHT))
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
    
settings = Settings()