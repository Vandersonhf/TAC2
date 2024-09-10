#!/usr/bin/python
# -*- coding: cp1252 -*-
# Invasores
# Escrito por: Nilo Menezes (nilo at nilo dot pro dot br)
# Data: 21 de Setembro de 2003
# Vers�o 0.5 - 22/09/2003
#               Funcionamento b�sico
# Vers�o 0.6 - 23/09/2003
#               Ajuste e coment�rios
#               Adi��o de som
#               Melhoria das rotinas de impres�o
#               Bugs de fechamento corrigidos
#               Tratamento de eventos melhorados
# Vers�o 0.7 - 24/09/2003
#               Melhoria nos gr�ficos
#               Acentua��o do texto: contribui��o de Lu�s Braga (SciTE)
#               Imagem de t�tulo e fim feitas no GIMP
#               Novos gr�ficos
#               Recarga de M�sseis
#               Recarga de Resist�ncia
#               Nivel de dificuldade progressivo (mais inimigos a cada segundo a cada 10 segundos) :-)
#               Redutor de tiro (s� se dispara uma vez a cada 3 frames ou 1/10 s
# Vers�o 0.8 -  12/04/2004
#               Suporte � Joystick (aceleracao fixa)
#               Suporte � Mouse (aceleracao variavel - max 15)
#               ESC sai
#               M misses (+1000)
#               R resistencia (+1000)
# Vers�o 0.9 - 05/03/2005
#               # Fazendo # Limpeza no c�digo
#               # Fazendo # Isolamento da SDL em classes especificas
#               Divis�o das classes em v�rios arquivos
#               # Fazendo # Classe de recursos (som e imagem)
#               Corre��o do bug de Joystick [1157541]
#               Corre��o do bug de Som (para micros sem som) [1157542]
#               Corre��o de erro de path no Linux [1157558]
#               * - Alterna FullScreen
#               + - Pr�ximo modo de v�deo
#               - - Modo de v�deo anterior
#               Estrelas cintilantes
# Versao 0.9.1 - 12/11/2006
#              Controlador de jogo implementado
#              Resolvido bug de controle com mouse
#              Melhor jogabilidade
#              Resolvido bug ao iniciar nova partida
#              Primeiros testes com traducao
#              Implemena�ao basica de fases
# Versao 0.9.2 - 17/11/2006
#              Adicionado espanhol e franc�s a lista de tradu�ao


# TODO: limpar o c�digo
# TODO: reprojetar a engine de controle
# TODO: introduzir variabilidade de movimentos nos aliens
# TODO: criar telas de configura��o
# TODO: n�veis de dificuldade (fases)
# TODO: high score
# TODO: campo de for�a
# TODO: novas armas
# TODO: novos inimigos - boss

#   This file is part of Invasores.
#
#   Invasores is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   Invasores is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Invasores; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# M�dulos do PyGame

import pygame

import pygame.joystick
#import pygame.mixer
from pygame.locals import *

# M�dulos do Python


# M�dulos do jogo
from universo import *
from objetodojogo import *
from nave import *
from objetosbonus import *
from laser import *
from alienigena import *
from score import *

import traducao

import video
import som
import naleatorios

