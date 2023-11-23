"""
Universidade de Brasilia
Instituto de Ciencias Exatas
Departamento de Ciencia da Computacao
Algoritmos e Programação de Computadores - 2/2023
Turma: Prof. Carla Castanho e Prof. Frank Ned
Aluno(a): Rafael Dias Ghiorzi
Matricula: 232006144
Projeto Final - Parte 1
Descricao: < O programa é um jogo básico parecido onde você é um personagem que deve
destruir inimigos sem deixar que eles te encostem, enquanto captura tanques de combustível
para sobreviver o máximo de tempo possível. é um jogo simples que usa apenas elementos
retangulares, feito para ser intuitivo até para o menos conhecedor de jogos de computadores >
"""

import pygame
import os
import sys
from pygame.locals import *
import random

# -------------VARIÁVEIS----------#
displayHeight = 500
displaWidth = 1080
tamanhoPixel = 20
fps = float(50)
combustivel = 400
probabilidadeInimigo = 30
probabilidadeTanque = 60
velocidade = 2  # velocidade do jogo
pontos = 0
run = True
clock = pygame.time.Clock()
qntTiros = []
qntInimigos = []
qntTanquesCombustivel = []

# ------------CLASSES-------------#
class Jogador:
    def __init__(self, cor, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = cor
        self.speed = velocidade + 1

    def colisao(self, outro_rect):
        return self.rect.colliderect(outro_rect)

class Projeteis:
    def __init__(self, cor, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = cor
        self.speed = velocidade
        self.rect.x = self.rect.x + self.speed

    def colisao(self, outro_rect):
        return self.rect.colliderect(outro_rect)

class TanquesCombustivel:
    def __init__(self, y):
        self.rect = pygame.Rect(displaWidth, y, tamanhoPixel, tamanhoPixel)
        self.color = (0, 0, 255)
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed

class Inimigos:
    def __init__(self, y):
        self.rect = pygame.Rect(displaWidth, y, tamanhoPixel, tamanhoPixel)
        self.color = (0, 255, 0)
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed

# ------------FUNÇÕES-------------#
def ResetGame():
    global run, combustivel, pontos, fps, clock, jogador, janela, qntTiros, qntInimigos, tiro, qntInimigos, probabilidadeInimigo, probabilidadeTanque, unidadeCombustivel, qntTanquesCombustivel

    # reinicia todas as variáveis globais #
    global displayHeight, displaWidth, tamanhoPixel, fps, combustivel, probabilidadeInimigo, probabilidadeTanque, velocidade, pontos, run, clock, qntTiros, qntInimigos, qntTanquesCombustivel
    displayHeight = 500
    displaWidth = 1080
    tamanhoPixel = 20
    fps = float(50)
    combustivel = 400
    probabilidadeInimigo = 30
    probabilidadeTanque = 60
    velocidade = 2
    pontos = 0
    run = True
    clock = pygame.time.Clock()
    qntTiros = []
    qntInimigos = []
    qntTanquesCombustivel = []

    # reinicia objetos específicos 
    jogador = Jogador((0, 255, 0), 5, 50, tamanhoPixel, tamanhoPixel)

    # reinicia a janela
    janela = pygame.display.set_mode((displaWidth, displayHeight))

    # reinicialize o jogo
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Window Invaders")
    font = pygame.font.Font(None, 24)

def Start():
    os.system('cls||clear')
    escolha = input("Window Invaders! \nBem-vindo, jogador!\nPressione enter para prosseguir...")
    if escolha == "":
        Menu()
    else:
        Start()

def Menu():
    os.system('cls||clear')
    print("1 - Jogar")
    print("2 - Configuracoes")
    print("3 - Rankings")
    print("4 - Instrucoes")
    print("5 - Sair")
    escolha = input("Escolha uma opção: ")

    match escolha:
        case "1": Jogo()
        case "2": Config()  # ainda a ser implementada
        case "3": Ranking()  # ainda a ser implementada
        case "4": Instrucoes()
        case "5": Sair()  # ainda a ser implementada

def Instrucoes():
    os.system('cls||clear')
    print("Bem-vindo ao windows invaders!\n- O jogo é bem simples, você é o personagem verde que está tentando sobreviver aos ataques dos inimigos vermelhos.\n- Se movimente para cima e para baixo com as teclas 'W' e 'S', respectivamente, para desviar dos ataques.\nNão deixe os inimigos encostarem em você!\n- Pressione 'X' para disparar um projétil que é capaz de destruir os inimigos!\n- O seu combustível vai gradualmente acabando com o decorrer do tempo, então toda vez que você tiver a oportunidade,\npegue os tanques azuis de combustível que regeneram em 40 pontos sua capacidade!\n- Cada inimigo que você derrotar são mais 50 pontos para sua pontuação, então trate de eliminar o máximo que você for capaz!\n\nBoa sorte, e não se esqueça que, quanto mais tempo se passa, mais rápida e dinâmica a batalha fica. Tome cuidado!\n")
    escolha = input("Pressione 'enter' para voltar...")
    if escolha == "":
        Menu()
    else:
        Instrucoes()

def Tiro():
    global linha, tiro, combustivel, qntTiros

    linha = jogador.rect.x
    combustivel -= 3
    tiro = Projeteis((0, 100, 0), linha, jogador.rect.y, tamanhoPixel, tamanhoPixel)
    qntTiros.append(tiro)

def Inimigo():
    inimigo = Inimigos(random.randint(30, displayHeight))
    qntInimigos.append(inimigo)

def Combustivel():
    unidadadeCombustivel = TanquesCombustivel(random.randint(30, displayHeight))
    qntTanquesCombustivel.append(unidadadeCombustivel)

def Jogo():
    global run, combustivel, pontos, fps, clock, jogador, janela, qntTiros, qntInimigos, tiro, qntInimigos, probabilidadeInimigo, probabilidadeTanque, unidadeCombustivel, qntTanquesCombustivel
        
    os.system('cls||clear')
    print("Boa sorte")
    
    #inicia a tela  
    janela = pygame.display.set_mode((displaWidth, displayHeight))
    #inicia jogador
    jogador = Jogador((0,255,0), 5, 50, tamanhoPixel, tamanhoPixel)
    #Configurações iniciais
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Window Invaders")
    font = pygame.font.Font(None, 24)


    while run:

        # imprime combustivel e pontuação no topo da tela #
        pontuacao = font.render(f'Pontuação: {pontos}', True, (0, 0, 0))
        nivelCombustivel = font.render(f'Combustível: {combustivel}', True, (0,0,0))
        janela.blit(pontuacao, (displaWidth - 140 , 10))
        janela.blit(nivelCombustivel, (10, 10))
        #-------------------------------------------------#
        
        # evento de fechar a janela #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                GameoverQuit()     
        #---------------------------#
        
        
        # ações possíveis do jogador #
            elif event.type == pygame.KEYDOWN:
                if event.key==120:
                    Tiro()

        key = pygame.key.get_pressed()
        if key[pygame.K_w] == True:
            jogador.rect.y = jogador.rect.y - jogador.speed

        elif key[pygame.K_s] == True:
            jogador.rect.y = jogador.rect.y + jogador.speed
        #----------------------------#
        
        # Cria inimigos e tanques de combustivel #
        chance = random.randint(0, probabilidadeInimigo)
        if chance == 10:
            Inimigo()
            
        chance = random.randint(0, probabilidadeTanque)
        if chance == 10:
            Combustivel()
        #----------------------------------------#
        
        # Detecta colisões #
        for inimigo in qntInimigos:
            if jogador.colisao(inimigo.rect):
                run = False
                pygame.quit()
                GameoverMorte()   
        
        for unidadeCombustivel in qntTanquesCombustivel:
            if jogador.colisao(unidadeCombustivel.rect):
                qntTanquesCombustivel.remove(unidadeCombustivel)
                combustivel += 40   
        
        for tiro in qntTiros:
            for inimigo in qntInimigos:
                if tiro.colisao(inimigo.rect):
                    qntInimigos.remove(inimigo)
                    qntTiros.remove(tiro)
                    pontos += 50

        if jogador.rect.top <= 30:
            jogador.rect.top = 30
        if jogador.rect.bottom >= displayHeight:
            jogador.rect.bottom = displayHeight
        #------------------#
        
        # atualiza a tela, inimigos, projeteis, personagem e combustiveis #
        chance = random.randint(0, 7)                                    # fácil (0,10) | médio (0,7) | dificil (0,5)
        if chance == 7:
            combustivel -= 1
        
        pygame.draw.rect(janela, (0, 255, 0), jogador)
        
        for inimigo in qntInimigos:
            pygame.draw.rect(janela, (255, 0 ,0), inimigo)
            inimigo.rect.x = inimigo.rect.x - inimigo.speed
        
        for tiro in qntTiros:
            pygame.draw.rect(janela, (0, 100, 0), tiro)
            tiro.rect.x = tiro.rect.x + tiro.speed + 3
        
        for unidadeCombustivel in qntTanquesCombustivel:
            pygame.draw.rect(janela, (0, 0, 255), unidadeCombustivel)
            unidadeCombustivel.rect.x = unidadeCombustivel.rect.x - unidadeCombustivel.speed
            
        pygame.display.flip()
        janela.fill(pygame.Color('grey'))
        fps = float(fps) + float(0.01)
        clock.tick(fps)   
        #-----------------#
        
        # Checa a quantidade de combustível #
        if combustivel <= 0:
            pygame.quit()

            GameoverCombustivel()
        #-----------------------------------#
def GameoverMorte():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTiros, qntInimigos

    os.system('cls||clear')
    print("O inimigo chegou até você! Não deixe acontecer novamente...")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu")
    combustivel = 400
    pontos = 0
    fps = 50
    qntInimigos.clear()
    qntTiros.clear()
    qntTanquesCombustivel.clear()

    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":
            ResetGame()
            run = True
            Jogo()
        case "2":
            run = True
            Menu()

def GameoverCombustivel():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTiros, qntInimigos
    
    os.system('cls||clear')
    
    print("Seu combustível acabou! Preste mais atenção na próxima vez...")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu")
    combustivel = 400
    pontos = 0
    fps = 50
    qntInimigos.clear()
    qntTiros.clear()
    qntTanquesCombustivel.clear()
    
    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":
            ResetGame()
            run = True
            Jogo()
        case "2": 
            run = True
            Menu()
def GameoverQuit():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTiros, qntInimigos
    
    os.system('cls||clear')
    
    print("Não desista tão fácil assim da missão!")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu")
    combustivel = 400
    pontos = 0
    fps = float(50)
    qntInimigos.clear()
    qntTiros.clear()
    qntTanquesCombustivel.clear()
    
    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":
            ResetGame()            
            run = True
            Jogo()
        case "2": 
            run = True
            Menu()
def Sair():
    os.system('cls||clear')
    sys.exit()
Start()



