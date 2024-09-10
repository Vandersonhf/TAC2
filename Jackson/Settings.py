import pygame

WIDTH = 1920
HEIGHT = 1080
#BACKGROUND = (0, 0, 0)
#background_image = 'images/cenario.jpg'
#game_images = {}
move_delay = 7


# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CORTEXTO = (255, 255, 255) # cor do texto (branca)

class Settings:
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()

        # Ocultando o cursor e redimensionando a imagem de fundo.
        pygame.mouse.set_visible(False)

        # carregando imagens
        imagemFundo = pygame.image.load('Jackson/images/cenario.jpg')
        self.imagemFundo = pygame.transform.scale(imagemFundo,(WIDTH, HEIGHT))

        #imagemRaio = pygame.image.load('raio.png')
        #imagemRaio = pygame.transform.rotate(imagemRaio,90)
        #imagemRaio = pygame.transform.scale(imagemRaio,(50,10))


        # Configurando a fonte.
        self.fonte = pygame.font.Font(None, 48)

        # configurando o som
        self.somRaio = pygame.mixer.Sound('Jackson/sound/laser1.mp3')
        self.somRaio.set_volume(0.2)
        pygame.mixer.music.load('Jackson/sound/simplicity.ogg')
        #pygame.mixer.music.play(-1, 0.0)
        self.somAtivado = True