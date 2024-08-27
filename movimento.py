import pygame, time
import math

# Defnindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Definindo PI
#PI = 3.1416
PI = math.pi

# definindo outras constantes do jogo
LARGURAJANELA = 800
ALTURAJANELA = 600


# definindo a função mover()
def mover(figura, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    if figura['objRect'].top < borda_superior or figura['objRect'].bottom > borda_inferior:
        # figura atingiu o topo ou a base da janela
        figura['vel'][1] = -figura['vel'][1]
    if figura['objRect'].left < borda_esquerda or figura['objRect'].right > borda_direita:
        # figura atingiu o lado esquerdo ou direito da janela
        figura['vel'][0] = -figura['vel'][0]
    figura['objRect'].x += figura['vel'][0]
    figura['objRect'].y += figura['vel'][1]


# Inicializando módulos de Pygame
pygame.init()

# criando um objeto pygame.time.Clock
#relogio = pygame.time.Clock()

# Criando uma janela com o título “Olá, mundo!”
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('GAME')

# criando as figuras
f1 = {'objRect': pygame.Rect(300, 80, 40, 80), 'cor': VERMELHO, 'vel': [0,-5], 'forma': 'ELIPSE'}
f2 = {'objRect': pygame.Rect(200, 200, 20, 20), 'cor': VERDE, 'vel': [5,5], 'forma': 'ELIPSE'}
f3 = {'objRect': pygame.Rect(100, 150, 60, 60), 'cor': AZUL, 'vel': [-5,5], 'forma': 'RETANGULO'}
f4 = {'objRect': pygame.Rect(200, 150, 80, 40), 'cor': AMARELO, 'vel': [5,0], 'forma': 'RETANGULO'}
figuras = [f1, f2, f3, f4]


'''
# Preenchendo o fundo da janela com a cor branca
janela.fill(PRETO)
# Trabalhando com texto
fonte = pygame.font.Font(None, 48)
texto = fonte.render('START GAME', True, BRANCO)
janela.blit(texto, [300, 150])
texto = fonte.render('MULTIPLAYER', True, BRANCO)
janela.blit(texto, [300, 200])
texto = fonte.render('OPTIONS', True, BRANCO)
janela.blit(texto, [300, 250])
texto = fonte.render('QUIT', True, BRANCO)
janela.blit(texto, [300, 300])

# selecionar opcao
pygame.draw.rect(janela, VERDE, (295, 145, 250, 40), 1)

# Desenhando figuras
pygame.draw.line(janela, VERDE, (60, 260), (420, 260), 4)
pygame.draw.polygon(janela, PRETO, ((191, 206), (236, 277), (156, 277)),0)
pygame.draw.circle(janela, AZUL, (110, 40), 20, 0)
pygame.draw.ellipse(janela, VERMELHO, (400, 250, 40, 80), 1)
pygame.draw.rect(janela, VERDE, (20, 20, 60, 40), 0)
pygame.draw.arc(janela, VERMELHO, [250, 75, 150, 125], PI/2, 3*PI/2, 2)
pygame.draw.arc(janela, PRETO, [250, 75, 150, 125], -PI/2, PI/2, 2)
'''
# mostrando na tela tudo o que foi desenhado
#pygame.display.update()


deve_continuar = True
x = 110 
# Loop do jogo
while deve_continuar:
    # Checando eventos
    for event in pygame.event.get():
        # Se for um evento QUIT
        if event.type == pygame.QUIT:
            deve_continuar = False
            print("SAINDO...")
        #if event.type == pygame.K_SPACE:
        #    print("espaco..")
    
    # preenchendo o fundo com a cor preta
    janela.fill(PRETO)

    for figura in figuras:
        # reposicionando a figura
        mover(figura,(LARGURAJANELA, ALTURAJANELA))
        # desenhando a figura na janela
        if figura['forma'] == 'RETANGULO':
            pygame.draw.rect(janela, figura['cor'], figura['objRect'])
        elif figura['forma'] == 'ELIPSE':
            pygame.draw.ellipse(janela, figura['cor'], figura['objRect'])
    
    # atualizando na tela tudo o que foi desenhado
    pygame.display.update()
    # esperando 0.02 segundos
    time.sleep(0.02)

# Encerrando módulos de Pygame
pygame.quit()