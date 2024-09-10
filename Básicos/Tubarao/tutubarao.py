import pygame, random

# Inicializando módulos de Pygame
pygame.init()

# criando um objeto pygame.time.Clock
relogio = pygame.time.Clock()

# carregando imagens
imagemTubarao = pygame.image.load('tubarao2.png')
imagemTubarao = pygame.transform.scale(imagemTubarao,(150,70))
imagemInimigo = pygame.image.load('tubarao.png')
imagemInimigo = pygame.transform.scale(imagemInimigo,(150,70))
imagemInimigo = pygame.transform.flip(imagemInimigo,True, False)
imagemPeixe = pygame.image.load('peixe.png')
imagemPeixe = pygame.transform.scale(imagemPeixe,(70,50))
imagemPeixe = pygame.transform.flip(imagemPeixe,True, False)
imagemFundo = pygame.image.load('fundo.jpg')
imagemRaio = pygame.image.load('raio.png')
imagemRaio = pygame.transform.rotate(imagemRaio,90)
imagemRaio = pygame.transform.scale(imagemRaio,(50,10))


# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CORTEXTO = (255, 255, 255) # cor do texto (branca)

# definindo algumas constantes
LARGURAJANELA = imagemFundo.get_width()
ALTURAJANELA = imagemFundo.get_height()
LARGURAPEIXE = imagemPeixe.get_width()
ALTURAPEIXE = imagemPeixe.get_height()
LARGURATUBARAO = imagemTubarao.get_width()
ALTURATUBARAO = imagemTubarao.get_height()
LARGURARAIO = imagemRaio.get_width()
ALTURARAIO = imagemRaio.get_height()
VEL = 6
ITERACOES = 30
VELRAIO = -15 # velocidade do raio

# Criando uma janela com o título “Olá, mundo!”
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('GAME')

# carregando imagens
imagemTubarao = imagemTubarao.convert_alpha()
imagemPeixe = imagemPeixe.convert_alpha()
imagemFundo = imagemFundo.convert_alpha()


# definindo a função moverJogador(), que registra a posição do jogador
def moverJogador(jogador, teclas, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    if teclas['esquerda'] and jogador['objRect'].left > borda_esquerda:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita'] and jogador['objRect'].right < borda_direita:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima'] and jogador['objRect'].top > borda_superior:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo'] and jogador['objRect'].bottom < borda_inferior:
        jogador['objRect'].y += jogador['vel']

# definindo a função moverPeixe(), que registra a posição do peixe
def moverElemento(peixe):
    peixe['objRect'].x += peixe['vel']
    
def terminar():
    # Termina o programa.
    pygame.quit()
    exit()
    
def aguardarEntrada():
    # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                return

def colocarTexto(texto, fonte, janela, x, y):
    # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)
    

# Ocultando o cursor e redimensionando a imagem de fundo.
pygame.mouse.set_visible(False)
imagemFundoRedim = pygame.transform.scale(imagemFundo,(LARGURAJANELA, ALTURAJANELA))

# Configurando a fonte.
fonte = pygame.font.Font(None, 48)

# configurando o som
somComer = pygame.mixer.Sound('comer.mp3')
somTiro = pygame.mixer.Sound('laser1.mp3')
somTiro.set_volume(0.2)
pygame.mixer.music.load('space.mp3')
#pygame.mixer.music.play(-1, 0.0)
somAtivado = True
 
# Tela de inicio.
colocarTexto('Tutubarão', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURAJANELA / 20 , ALTURAJANELA / 2)
pygame.display.update()
aguardarEntrada()