class Invasores:
    """
        Classe Invasores
        ----------------
        Esta classe � responsavel pelo jogo em si.
        Toda customizacao deve ser feita aqui
    """
    def __init__(self, tela):
        self.tamanho = tela
        self.eventos = {}
        self.comandos = {}
        self.universo = Universo(tela)
        self.video = self.universo.video
        self.carregue_imagens()
        self.sair=None
        self.frame = 0
        self.ultimo_tiro = 0
        self.jogador = Nave("Nave", [400,400], self.iJogador)
        self.placar = Score("Placar", [0,0])
        #self.placar = Score("Placar", [0,0])
        self.placar.jogador = self.jogador
        self.universo.quadros = 30
        self.universo.calcule_pontos = self.calcula_pontos
        self.video.titulo("Invasores")
        self.fases = ( self.fase1, self.fase2)
        #self.fases = ( self.faseT, self.faseT)
        self.nova_partida()


        try:
            pygame.joystick.init()
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except:
            pass
        self.sensibilidade_mouse = 2
        self.inicializa_eventos()
        self.inicializa_comandos()

    def carregue_imagens(self):
        self.iJogador = video.carregue("NAVE", "nave2.bmp")
        self.iMissil = video.carregue("TIRO", "laser.png")
        self.iInimigo = video.carregue("INIMIGO", "inimigo2.bmp")
        self.iCaixaDeMisseis = video.carregue("CMISSIL", "caixademisseis.png")
        self.iCaixaDeResistencia = video.carregue("CRESITENCIA","caixaderesistencia.png")
        self.logo = video.Imagem("LOGO","Invasoreslogo.png")
        self.logo.ponto_croma(0,0)
        self.fim_de_jogo = video.Imagem("FIMDEJOGO","fimdejogo.png")
        self.fim_de_jogo.ponto_croma(0,0)




    def mostra_texto(self, ttexto):
        texto = Texto("Texto", [-1,-1], ttexto, 80, 90, self.universo, (255,0,0))
        texto.respire()
        self.universo.adicione(texto)

    def fase1(self):
        self.script=[ [0, """self.mostra_texto("fase1") """],
                              [100, "self.cria_alienigena(100,50, 8, 3, [(3,0,120),(-3,1,120),(3,0,120),(-3,2,120)] )"],
                              [250, "self.cria_municao()"],
                              [300, "self.cria_alienigena(100,50, 10, 2, [(3,0,120),(-3,1,120),(3,0,120),(-3,2,120)] )"],
                              [450, "self.cria_municao()"],
                              [500, "self.cria_alienigena(100,50, 10, 4, [(4,0,120),(-4,1,120),(4,0,120),(-4,2,120)] )"],
                              [700, "self.cria_resistencia()"],
                              [720, "self.cria_municao()"],
                              [800, "self.cria_alienigena(100,50, 12, 4, [(5,0,120),(-5,1,120),(5,0,120),(-5,2,120)] )" ],
                              [810, "self.cria_municao()"],
                              [850, "self.cria_municao()"],
                              [900, ""] ]

    def fase2(self):
        self.script=[ [0, """self.mostra_texto("fase2")"""],
                              [100, "self.cria_alienigena(100,100, 6, 4, [(5,3,120),(-3,1,120),(3,-1,120),(-5,-2,120)] )"],
                              [250, "self.cria_municao()"],
                              [300, "self.cria_alienigena(100,100, 8, 6, [(5,0,120),(-3,1,120),(3,0,120),(-5,2,120)] )"],
                              [450, "self.cria_municao()"],
                              [600, "self.cria_alienigena(100,100, 8, 6, [(4,0,120),(-4,1,120),(4,0,120),(-4,2,120)] )"],
                              [700, "self.cria_resistencia()"],
                              [900, "self.cria_alienigena(100,100, 10, 6, [(6,0,120),(-6,1,120),(6,0,120),(-6,2,120)] )" ],
                              [1200,"""self.mostra_texto("venceu")"""],
                              [1500,"self.saida()"]]


    def faseT(self):
        self.script=[ [0, """self.mostra_texto("fase1") """],
                      [5,"""self.faseTCriaalienigena()"""],
                      [200,"""self.faseTCriaalienigena()"""],
                      [400,"""self.faseTCriaalienigena()"""],
                      [1400, "self.saida()"]      ]

    def cria_alienigena(self,xi,yi,c,l,script,xl=60, yl=60):

        for y in range(l):
            for x in range(c):
                a = Alienigena("Inimigo", [xi+x*xl,yi+y*yl], self.iInimigo)
                a.set_script( [(5,0,120),(-5,1,120),(5,0,120),(-5,2,120)])
                self.universo.adicione(a)



    def controle_joystick(self):
        pass

    def controle_mouse(self):
        pass

    def controle_teclado(self):
        pass

    def nova_partida(self):
        self.jogador.resistencia = 300
        self.jogador.misseis = 300
        self.jogador.pos = [400,400]
        self.jogador.ix = 0
        self.jogador.iy = 0
        self.universo.score=0
        self.universo.objetos=[]
        self.universo.colisoes={}
        self.universo.adicione(self.jogador)
        self.universo.adicione(self.placar)
        self.placar.respire()
        self.fase=0
        self.frame=0

    def calcula_pontos(universo, a, b):
        if a.nome != b.nome:
            a.colida(b)
            b.colida(a)
            return a.valor + b.valor
        else:
            return 0


    #def carregue_imagem(self,nome):
    #   return pygame.image.load(nome).convert()

    def atira(self, evento = None):
        #print "M: %d F:%d UT: %d" % (self.jogador.misseis, self.frame, self.ultimo_tiro)
        if self.jogador.misseis > 0 and self.frame - self.ultimo_tiro >=5:
            self.universo.adicione(Laser("tiro",
                                    [self.jogador.pos[0]+5,
                                self.jogador.pos[1]-30], self.iMissil))
            self.universo.adicione(Laser("tiro",
                                    [self.jogador.pos[0]+self.jogador.lx-15,
                                    self.jogador.pos[1]-30], self.iMissil))
            self.jogador.misseis -=2
            self.ultimo_tiro = self.frame


