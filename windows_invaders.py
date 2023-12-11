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
import time
import json

# -------------VARIÁVEIS----------#
displayHeight = 500
displayWidth = 1000
tamanhoPixel = 20
fps = float(50)

combustivel = 400
pontos = 0

probabilidadeX = 40 # 1 até 4, 25% de chance
probabilidadeF = 100# 10% de chance
probabilidadeO = 1000 # 1% de chance
probabilidadeT = 250
vidaO = 10 #cada tiro dá 5
municaoT = 5 #quantos tiros pode dar

velocidade = 2  # velocidade do jogo

modoRanqueado = False
run = True

clock = pygame.time.Clock()
qntTirosJogador = []
qntTirosInimigo = []
qntInimigosX = []
qntInimigosO = []
qntInimigosT = []
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

class ProjeteisInimigos: #amarelo
    def __init__(self, cor, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255,255,0)
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed + 10

    def colisao(self, outro_rect):
        return self.rect.colliderect(outro_rect)

class TanquesCombustivel:
    def __init__(self, y):
        self.rect = pygame.Rect(displayWidth, y, tamanhoPixel, tamanhoPixel)
        self.color = (0, 0, 255)
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed

class criaInimigosX:
    def __init__(self, y):
        self.rect = pygame.Rect(displayWidth, y, tamanhoPixel, tamanhoPixel)
        self.color = (0, 255, 0)
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed

class criaInimigosO: #anda e quando é morto apaga todos os inimigos da tela
    def __init__(self, y):
        self.rect = pygame.Rect(displayWidth, y, tamanhoPixel, tamanhoPixel)
        self.color = (255,99,71) #laranja
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed
        self.vida = vidaO
        
class criaInimigosT: #atira e pode colidir com o jogador, tiro mais rápido
    def __init__(self, y):
        self.rect = pygame.Rect(displayWidth, y, tamanhoPixel, tamanhoPixel)
        self.color = (128,0,0) # vermelho escuro
        self.speed = velocidade
        self.rect.x = self.rect.x - self.speed
        self.municao = municaoT
        self.direcao = 1
        
# ------------FUNÇÕES-------------#
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
        case "3": Rankings()  # ainda a ser implementada
        case "4": Instrucoes()
        case "5": Sair()  # ainda a ser implementada
        case _: Menu()

def Instrucoes():
    os.system('cls||clear')
    print("Bem vindo ao Window invaders!\nSua missão é sobreviver o máximo de tempo na arena enquanto elimina inimigos que tentam de matar!\nMova-se para cima e para baixo usando 'W' e 'S' e atire usando 'X'\nExistem 4 elementos que surgem no mapa:\n- O inimigo vermelho apenas anda em sua direção e eliminá-lo você ganha 50 pontos\n- O inimigo laranja não atira e não te mata, ele tem mais vida que o inimigo normal e ao matá-lo, todos os inimigos vermelhos do mapa são eliminados\n- O inimigo vermelho escuro se move na sua direção e para cima e para baixo. Ele tem 5 munições que ele atira aleatoriamente na sua direção. Desvie do inimigo e do tiro ou atire contra ele, os dois funcionam!\n\nVocê pode ativar o modo ranqueado para salvar sua pontuação no placar ou apenas jogar casualmente.\nSeu combustível acaba gradualmente. Pegue os tanques azuis para repor 40 pontos de combustível por vez.\n\nBoa sorte na sua jornada!\n")
    escolha = input("Pressione 'enter' para voltar...")
    if escolha == "":
        Menu()
    else:
        Instrucoes()

def Rankings():
    os.system('cls||clear')
    print("Ranking dos 10 Melhores Jogadores:")
    
    destino = "ranking.json"

    try:
        # Tentar abrir o arquivo para leitura
        with open(destino, "r") as arquivo:
            try:
                ranking = json.load(arquivo)
            except json.JSONDecodeError:
                print("ainda não existe um rank, tente novamente após jogar uma partida ranqueada")
                time.sleep(3)
                Menu()
    except FileNotFoundError:
            print("O arquivo rank ainda não existe, tente novamente após jogar uma partida ranqueada")
            time.sleep(2)
            Menu()

    if not ranking:
        print("Ainda não há jogadores no ranking.")
        time.sleep(2)
        Menu()
    else:
        # Exibir os 10 primeiros registros do ranking
        for i, jogador in enumerate(ranking[:10], start=1):
            print(f"{i}. {jogador['nickname']}: {jogador['pontos']} pontos")

    input("Pressione Enter para voltar ao menu...")
    Menu()
