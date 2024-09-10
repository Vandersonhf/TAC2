import pygame
from .Settings import *
from .Player import Player
from .Objects import Box

class Jackson():    
    def play(self):   
        settings = Settings()
        settings.setup()
        player = Player(300, 200)

        boxes = pygame.sprite.Group()        

        boxes.add(Box(200, 600))
        boxes.add(Box(500, 600))
        
        while True:
            pygame.event.pump()
            player.update(boxes)

            # Draw loop            
            settings.screen.blit(settings.imagemFundo, (0, 0))
            player.draw(settings.screen)
            boxes.draw(settings.screen)
            
            pygame.display.flip()
            settings.clock.tick(60)
            
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

    def colocarTexto(self, texto, fonte, janela, x, y):
        # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
        objTexto = fonte.render(texto, True, CORTEXTO)
        rectTexto = objTexto.get_rect()
        rectTexto.topleft = (x, y)
        janela.blit(objTexto, rectTexto)
    