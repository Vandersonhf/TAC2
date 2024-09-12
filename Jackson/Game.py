import pygame
from .Settings import *
from .Player import Player
from .Objects import Box
from .Enemy import Enemy1

class Jackson():    
    def play(self, debug:bool):  
        settings.setup(debug)
        player = Player(WIDTH*0.1, HEIGHT*0.7)

        boxes = pygame.sprite.Group()        
        box = Box(0, HEIGHT)
        boxes.add(box)
        for i in range(6):            
            box = Box(box.size[0]*i, HEIGHT)
            boxes.add(box)
        
        enemies = pygame.sprite.Group()        
        enemies.add(Enemy1(WIDTH*0.5,HEIGHT-box.size[1]))
        
        while True:
            pygame.event.pump()
            player.update(boxes, enemies)

            # Draw loop            
            #settings.screen.blit(settings.imagemFundo, (0, 0))
            settings.screen.fill(BACKGROUND)           
            player.draw(settings.screen)
            boxes.draw(settings.screen)
            #enemies.draw(settings.screen)
            for enemy in enemies:
                enemy.draw(settings.screen)
            
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
    