#--------------- FUNÇÕES DAS CONFIGURAÇÕES ---------------#
def Config():
    os.system('cls||clear')
    print("Selecione as configurações que deseja mudar")
    print("1 - Tabuleiro")
    print("2 - NPCs")
    print(f'3 - {"Ativar" if modoRanqueado == False else "Desativar" } modo ranqueado')
    print("4 - Voltar")
    escolha = input("Escolha uma opção: ")
        
    match escolha:
        case "1": Tabuleiro()
        case "2": NPCs()
        case "3": ModoRanqueado()
        case "4": Menu()
        case _: Config()

def Tabuleiro():
    global displayWidth, displayHeight
    os.system('cls||clear')
    if modoRanqueado == True:
        print("Você não pode alterar o tamanho do tabuleiro no modo ranqueado!\nVoltando para o menu...")
        time.sleep(3)
        Menu()
    
    print("Selecione o tamanho do tabuleiro da seguinte forma (TamanhoX TamanhoY):")
    print(f'O tamanho atual é de {displayWidth} por {displayHeight}')
    escolhaX, escolhaY = input("Digite as medidas para qual você deseja alterar:\n").split()
    displayWidth = int(escolhaX)
    displayHeight = int(escolhaY)
    time.sleep(1)
    print("Escolha salva! voltando para as configurações...")
    time.sleep(2)
    Config()
    
def NPCs():
    global probabilidadeF, probabilidadeO, probabilidadeT, probabilidadeX,vidaO, municaoT
    os.system('cls||clear')
    if modoRanqueado == True:
        print("Você não pode as propriedades dos NPCs no modo ranqueado!\nVoltando para o menu...")
        time.sleep(3)
        Menu()
        
    print("Selecione a chance de aparecer todos os respectivos personagens do jogo, a chance é de 0 a 100,\nsendo 0 a 25 fácil, 25 a 60 média dificuldade, 60 a 100 é difícil")
    escolha = input("Selecione a probabilidadeX (de aparecer inimigos vermelhos):\n")
    probabilidadeX = int(escolha)
    print("Ok! passando para o próximo NPC...")
    time.sleep(1)
    
    os.system('cls||clear')
    escolha = input("Ótimo, agora selecione a probabilidadeF (de aparecer tanques de combustível):\n")
    probabilidadeF = int(escolha)
    print("Ok! passando para o próximo NPC...")
    time.sleep(1)
    
    os.system('cls||clear')
    escolha = input("Ótimo, agora selecione a probabilidadeO (de aparecer inimigos laranjas):\n")
    probabilidadeO = int(escolha)
    print("Ok! passando para o próximo NPC...")
    time.sleep(1)
    
    os.system('cls||clear')
    escolha = input("Ótimo, agora selecione a probabilidadeT (de aparecer inimigos vermelho escuro):\n")
    probabilidadeT = int(escolha)
    print("Ok! Agora veremos as qualidadades dos inimigos...")
    time.sleep(1)
    
    os.system('cls||clear')
    escolha = input("Qual deve ser a vida do inimigo laranja? Lembrando que cada tiro seu dá 5 de dano cada:\n")
    vidaO = int(escolha)
    print("Ok!")
    time.sleep(1)
    print("")
    escolha = input("E qual deve ser a munição do inimigo vermelho escuro? Lembrando que o padrão é de 5 tiros cada um:\n")
    municaoT = int(escolha)
    print("Ok! Todas as configurações foram aplicadas! Voltando para as configurações...")
    time.sleep(1)
    Config()
    
