import pygame

WIDTH = 1920
HEIGHT = 1080
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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()

        # Ocultando o cursor 
        pygame.mouse.set_visible(False)
        
        # Configurando a fonte.
        self.fonte = pygame.font.Font(None, 48)
        
        #game globals        
        
        #load resources
        self.load_images()
        self.load_sounds()
     
    
    def load_images(self):
        """loading surfaces for sprites"""                
        # cenario - clouds
        clouds = pygame.image.load('Jackson/images/bg-clouds-cutout.png').convert_alpha()
        left = [20]
        top = [288]
        w = [657]
        h = [170] 
        self.sky1, self.sky1_mask = self.cut_sub_surface(clouds, left, top, w, h, 2, full_screen=True)
        
        # boxes
        self.box = pygame.image.load('Jackson/images/box.jpg').convert_alpha()
        self.box_mask = pygame.mask.from_surface(self.box)
        
        # get light dance
        full = pygame.image.load('Jackson/images/full-cutout.png').convert_alpha()
        left = [1609]
        top = [1704]
        w = [74]
        h = [223] 
        self.dance, self.dance_mask = self.cut_sub_surface(full, left, top, w, h, 2)
        
        #attack - fire
        left = [262,297,358]
        top = [1105] * len(left)
        w = [30,56,56]
        h = [32] * len(w) 
        self.fire, self.fire_masks = self.cut_sub_surface(full, left, top, w, h, 2)
        self.fire_flip, self.fire_flip_masks = self.get_flipped(self.fire)
        
        #enemies
        enemy_all = pygame.image.load('Jackson/images/mobs-cutout.png').convert_alpha()        
        left = [238,257,219]
        top = [186] * len(left)
        w = [16] * len(left)
        h = [16] * len(left)
        self.enemy1, self.enemy1_masks = self.cut_sub_surface(enemy_all, left, top, w, h, 3)
        
        player_all = pygame.image.load('Jackson/images/jackson_align-cutout.png').convert_alpha()
        #attack
        left = [1]
        top = [20] 
        w = [41] 
        h = [60] 
        self.player_atk, self.player_atk_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_atk_flip, self.player_atk_flip_masks = self.get_flipped(self.player_atk)        
        
        # walk animation - load them all just once before execution        
        left = [1+i for i in range(0,200,35)]
        top = [400] * len(left)        
        w = [32] * len(left)
        h = [60] * len(w)
        self.player_walk, self.player_walk_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_walk_flip, self.player_walk_flip_masks = self.get_flipped(self.player_walk)
        
        #jump animation        
        left = [1+i for i in range(0,100,35)]
        top = [480] * len(left)
        w = [32] * len(left)
        h = [60] * len(w)
        self.player_jump, self.player_jump_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_jump_flip, self.player_jump_flip_masks = self.get_flipped(self.player_jump)
        
        #stand animation        
        left = [1+i for i in range(0,270,35)]
        top = [560] * len(left)
        w = [32] * len(left)
        h = [60] * len(w)        
        self.player_stand, self.player_stand_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_stand_flip, self.player_stand_flip_masks = self.get_flipped(self.player_stand)
        

    def load_sounds(self):
         # configurando o som
        self.sound_fire = pygame.mixer.Sound('Jackson/sound/Uh.wav')
        self.sound_fire.set_volume(0.1)
        pygame.mixer.music.load('Jackson/sound/Smooth Criminal.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.4)
        self.somAtivado = True
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
                surf = pygame.transform.scale(surf,(WIDTH,HEIGHT))
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
    
settings = Settings()