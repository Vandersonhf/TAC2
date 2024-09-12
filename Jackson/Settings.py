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
        # carregando imagens
        imagemFundo = pygame.image.load('Jackson/images/cenario.jpg').convert_alpha()
        self.imagemFundo = pygame.transform.scale(imagemFundo,(WIDTH, HEIGHT))
        
        self.box = pygame.image.load('Jackson/images/box.jpg').convert_alpha()
        self.box_mask = pygame.mask.from_surface(self.box)
        
        enemy_all = pygame.image.load('Jackson/images/mobs-cutout.png').convert_alpha()        
        left = [238]
        top = [186]
        w = [16]
        h = [16] 
        self.enemy1, self.enemy1_masks = self.cut_sub_surface(enemy_all, left, top, w, h, 3)
        
        player_all = pygame.image.load('Jackson/images/sprites1.png').convert_alpha()
        # walk animation - load them all just once before execution
        left = [58,73,92,107,128,147,162,180,199,215,230,251]
        top = [1] * len(left)
        w = [14,18,14,20,17,14,17,18,15,14,20,17]
        h = [47] * len(w)
        self.player_walk, self.player_walk_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_walk_flip, self.player_walk_flip_masks = self.get_flipped(self.player_walk)
          
        #jump animation
        left = [58,83,106]
        top = [98] * len(left)
        w = [22,22,20]
        h = [45] * len(w)
        self.player_jump, self.player_jump_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_jump_flip, self.player_jump_flip_masks = self.get_flipped(self.player_jump)
        
        #stand animation
        left = [19,86,106,124,141,163,181]
        top = [334,154,151,152,152,153,144] 
        w = [15,19,17,16,18,17,25]
        h = [48,44,47,46,46,45,54] 
        self.player_stand, self.player_stand_masks = self.cut_sub_surface(player_all, left, top, w, h, 2)
        self.player_stand_flip, self.player_stand_flip_masks = self.get_flipped(self.player_stand)

        #imagemRaio = pygame.image.load('raio.png')
        #imagemRaio = pygame.transform.rotate(imagemRaio,90)
        #imagemRaio = pygame.transform.scale(imagemRaio,(50,10))


    def load_sounds(self):
         # configurando o som
        self.somRaio = pygame.mixer.Sound('Jackson/sound/laser1.mp3')
        self.somRaio.set_volume(0.2)
        pygame.mixer.music.load('Jackson/sound/simplicity.ogg')
        #pygame.mixer.music.play(-1, 0.0)
        self.somAtivado = True
    
    
    def get_flipped(self, surfaces:list):
        list = []
        mask_list = []
        for image in surfaces:
            surf = pygame.transform.flip(image, True, False)
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
    def cut_sub_surface(self, surface:pygame.Surface, left, top, w, h, scale):
        list = []
        mask_list = []
        if not (len(left) == len(top) == len(w) == len(h)):
            if self.debug: print('Subsurface empty list!!!')
            return list
        for i in range(len(left)):
            surf = surface.subsurface((left[i],top[i]),(w[i],h[i]))
            surf = pygame.transform.rotozoom(surf,0,scale)
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
    
settings = Settings()