def ModoRanqueado():
    global modoRanqueado, displayHeight, displayWidth, probabilidadeF, probabilidadeO, probabilidadeT, probabilidadeX, municaoT, vidaO
    if modoRanqueado == True:
        os.system('cls||clear')
        escolha = input("Desativar modo ranqueado? (s/n):\n")
        if escolha == "s":
            modoRanqueado = False
            probabilidadeX = 40 # 1 até 4, 25% de chance
            probabilidadeF = 100# 10% de chance
            probabilidadeO = 1000 # 1% de chance
            probabilidadeT = 250
            vidaO = 10 #cada tiro dá 5
            municaoT = 5 #quantos tiros pode dar
            
            
        elif escolha == "n":
            modoRanqueado = True
            displayHeight = 400
            displayWidth = 1350
            probabilidadeX = 60 # 1 até 4, 25% de chance
            probabilidadeF = 150 # 10% de chance
            probabilidadeO = 500 # 1% de chance
            probabilidadeT = 250  # 4% de chance
            municaoT = 7
            vidaO = 15
            
            
        else:
            ModoRanqueado()
        print("Salvando sua escolha e voltando para as configurações...")
        time.sleep(2)    
        Config()
        
    if modoRanqueado == False:
        os.system('cls||clear')
        escolha = input("Ativar modo ranqueado? (s/n)\n")
        if escolha == "s":
            modoRanqueado = True
            displayHeight = 400
            displayWidth = 1350
            probabilidadeX = 40 # 1 até 4, 25% de chance
            probabilidadeF = 150 # 10% de chance
            probabilidadeO = 700 # 1% de chance
            probabilidadeT = 250  # 4% de chance
            municaoT = 7
            vidaO = 15
        elif escolha == "n":
            modoRanqueado = False
            probabilidadeX = 60 # 1 até 4, 25% de chance
            probabilidadeF = 100# 10% de chance
            probabilidadeO = 500 # 1% de chance
            probabilidadeT = 400
            vidaO = 10 #cada tiro dá 5
            municaoT = 5 #quantos tiros pode dar
        else:
            ModoRanqueado()
        print("Salvando sua escolha e voltando para as configurações...")
        time.sleep(2)
        Config()
#---------------------------------------------------------#

#--------------- FUNÇÕES DE FUNCIONAMENTO DO JOGO --------#
def ResetGame():
    global run, combustivel, pontos, fps, clock, jogador, janela, qntTirosJogador, qntInimigos, tiro, qntInimigos, probabilidadeX, probabilidadeF, probabilidadeO, probabilidadeT, unidadeCombustivel, qntTanquesCombustivel

    # reinicia todas as variáveis globais #
    global displayHeight, displayWidth, tamanhoPixel, fps, combustivel, probabilidadeX, velocidade, pontos, run, clock, qntTirosJogador, qntInimigos, qntTanquesCombustivel, municaoT, vidaO
    displayHeight = displayHeight
    displayWidth = displayWidth
    tamanhoPixel = tamanhoPixel
    fps = float(50)
    combustivel = 400
    velocidade = 2
    pontos = 0
    run = True
    clock = pygame.time.Clock()
    qntTirosJogador = []
    qntInimigos = []
    qntTanquesCombustivel = []
    probabilidadeX = probabilidadeX
    probabilidadeF = probabilidadeF
    probabilidadeO = probabilidadeO
    probabilidadeT = probabilidadeT
    municaoT = 5  # Valor padrão
    vidaO = vidaO

    # reinicia objetos específicos 
    jogador = Jogador((0, 255, 0), 5, (displayHeight / 2), tamanhoPixel, tamanhoPixel)

    # reinicia a janela
    janela = pygame.display.set_mode((displayWidth, displayHeight))

    # reinicialize o jogo
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Window Invaders")
    font = pygame.font.Font(None, 24)

def Tiro():
    global linha, tiro, combustivel, qntTirosJogador

    linha = jogador.rect.x
    combustivel -= 3
    tiro = Projeteis((0, 100, 0), linha, jogador.rect.y, tamanhoPixel, tamanhoPixel)
    qntTirosJogador.append(tiro)

def InimigoX():
    inimigoX = criaInimigosX(random.randint(30, displayHeight))
    qntInimigosX.append(inimigoX)

def InimigoO():
    inimigoO = criaInimigosO(random.randint(30, displayHeight))
    qntInimigosO.append(inimigoO)
    