##    def cria_alienigena(self, tipo = 0):
##        if tipo == 0:
##            self.universo.adicione(Alienigena("Inimigo",
##                [naleatorios.faixa(self.tamanho[0]),
##                 naleatorios.faixa(self.tamanho[1]/2)],
##                 self.iInimigo))


    def cria_municao(self):
        caixa_m = ObjetosBonus("CaixaDeMisseis",
                    [naleatorios.faixa(self.tamanho[0]),
                    10], self.iCaixaDeMisseis)
        caixa_m.carga=50
        self.universo.adicione(caixa_m)

    def cria_resistencia(self):
        caixa_r = ObjetosBonus("CaixaDeResistencia",
                    [naleatorios.faixa(self.tamanho[0]),
                    10], self.iCaixaDeResistencia)
        caixa_r.carga=50
        self.universo.adicione(caixa_r)

    def tela_inicial(self):
        self.universo.desenhe_fundo()
        self.universo.desenhe([-1,-1],self.logo.imagem)
        self.universo.escreva([-1,450],  traducao.pega("pressionequalquertecla"), (255,255,0), 24)
        self.universo.escreva([-1,200],  "[P]Portugues [E]English [S]Spanol [F]Fran�ais", (255,255,0), 24)
        self.universo.atualize()
        while 1:
            #self.universo.inicie_sincronia()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return(1)

                if event.type==KEYDOWN or event.type==JOYBUTTONDOWN:
                    teclas = pygame.key.get_pressed()
                    if teclas[K_p]:
                        traducao.dicionario("pt_br")

                    if teclas[K_e]:
                        traducao.dicionario("en")

                    if teclas[K_s]:
                        traducao.dicionario("es")

                    if teclas[K_f]:
                        traducao.dicionario("fr")

                    self.nova_partida()
                    return(0)
            #self.universo.finalize_sincronia()

    def tela_fim_de_jogo(self):
        self.universo.desenhe([-1,-1], self.fim_de_jogo.imagem)
        self.universo.escreva([-1,450], traducao.pega("pressionexour"), (255,255,0),24)
        self.universo.atualize()
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return(1)
                if event.type==KEYDOWN:
                    teclas = pygame.key.get_pressed()
                    if teclas[K_r]:
                        return(0)
                    elif teclas[K_x]:
                        return(1)
                if event.type==JOYBUTTONDOWN:
                                        if event.button % 2 == 0:
                                            return(0)
                                        else:
                                            return(1)

    def movemouse(self, evento):
                if evento.rel[0] < -self.sensibilidade_mouse:
                    self.jogador.move(1)
                elif evento.rel[0]> self.sensibilidade_mouse:
                    self.jogador.move(0)
                if evento.rel[1] < -self.sensibilidade_mouse:
                    self.jogador.move(3)
                elif evento.rel[1] > self.sensibilidade_mouse:
                    self.jogador.move(2)
                if evento.buttons[0] == 1: #and c % 3 == 0:
                    self.atira(evento)

    def movejoystick(self, evento):
        # print "JOYAXISMOTION"
        #print event.joy
        #print event.axis
        #print event.value
        if event.axis == 0:
            if event.value>0.0:
                self.jogador.ix=5
                #self.jogador.move(0)
                #print "direita"
            elif event.value<-1.0:
                self.jogador.ix=-5
                #self.jogador.move(1)
                #print "esquerda"
        elif event.axis == 1:
            if event.value>0.0:
                self.jogador.iy=5
                #self.jogador.move(2)
                #print "baixo"
            elif event.value<-1.0:
                self.jogador.iy=-5
                #self.jogador.move(3)
                #print "cima"

    def inicializa_eventos(self):
        self.eventos[MOUSEBUTTONDOWN] = self.atira
        self.eventos[MOUSEMOTION] = self.movemouse
        self.eventos[JOYAXISMOTION]=self.movejoystick
        self.eventos[MOUSEBUTTONDOWN]=self.atira
        #self.eventos[MOUSEBUTTONUP]
        self.eventos[QUIT]=self.saida
        #self.eventos[JOYBALLMOTION]
        #self.eventos[ JOYBUTTONUP]
        #self.eventos[JOYHATMOTION]
        self.eventos[JOYBUTTONDOWN]=self.atira

    def esquerda(self):
        self.jogador.move(1)

    def direita(self):
        self.jogador.move(0)

    def cima(self):
        self.jogador.move(3)

    def baixo(self):
        self.jogador.move(2)

    def aumentamisseis(self):
        self.jogador.misseis+=1000

    def aumentaresistencia(self):
        self.jogador.resistencia+=1000

    def inicializa_comandos(self):
        self.comandos[K_LEFT]=self.esquerda
        self.comandos[K_RIGHT]=self.direita
        self.comandos[K_UP]=self.cima
        self.comandos[K_DOWN]=self.baixo
        self.comandos[K_SPACE]=self.atira
        self.comandos[K_x]=self.saida
        self.comandos[K_ESCAPE]=self.saida
        self.comandos[K_m]=self.aumentamisseis
        self.comandos[K_r]=self.aumentaresistencia
        self.comandos[K_KP_PLUS]=self.video.proximo_modo
        self.comandos[K_PLUS]=self.video.proximo_modo
        self.comandos[K_EQUALS]=self.video.proximo_modo
        self.comandos[K_KP_MINUS]=self.video.anterior_modo
        self.comandos[K_MINUS]=self.video.anterior_modo
        self.comandos[K_KP_MULTIPLY] =self.video.faz_tela_cheia
        self.comandos[K_ASTERISK]=self.video.faz_tela_cheia
        self.comandos[K_8]=self.video.faz_tela_cheia

    def saida(self,evento=None):
        self.sair = True

    def carrega_fase(self):
        self.frame = 0
        self.ultimo_tiro=0
        self.fases[self.fase]()

    def avanca_fase(self):
        self.fase+=1
        if self.fase==len(self.fases):
            return False
        else:
            self.carrega_fase()
            return True

    def repeticao_do_jogo(self):
        self.universo.desenhe_fundo()
        self.sair = False
        self.frame = 0
        self.carrega_fase()
        pos_script = 0
        while self.jogador.resistencia > 0 and not self.sair:
            self.frame += 1
            self.universo.inicie_sincronia()



            while 1:
                event = pygame.event.poll()
                if event.type == NOEVENT: break
                if event.type in self.eventos:
                       self.eventos[event.type](event)

