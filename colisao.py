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
relogio = pygame.time.Clock()

# Criando uma janela com o título “Olá, mundo!”
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('GAME')

# criando os blocos e colocando-os em uma lista
b1 = {'objRect': pygame.Rect(375, 80, 40, 40), 'cor': VERMELHO, 'vel': [0,2]}
b2 = {'objRect': pygame.Rect(175, 200, 40, 40), 'cor': VERDE, 'vel': [0,-3]}
b3 = {'objRect': pygame.Rect(275, 150, 40, 40), 'cor': AMARELO, 'vel': [0,-1]}
b4 = {'objRect': pygame.Rect(75, 150, 40, 40), 'cor': AZUL, 'vel': [0,4]}
blocos = [b1, b2, b3, b4]

# criando a bola
bola = {'objRect': pygame.Rect(270, 330, 30, 30), 'cor': BRANCO, 'vel': [3,3]}

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

    for bloco in blocos:
        # reposicionando o bloco
        mover(bloco, (LARGURAJANELA,ALTURAJANELA))
        # desenhando o bloco na janela
        pygame.draw.rect(janela, bloco['cor'], bloco['objRect'])
        # mudando a cor da bola caso colida com algum bloco
        mudarCor = bola['objRect'].colliderect(bloco['objRect'])
        if mudarCor:
            bola['cor'] = bloco['cor']
            bola['vel'][0] = -bola['vel'][0]
            bola['vel'][1] = -bola['vel'][1]
            bloco['vel'][0] = -bloco['vel'][0]
            bloco['vel'][1] = -bloco['vel'][1]

    # reposicionando e desenha a bola
    mover(bola, (LARGURAJANELA, ALTURAJANELA))
    pygame.draw.ellipse(janela, bola['cor'], bola['objRect'])
    # mostrando na tela tudo o que foi desenhado
    pygame.display.update()
    # limitando a 60 quadros por segundo
    relogio.tick(60)

# Encerrando módulos de Pygame
pygame.quit()