def InimigoT():
    inimigoT = criaInimigosT(random.randint(30, displayHeight))
    qntInimigosT.append(inimigoT)

def Combustivel():
    unidadadeCombustivel = TanquesCombustivel(random.randint(30, displayHeight))
    qntTanquesCombustivel.append(unidadadeCombustivel)

#------------------ MAIN -----------------------------#
def Jogo():
    global run, combustivel, pontos, fps, clock, jogador, janela, qntTirosJogador, qntInimigos, tiro, qntInimigos, unidadeCombustivel, qntTanquesCombustivel, modoRanqueado, nickname

    
    if modoRanqueado == True:
        def Nickname():
            global nickname
            os.system('cls||clear')
            nickname = input("Antes do jogo ranqueado começar, escreva seu nickname para que possamos salvar sua pontuação:\nOBS: o nome deve conter entre 1 e 10 caracteres:\n")
            if len(nickname) < 1 or len(nickname) > 10:
                print("nome inválido, tente novamente!")
                time.sleep(2)
                Nickname()
            return
        Nickname()
        
        time.sleep(1)
        print("Ok! Boa sorte na arena!")
        time.sleep(2)
    else:
        os.system('cls||clear')
        print("Boa sorte")
        time.sleep(1)
    
    ResetGame()
    
    #inicia a tela  
    janela = pygame.display.set_mode((displayWidth, displayHeight))
    #inicia jogador
    jogador = Jogador((0,255,0), 5, 50, tamanhoPixel, tamanhoPixel)
    #Configurações iniciais
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Window Invaders")
    font = pygame.font.Font(None, 24)


    while run:

        # imprime combustivel e pontuação no topo da tela e modo ranqueado se estiver ativo#
        pontuacao = font.render(f'Pontuação: {pontos}', True, (0, 0, 0))
        nivelCombustivel = font.render(f'Combustível: {combustivel}', True, (0,0,0))
        janela.blit(pontuacao, (displayWidth - 140 , 10))
        janela.blit(nivelCombustivel, (10, 10))
        
        if modoRanqueado == True:
            avisoRanqueado = font.render(f'Modo Ranqueado', True, (0,0,0))
            janela.blit(avisoRanqueado, ((displayWidth/2) - 5, 10))
        #-------------------------------------------------#
        
        # evento de fechar a janela #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                if modoRanqueado == True:
                    registerMatch(nickname, pontos)
                GameoverQuit()     
        #---------------------------#
        
        
        # ações possíveis do jogador #
            elif event.type == pygame.KEYDOWN:
                if event.key==120:  #ascii pra 'X'
                    Tiro()

        key = pygame.key.get_pressed()
        if key[pygame.K_w] == True:
            jogador.rect.y = jogador.rect.y - jogador.speed

        elif key[pygame.K_s] == True:
            jogador.rect.y = jogador.rect.y + jogador.speed
        #----------------------------#
        
        # Cria tipos de inimigos e tanques de combustivel # (0 a 25 é fácil, 25 a 60 é média dificuldade, 60 a 100 é difícil)
        chance = random.randint(0, probabilidadeX)
        if chance == 1:
            InimigoX()
            
        chance = random.randint(0, probabilidadeF)
        if chance == 1:
            Combustivel()
            
        chance = random.randint(0, probabilidadeO)
        if chance == 1:
            InimigoO()
            
        chance = random.randint(0, probabilidadeT)
        if chance == 1:
            InimigoT()
        
        
        for inimigo in qntInimigosT:    
            chance = random.randint(0, 500)
            if chance == 1:
                if inimigo.municao >= 0:
                    linhaInimigo = inimigo.rect.x
                    colunaInimigo = inimigo.rect.y
                    tiro = ProjeteisInimigos((255,255,0), linhaInimigo, colunaInimigo, tamanhoPixel, tamanhoPixel)
                    qntTirosInimigo.append(tiro)
                inimigo.municao -= 1
        #----------------------------------------#
        
        # Detecta colisões #
        for inimigo in qntInimigosX:
            if jogador.colisao(inimigo.rect):
                run = False
                pygame.quit()
                if modoRanqueado == True:
                    registerMatch(nickname, pontos)
                GameoverMorte()   
                
        for inimigo in qntInimigosT:
            if jogador.colisao(inimigo.rect):
                run = False
                pygame.quit()
                if modoRanqueado == True:
                    registerMatch(nickname, pontos)
                GameoverMorte()
        
        for unidadeCombustivel in qntTanquesCombustivel:
            if jogador.colisao(unidadeCombustivel.rect):
                qntTanquesCombustivel.remove(unidadeCombustivel)
                combustivel += 40 
                
        for tiro in qntTirosInimigo:
            if jogador.colisao(tiro.rect):  
                run = False
                pygame.quit()
                if modoRanqueado == True:
                    registerMatch(nickname, pontos)
                GameOverTiro()
                
        for tiro in qntTirosJogador:
            for inimigo in qntInimigosX:
                if tiro.colisao(inimigo.rect):
                    qntInimigosX.remove(inimigo)
                    qntTirosJogador.remove(tiro)
                    pontos += 50
                    
        for tiro in qntTirosJogador:
            for inimigo in qntInimigosO:
                if tiro.colisao(inimigo.rect):
                    inimigo.vida -= 5
                    if inimigo.vida <= 0:
                        qntInimigosO.remove(inimigo)
                        pontos += ((len(qntInimigosX)) * 10)
                        qntInimigosX.clear()
                    qntTirosJogador.remove(tiro)
                    break
                        
        for tiro in qntTirosJogador:
            for inimigo in qntInimigosT:
                if tiro.colisao(inimigo.rect):
                    qntInimigosT.remove(inimigo)
                    qntTirosJogador.remove(tiro)
                    
        for inimigo in qntInimigosT:
            if jogador.colisao(inimigo.rect):
                run = False
                pygame.quit()
                if modoRanqueado == True:
                    registerMatch(nickname, pontos)
                GameoverMorte()  
                
        for tiro in qntTirosJogador:
            for tiroInimigo in qntTirosInimigo:
                if tiro.colisao(tiroInimigo.rect):
                    qntTirosInimigo.remove(tiroInimigo)
                    qntTirosJogador.remove(tiro)
                 
        #-----não deixa o jogador e inimigos sairem da tela----#
        if jogador.rect.top <= 30:
            jogador.rect.top = 30
        if jogador.rect.bottom >= displayHeight:
            jogador.rect.bottom = displayHeight
            
        for inimigo in qntInimigosT:
            if inimigo.rect.top <= 30:
                inimigo.rect.y = 30
            if inimigo.rect.bottom >= displayHeight:
                inimigo.rect.bottom = displayHeight
                
        for inimigo in qntInimigosO:
            if inimigo.rect.y <= 30:
                inimigo.rect.top = 30
            if inimigo.rect.bottom >= displayHeight:
                inimigo.rect.bottom = displayHeight      
                
        for inimigo in qntInimigosX:
            if inimigo.rect.top <= 30:
                inimigo.rect.y = 30
            if inimigo.rect.bottom >= displayHeight:
                inimigo.rect.bottom = displayHeight  
        #-----------------------------------------#
        
        

        # atualiza a tela, inimigos, projeteis, personagem e combustiveis #
        chance = random.randint(0, 5)                             
        if chance == 3:
            combustivel -= 1
        
        pygame.draw.rect(janela, (0, 255, 0), jogador)
        
        for inimigo in qntInimigosX:
            pygame.draw.rect(janela, (255, 0 ,0), inimigo)
            inimigo.rect.x = inimigo.rect.x - inimigo.speed
        
        for inimigo in qntInimigosO:
            pygame.draw.rect(janela, (216, 108, 0), inimigo)
            inimigo.rect.x = inimigo.rect.x - inimigo.speed        

        for inimigo in qntInimigosT:
            pygame.draw.rect(janela, (128, 0, 0), inimigo)
            inimigo.rect.x = inimigo.rect.x - inimigo.speed
            inimigo.rect.y += inimigo.speed * inimigo.direcao
            
            chance = random.randint(0,50)
            if chance == 1:
                inimigo.direcao = -1   
            if chance == 2:
                inimigo.direcao = 1
                    
        for tiro in qntTirosJogador:
            pygame.draw.rect(janela, (0, 100, 0), tiro)
            tiro.rect.x = tiro.rect.x + tiro.speed + 3
            
        for tiro in qntTirosInimigo:
            pygame.draw.rect(janela, (255, 255, 0), tiro)
            tiro.rect.x = tiro.rect.x - tiro.speed - 2
        
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
            if modoRanqueado == True:
                registerMatch(nickname, pontos)
            GameoverCombustivel()
        #-----------------------------------#
