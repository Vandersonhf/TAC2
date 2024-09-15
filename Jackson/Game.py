import pygame
from .Settings import *
from .Player import Player
from .Objects import Box
from .Enemy import Enemy1

class Jackson():    
    def play(self, debug:bool):  
        settings.setup(debug)
        player = Player(WIDTH*0.1, HEIGHT*0.7)

        # cenario creation - sprites
        boxes = pygame.sprite.Group()        
        box = Box(0, HEIGHT)
        boxes.add(box)
        for i in range(7):            
            box = Box(box.size[0]*i, HEIGHT)
            boxes.add(box)
        
        box = Box(0, HEIGHT-box.size[1]*2)
        boxes.add(box)
        box = Box(box.size[0]*6, HEIGHT-box.size[1])
        boxes.add(box)
        
        enemies = pygame.sprite.Group()        
        enemies.add(Enemy1(WIDTH*0.5,HEIGHT-box.size[1]))
        
        # main game loop
        while True:
            pygame.event.pump()

            # Draw loop            
            settings.screen.fill(BACKGROUND) 
            settings.screen.blit(settings.sky1[0], (0, 0))
            
            # update elements in memory
            player.update(boxes, enemies)
            boxes.update()
            enemies.update()
                      
            #draw elements           
            if settings.debug:
                for enemy in enemies:
                    enemy.draw(settings.screen)
                for box in boxes:
                    box.draw(settings.screen)
            else:
                boxes.draw(settings.screen)
                enemies.draw(settings.screen)            
            player.draw(settings.screen)
            
            #update screen
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
    