recorde = 0
while True:
    # Configurando o começo do jogo.
    peixes = [] # lista com os peixes
    inimigos = [] # lista com os peixes
    raios = [] # lista com os raios
    pontuacao = 0 # pontuação
    deve_continuar = True # indica se o loop do jogo deve continuar
    
    # direções de movimentação
    # definindo o dicionario que guardará as direcoes pressionadas
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    contador = 0 # contador de iterações
    pygame.mixer.music.play(-1, 0.0) # colocando a música de fundo
    # criando jogador
    jogador = {'objRect': pygame.Rect(300, 100, LARGURATUBARAO,ALTURATUBARAO), 'imagem': imagemTubarao, 'vel': VEL}

    # Loop do jogo
    while deve_continuar:
        # Checando eventos
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                terminar()
            # quando uma tecla é pressionada
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_m:
                    if somAtivado:
                        pygame.mixer.music.stop()
                        somAtivado = False
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        somAtivado = True
                if evento.key == pygame.K_SPACE:
                    raio = {'objRect': pygame.Rect(jogador['objRect'].left-5, jogador['objRect'].top+5,
                                                   LARGURARAIO, ALTURARAIO),
                    'imagem': imagemRaio,
                    'vel': VELRAIO}
                    raios.append(raio)
                    somTiro.play()
            # quando uma tecla é solta
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = False
            # quando um botao do mouse é pressionado
            #if evento.type == pygame.MOUSEBUTTONDOWN:
            #    peixes.append({'objRect': pygame.Rect(evento.pos[0], evento.pos[1],
            #                        LARGURAPEIXE, ALTURAPEIXE), 'imagem': imagemPeixe, 'vel': VEL - 3})    
        
        contador += 1
        if contador >= ITERACOES:
            # adicionando um novo peixe
            contador = 0
            posY = random.randint(0, ALTURAJANELA - ALTURAPEIXE)
            posX = -LARGURAPEIXE
            velRandom = random.randint(VEL - 3, VEL + 3)
            tipo = random.randint(0,1)
            if tipo: peixes.append({'objRect': pygame.Rect(posX, posY,LARGURAPEIXE,ALTURAPEIXE),                                
                        'imagem': imagemPeixe, 'vel': velRandom})
            else: inimigos.append({'objRect': pygame.Rect(posX, posY,LARGURATUBARAO,ALTURATUBARAO),                                
                        'imagem': imagemInimigo, 'vel': velRandom})
                
        # preenchendo o fundo de janela com a sua imagem
        janela.blit(imagemFundo, (0,0))
        
        # Colocando as pontuações.
        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)

        # movendo o jogador
        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))        
        # desenhando jogador
        janela.blit(jogador['imagem'], jogador['objRect'])
        
        # checando se jogador comeu algum peixe ou se o peixe saiu da janela para retirá-lo da lista
        for peixe in peixes[:]:
            comeu = jogador['objRect'].colliderect(peixe['objRect'])
            if comeu and somAtivado:
                somComer.play()
            if comeu or peixe['objRect'].x > LARGURAJANELA:
                peixes.remove(peixe)
                if comeu: pontuacao += 50
            for raio in raios[:]:
                raioColidiu = raio['objRect'].colliderect(peixe['objRect'])
                if raioColidiu:
                    raios.remove(raio)
                    peixes.remove(peixe)
                    pontuacao += 50
        
        # checando se jogador comeu algum peixe ou se o peixe saiu da janela para retirá-lo da lista
        for inimigo in inimigos:
            morreu = jogador['objRect'].colliderect(inimigo['objRect'])
            if morreu:
                deve_continuar = False 
            for raio in raios[:]:
                raioColidiu = raio['objRect'].colliderect(inimigo['objRect'])
                if raioColidiu:
                    raios.remove(raio)
                    inimigos.remove(inimigo)
                    pontuacao += 100
        
        # movendo e desenhando os peixes
        for peixe in peixes:
            moverElemento(peixe)
            janela.blit(peixe['imagem'], peixe['objRect'])
        
        # movendo e desenhando os inimigos
        for inimigo in inimigos:
            moverElemento(inimigo)
            janela.blit(inimigo['imagem'], inimigo['objRect'])
            
        # Movimentando e desenhando os raios.
        for raio in raios:
            moverElemento(raio)
            janela.blit(raio['imagem'], raio['objRect'])
            
        #Eliminando os raios que passam pelo topo da janela.
        for raio in raios[:]:            
            direita_raio = raio['objRect'].right
            if direita_raio < 0:
                raios.remove(raio)

        # mostrando na tela tudo o que foi desenhado
        pygame.display.update()
        # limitando a 60 quadros por segundo
        relogio.tick(60)
    
    # Parando o jogo e mostrando a tela final.
    pygame.mixer.music.stop()    
    colocarTexto('GAME OVER', fonte, janela, (LARGURAJANELA / 3), (ALTURAJANELA / 3))
    colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (LARGURAJANELA / 10), (ALTURAJANELA / 2))
    pygame.display.update()
    # Aguardando entrada por teclado para reiniciar o jogo ou sair.
    aguardarEntrada()