##            if event.type ==  KEYDOWN:
            teclas = pygame.key.get_pressed()
            for comando in self.comandos.keys():
                if teclas[comando]:
                    self.comandos[comando]()


            if self.script[pos_script][0] <= self.frame:
                exec(self.script[pos_script][1])
                pos_script+=1
                if pos_script == len(self.script):
                    pos_script=0
                    if not self.avanca_fase():
                        return(0)
##            if self.frame % 30 == 0:
##                for x in range(naleatorios.faixa(1, 2 +self.frame / 300)):
##                    self.cria_alienigena()
##            if self.frame % 300 == 0:
##                self.cria_municao()
##            if self.frame % 600 == 0:
##                self.cria_resistencia()

            self.universo.desenhe_fundo()
            self.universo.desenhe_objetos()
            self.universo.atualize()


            self.universo.finalize_sincronia()

        self.universo.desenhe_fundo()
        self.placar.respire()
        self.universo.desenhe_objetos()
        self.universo.atualize()
        if self.sair:
            return(1)
        else:
            return(0)

# Jogo - Principal
def jogo():
    try:
        # Cria o jogo em uma janela de 800x600
        jogo = Invasores([800,600])
        pygame.mouse.set_visible(0)
        # Loop principal do Jogo
        while 1:
            if jogo.tela_inicial():
                break;
            pygame.event.set_grab(1)
            jogo.nova_partida()
            if jogo.repeticao_do_jogo():
                break;
            pygame.event.set_grab(0)
            if jogo.tela_fim_de_jogo():
                break;
    finally:
        pygame.display.quit()


#import profile
#profile.run("jogo()")
#traducao.dicionario("pt_br")

traducao.dicionario("en")

jogo()