#-----------------------------------------------------#

#------------------ FINALIZAÇÃO DA RODADA E SALVAMENTO DOS DADOS -------------------#
def registerMatch(nickname, pontos):

    arquivoRank = "ranking.json"

    try:
        with open(arquivoRank, "r") as arquivo:
            try:
                ranking = json.load(arquivo)
            except json.JSONDecodeError:
                with open(arquivoRank, "w") as arquivo:
                    ranking = [{"nickname": nickname, "pontos" : pontos}]
                    json.dump(ranking, arquivo)
    except FileNotFoundError:
        print("arquivo de ranks não encontrado!")
        time.sleep(2)
        Menu()

    ranking.append({"nickname": nickname, "pontos": pontos})

    ranking = sorted(ranking, key=lambda x: x["pontos"], reverse=True)

    ranking = ranking[:10]

    with open(arquivoRank, "w") as arquivo:
        json.dump(ranking, arquivo)

    print("Partida registrada no ranking com sucesso!")
def GameOverTiro():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTirosJogador, qntInimigos, nickname

    os.system('cls||clear')
    print("Você levou um tiro! Não deixe acontecer novamente...")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu\n3 - Ver os rankings")
    combustivel = 400
    pontos = 0
    fps = 50
    qntInimigosX.clear()
    qntInimigosO.clear()
    qntInimigosT.clear()
    qntTirosInimigo.clear()
    qntTirosJogador.clear()
    qntTanquesCombustivel.clear()

    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":         
            run = True
            Jogo()
        case "2": 
            run = True
            Menu()
        case "3":
            run = True
            Rankings()  
