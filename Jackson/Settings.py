import pygame

#WIDTH = 800
#HEIGHT = 600
BACKGROUND = (50, 100, 200)

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CORTEXTO = (255, 255, 255) # cor do texto (branca)

class Settings:
    '''Configure initial settings for Jackson'''
    def setup(self, debug:bool):        
        self.debug = debug
        pygame.init()
        self.WIDTH, self.HEIGHT = pygame.display.get_desktop_sizes()[0]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
                
        # Configurando a fonte.
        self.fonte = pygame.font.Font(None, 48)
        
        #game globals        
        self.fps = 60
        self.base_tile = 16
        self.factor_tile = 3    #change the scale as your will :)
        self.tile = self.base_tile * self.factor_tile        
        self.map_lin = 100
        self.map_col = 300
        
        #load resources
        self.load_images()
        self.load_sounds()
     
    
    def load_images(self):
        """loading surfaces for sprites"""   
        # objects to collide
        full = pygame.image.load('Jackson/images/bg-1-1-cutout.png').convert_alpha()
        left = [0,320,768,832,448,464,448,464,2192,976,976,992,992,1008,1008]        
        top = [176,112,416,368,144,144,160,160,112,384,400,384,400,384,400]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.objects, self.objects_mask = self.cut_sub_surface(full, left, top, w, h, self.factor_tile)
        
        # objects that not collide - background
        left = [136,152,136,152,456,456,664,680,696,256,272,1568,1584,272,288]        
        top = [16,16,32,32,16,32,160,160,160,160,160,160,160,144,160]
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
                
        # items - coins        
        left = [0,16,32,48]
        top = [96,96,96,96]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.coin, self.coin_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
        # items - box ?        
        left = [0,16,32,48]
        top = [64,64,64,64]
        w = [self.base_tile] * len(left)
        h = [self.base_tile] * len(left)
        self.box, self.box_mask = self.cut_sub_surface(full_items, left, top, w, h, self.factor_tile)
        
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
        
        #attack - fire
        left = [262,297,358]
        top = [1105] * len(left)
        w = [30,56,56]
        h = [32] * len(w) 
        self.fire, self.fire_masks = self.cut_sub_surface(full, left, top, w, h, self.factor_tile/2)
        self.fire_flip, self.fire_flip_masks = self.get_flipped(self.fire)
        
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
        self.sound_fire.set_volume(0.1)
        self.sound_stomp = pygame.mixer.Sound('Jackson/sound/stomp.wav')
        self.sound_stomp.set_volume(0.1)
        self.sound_jump = pygame.mixer.Sound('Jackson/sound/jump.wav')
        self.sound_jump.set_volume(0.1)
        self.sound_coin = pygame.mixer.Sound('Jackson/sound/coin.wav')
        self.sound_coin.set_volume(0.3)
        self.sound_bump = pygame.mixer.Sound('Jackson/sound/bump.wav')
        self.sound_bump.set_volume(0.3)
        pygame.mixer.music.load('Jackson/sound/Smooth Criminal.wav')
        #pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.3)
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