def GameoverMorte():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTirosJogador, qntInimigos, nickname

    os.system('cls||clear')
    print("O inimigo chegou até você! Não deixe acontecer novamente...")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu\n3 - Ver os rankings")
    combustivel = 400
    pontos = 0
    fps = 50
    qntInimigosX.clear()
    qntInimigosO.clear()
    qntInimigosT.clear()
    qntTirosInimigo.clear()
    qntTirosJogador.clear()
    qntTanquesCombustivel.clear()

    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":         
            run = True
            Jogo()
        case "2": 
            run = True
            Menu()
        case "3":
            run = True
            Rankings()  
def GameoverCombustivel():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTirosJogador, qntInimigos
    
    os.system('cls||clear')
    
    print("Seu combustível acabou! Preste mais atenção na próxima vez...")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu\n3 - Ver os rankings")
    combustivel = 400
    pontos = 0
    fps = 50
    qntInimigos.clear()
    qntTirosJogador.clear()
    qntTanquesCombustivel.clear()
    
    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":      
            run = True
            Jogo()
        case "2": 
            run = True
            Menu()
        case "3":
            run = True
            Rankings()        
def GameoverQuit():
    global run, combustivel, pontos, fps, qntTanquesCombustivel, qntTirosJogador, qntInimigos
    
    os.system('cls||clear')
    
    print("Não desista tão fácil assim da missão!")
    print(f'Sua pontuação foi de {pontos} ponto(s), parabéns!')
    print("1 - Reiniciar\n2 - Voltar para o menu\n3 - Ver os rankings")
    combustivel = 400
    pontos = 0
    fps = float(50)
    qntInimigos.clear()
    qntTirosJogador.clear()
    qntTanquesCombustivel.clear()
    
    escolha = input("Escolha uma opção: ")
    match escolha:
        case "1":        
            run = True
            Jogo()
        case "2": 
            run = True
            Menu()
        case "3":
            run = True
            Rankings()            
def Sair():
    os.system('cls||clear')
    sys.exit()




#inicia tudo
Start()
