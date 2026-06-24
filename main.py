import pygame
import os
import classes.config as config

pygame.init()

#configurações
W = 1280
H = 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('make the gate')
font = pygame.font.Font('assets/font/DotGothic16-Regular.ttf', 28)
clock = pygame.time.Clock()

#música
pygame.mixer.music.load('assets/audio/background.mp3')
pygame.mixer.music.play()
som_finalizar = pygame.mixer.Sound('assets/audio/victory.mp3')

#precisam das configurações para serem importadas
from classes.portas import Porta, Input, Output, And, Not, Nand, Or, Xor
import classes.tools as tools

#classes
class Conexao():
    def __init__(self, origem, destino):
        self.origem = origem
        self.destino = destino

class Celula():
    def __init__(self,largura, altura, sprite):
        self.largura = largura
        self.altura = altura
        self.x = 0
        self.y = 0
        self.sprite = sprite
        self.sprite_original = sprite
        self.vazio = True
        self.porta = None
        self.valor = None

    def inserir_porta(self, porta:Porta):
        self.porta = porta
        self.vazio = False

    def limpar(self):
        self.vazio = True
        self.porta = None
        self.valor = None
        self.sprite = self.sprite_original

class Grid():
    def __init__(self, largura, altura, linhas, colunas, sprite):
        self.linhas = linhas
        self.colunas = colunas
        self.largura = largura
        self.altura = altura
        self.borda = 0
        self.sprite = sprite

        #células
        larguraCell = largura/colunas - self.borda
        alturaCell = altura/linhas - self.borda

        #matriz do tabuleiro com as células
        self.matriz = [] # self.matrix = list[list[Celula]]
        for i in range(linhas):
            self.matriz.append([])
            for j in range(colunas):
                self.matriz[i].append(Celula(larguraCell, alturaCell, self.sprite))

    def identificar_cell (self, li, col)-> Celula:
        return self.matriz[li][col]

    def selecionar_cell(self, pos):
            # converter as cordenadas x/y da tela para cordenadas do tabuleiro
            col = (pos[0] - self.x)//(self.identificar_cell(0,0).largura + self.borda)
            li = (pos[1] - self.y)//(self.identificar_cell(0,0).altura + self.borda)
            # mudar a cor da célula selecionada
            if 0 <= li < self.linhas and 0 <= col < self.colunas:
                #self.identificar_cell(int(li), int(col)).mudar()
                return self.identificar_cell(int(li), int(col))

class Board(Grid):
    def __init__(self, largura, altura, linhas, colunas, sprite, fundo=None):
        super().__init__(largura, altura, linhas, colunas,  sprite)
        #conexões entre blocos
        self.conexoes = []
        self.portas_ativas = []
        self.fundo = None

    def render(self, screen, x, y): #desenhar o grid
        self.x = x
        self.y = y
        #fazer para desenhar a borda aq dps
        screen.blit(fundo, (self.x - 16, self.y - 16))
        for li in range(self.linhas):
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                celula.x = x + (celula.largura + self.borda) * col
                celula.y = y + (celula.altura + self.borda) * li
                screen.blit(self.sprite, (celula.x, celula.y))

    def render_portas(self,screen):
        for li in range(self.linhas):
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                if celula.porta:
                    sprite = pygame.transform.scale(celula.porta.sprite, (celula.largura, celula.altura))
                    screen.blit(sprite, (celula.x, celula.y))

    def conectar(self, origem:Porta, destino:Porta):
        if origem == destino: #nao criar conexao entre a porta e ela mesma
            return
        if len(destino.entradas) >= destino.qte_entradas: #nao criar conexao caso as entradas do destino ja estiverem cheias
            return
        if not origem.pode_saida: #nao criar conexao caso a origem nao possa ser saída (caso output)
            return
        nova = Conexao(origem, destino) #criar conexao caso passe das verificações anteriores
        self.conexoes.append(nova)
        destino.entradas.append(origem)
        origem.saidas.append(destino)

        if origem not in self.portas_ativas:
            self.portas_ativas.append(origem)
        if destino not in self.portas_ativas:
            self.portas_ativas.append(destino)

    def limpar_cell(self, cell:Celula):
        porta = cell.porta
        if porta is None:
            return
        for entrada in porta.entradas: #remover a porta da lista de entrada de outras portas
            entrada.saidas.remove(porta)
        for saida in porta.saidas: #remover a porta da lista de saida de outras portas
            saida.entradas.remove(porta)
        self.conexoes = [  #refazer a lista de conexoes excluindo as que tenham a porta removida como entrada ou saída
            c for c in self.conexoes
            if c.origem != porta
            and c.destino != porta]

        if porta in self.portas_ativas:
            self.portas_ativas.remove(porta) #remover porta da lista de portas ativas
        cell.limpar() #limpar a celula (atributos porta, cor, vazio, valor)

    def avaliar_conexoes(self):
        for porta in self.portas_ativas:
            porta.avaliar()

    def simular(self, combinacao): #simular o output do circuito atual para diferentes estados dos inputs
        inputs = []
        estado_original = []
        for porta in self.portas_ativas:
            if isinstance(porta, Input):
                inputs.append(porta)
                estado_original.append(porta.estado)
        if len(inputs)==0 or len(inputs)!=len(combinacao):
            return

        for i in range(len(inputs)):
            inputs[i].estado = combinacao[i]

        self.avaliar_conexoes()

        resultado = None
        for porta in self.portas_ativas:
            if isinstance(porta, Output):
                resultado = porta.estado
        if resultado == None:
            return

        for i in range(len(inputs)):
            inputs[i].estado = estado_original[i]
        self.avaliar_conexoes()

        return resultado

    def render_conexoes(self, screen):
        for conexao in self.conexoes:
            origem = conexao.origem.celula
            destino = conexao.destino.celula
            x1 = origem.x + origem.largura - 10
            y1 = origem.y + origem.altura/2
            x2 = destino.x + 10
            y2 = destino.y + destino.altura/2
            if origem.porta.estado:
                cor = config.verde
            else:
                cor = config.vermelho
            pygame.draw.line(screen,cor,(x1,y1),(x2,y2),10)

    def reset(self):
        for porta in self.portas_ativas:
            self.limpar_cell(porta.celula)
        for li in range(self.linhas):
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                if celula.porta:
                    self.limpar_cell(celula)

class Inventario(Grid): #vou ter q refazer esse aqui tudo provavelmente RIP
    def __init__(self, largura, altura, linhas, colunas, sprite, itens):
        super().__init__(largura, altura, linhas, colunas, sprite)

        self.itens = itens

    def render(self, screen, x, y):
        i = 0
        self.x = x
        self.y = y
        portas = [Input, Output, Not, And, Or, Nand, Xor]
        tools_lista = [tools.continuar, tools.reiniciar, tools.sair]
        seta_sprite = pygame.image.load('assets/tools/seta_selecionado.png').convert_alpha()
        for li in range(self.linhas): #celulas
            for col in range(self.colunas):
                selecionado = False
                #retangulo
                celula = self.identificar_cell(li, col)
                xCell = x + (celula.largura + self.borda) * col
                yCell = y + (celula.altura + self.borda) * li
                if i < len(self.itens):
                    if self.itens[i].nome:
                        celula.valor = self.itens[i].nome
                        if self.itens[i] in portas:
                            celula.inserir_porta(self.itens[i])
                        if type(self.itens[i])==tools.Tool:
                            if self.itens[i].selecionado:
                                selecionado = True
                        sprite = self.itens[i].sprite
                    else:
                        sprite = pygame.image.load('assets/celula_iven.png').convert_alpha()
                else:
                    sprite = pygame.image.load('assets/celula_iven.png').convert_alpha()
                    celula.cor = config.vermelho
                i+=1
                screen.blit(sprite, (xCell, yCell))
                if selecionado:
                    screen.blit(seta_sprite, (xCell - 4, yCell))

    def atualizar(self, portas_novas):
        self.itens = portas_novas

class Fase():
    def __init__(self, inventario:list[Porta], limites:dict[Porta:int], objetivo:Porta, nome:str):
        #inventario = [In, Out, Not], limites = [In: 2, Out: 1], objetivo = Nand
        self.inventario = inventario
        self.limites = limites
        self.objetivo = objetivo
        self.nome = nome
        self.vitoria = False
    def render(self):
        text = f'{self.nome}, venceu: {self.vitoria}'
        text_surface = font.render(text, True, config.branco)
        text_rect = text_surface.get_rect()
        screen.blit(text_surface, text_rect)

class Tabela():
    def __init__(self, board:Board, fases, fase_atual:Fase):
        self.board = board
        self.fases = fases
        self.fase = fase_atual
        self.avaliacao = fases[fase_atual].objetivo.avaliacao
        self.dados = None

    def simular(self):
        def gerar_combinacoes(qte_inputs): #criar as combinações de valore para os inputs a partir da quantidade dada
            if qte_inputs < 1:
                return
            if qte_inputs == 1:
                return [(True,), (False,)]
            combinacoes = []
            anteriores = gerar_combinacoes(qte_inputs - 1)
            for comb in anteriores:
                combinacoes.append(comb + (True,))
                combinacoes.append(comb + (False,))
            return combinacoes

        combinacoes = gerar_combinacoes(self.fases[fase_atual].limites[Input]) #pq esse fase atual tá assim mds tenho que ajeitar
        self.combinacoes = combinacoes

        desejados = []
        for i in range(len(combinacoes)):
            desejados.append(self.avaliacao(*combinacoes[i]))
        self.desejados = desejados

        self.inputs = [] #pode ser os inputs atuais ou os inputs dados na fase
        self.outputs = []
        for porta in self.board.portas_ativas:
            if isinstance(porta, Input):
                self.inputs.append(porta)
            if isinstance(porta, Output):
                self.outputs.append(porta)

        #if len(self.inputs)==0 or len(self.outputs)==0:
        if len(self.inputs)<self.fases[self.fase].limites[Input] or len(self.outputs)<self.fases[self.fase].limites[Output]:
            return

        dados = []
        vitoria = True
        for i in range(len(combinacoes)):
            resultado = self.board.simular(combinacoes[i])
            #desejado = self.avaliacao(*combinacoes[i])
            desejado = desejados[i]
            comparacao = resultado==desejado

            pilha = []
            pilha.append(combinacoes[i])
            pilha.append(desejado)
            pilha.append(resultado)
            pilha.append(comparacao)
            dados.append(pilha)
            if not comparacao:
                vitoria = False

        self.dados = dados
        self.fases[fase_atual].vitoria = vitoria

    def atualizar (self, nova_fase):
        self.fase_atual = nova_fase
        self.avaliacao = self.fases[nova_fase].objetivo.avaliacao

    def render_text(self):
        print(self.dados)

    def render(self, screen, x, y):
        qte_inputs = self.fases[fase_atual].limites[Input]
        qte_outputs = self.fases[fase_atual].limites[Output]
        qte_combinacoes = 2**qte_inputs
        combinacoes = self.combinacoes
        output_fase = self.desejados

        #ajustando o fundo da tabela
        fundo_original = pygame.image.load('assets/tabela/tabela_fundo.png')
        altura = 16*3*(qte_combinacoes + 1)
        fundo = pygame.transform.scale(fundo_original,(fundo_original.get_width(), altura ))
        y -= altura
        screen.blit(fundo, (x, y))

        #sprites dos valores TRUE e FALSE
        true_sprite = pygame.image.load('assets/tabela/1.png')
        false_sprite = pygame.image.load('assets/tabela/0.png')

        #cabeçário inputs e valores das combinações
        for i in range(qte_inputs):
            input_sprite = pygame.image.load('assets/tabela/IN.png')
            screen.blit(input_sprite, (x + 16*(i*3+1), y + 16))
            for j in range(qte_combinacoes):
                if combinacoes[j][i]:
                    sprite = true_sprite
                else:
                    sprite = false_sprite
                screen.blit(sprite, (x + 16*(i*3+1), y + 16*(3 + j*3)))
                x_ultimo = x + 16*(i*3+1)

        #cabeçario fase e outputs desejados
        out_fase_sprite = pygame.image.load('assets/tabela/fase.png')
        screen.blit(out_fase_sprite, (x_ultimo + 16*3 , y + 16))
        x_ultimo += 16*3
        for i in range(len(output_fase)):
            if output_fase[i]:
                sprite = true_sprite
            else:
                sprite = false_sprite
            screen.blit(sprite, (x_ultimo + 16, y + 16*(3 + i*3)))

        #cabeçario player e outputs atuais
        player_sprite = pygame.image.load('assets/tabela/player.png')
        empty_sprite = pygame.image.load('assets/tabela/x.png')
        screen.blit(player_sprite, (x_ultimo+16*5, y + 16))
        for i in range(qte_combinacoes):
            if self.dados == None:
                sprite = empty_sprite
            else:
                if self.dados[2]== None:
                    sprite = empty_sprite
                elif self.dados[2]:
                    sprite = true_sprite
                else:
                    sprite = false_sprite
            screen.blit(sprite, (x_ultimo + 16*7, y + 16*(3 + i*3)))

        #type 1 tudo certo [[(True, True), True, True, True], [(True, False), False, False, True], [(False, True), False, False, True], [(False, False), False, False, True]]
        #type 2 circuito errado
        #type 3 mais de 1 output[[(True,), False, None, False], [(False,), True, None, False]]

    def render_info_fase (self, screen): #pode mover esse metodo pra classe Jogo dps, acho que fica melhor
        qte_fases = len(self.fases)
        atual = self.fase_atual
        fase_atual = self.fases[atual]

        #bara de progresso
        sprite_barra = pygame.image.load('assets/fase/barra_total.png').convert_alpha()
        sprite_progresso = pygame.image.load('assets/fase/barra_progresso.png').convert_alpha()
        x = W - 16 - sprite_barra.get_width()
        y = 16
        screen.blit(sprite_barra, (x, y))
        sprite_progresso_atual = pygame.transform.scale(sprite_progresso,(sprite_barra.get_width()*atual/qte_fases, sprite_barra.get_height()))
        screen.blit(sprite_progresso_atual, (x + sprite_barra.get_width() - sprite_progresso_atual.get_width(), y))

        text = f'fase {atual+1}: crie um {f'{fase_atual.nome}'.upper()}'
        text_surface = font.render(text, True, config.branco)
        screen.blit(text_surface, (16*2,8))

#sprites
sprite_board = pygame.image.load('assets/celula_board.png').convert_alpha()
fundo = pygame.image.load('assets/borda_tabuleiro.png').convert_alpha()
sprite_iven = pygame.image.load('assets/celula_iven.png').convert_alpha()
title = pygame.image.load('assets/title.png').convert_alpha()

#board
board = Board(880, 528, 11, 11, sprite_board, fundo)
boardX = 16*3
boardY = 16*5

#inventário e ferramentas
inven_lista = [Input, Output, Not, And]
inven = Inventario(1170, 64, 1, 10, sprite_board, inven_lista)
ferramentas_lista = [tools.borracha, tools.conectar, tools.testar, tools.finalizar]
ferramentas = Inventario(320, board.identificar_cell(0,0).altura*(len(inven_lista)), len(inven_lista), 1, sprite_iven, ferramentas_lista)

#opcoes para quando estiver pausado
opcoes_lista = [tools.continuar, tools.reiniciar, tools.sair]
opcoes = Inventario(320, board.identificar_cell(0,0).altura*(len(opcoes_lista)), len(opcoes_lista), 1, sprite_iven, opcoes_lista)

#fases
fase_not = Fase([Input, Output, Not, And], {Input:1, Output:1}, Not, "Not")
fase_and = Fase([Input, Output, Not, And], {Input:2, Output:1}, And, "And")
fase_nand = Fase([Input, Output, Not, And], {Input:2, Output:1}, Nand, "Nand")
fase_or = Fase([Input, Output, Not, And, Nand], {Input:2, Output:1}, Or, "Or")
fase_xor = Fase([Input, Output, Not, And, Nand, Or], {Input:2, Output:1}, Xor, "Xor")
fase_and2 = Fase([Input, Output, Nand], {Input:2, Output:1}, Xor, "And")

fases = [fase_and, fase_nand, fase_or, fase_xor, fase_not]
fases = [fase_and, fase_nand]
fase_atual = 0

#tabela
tabela = Tabela(board, fases, fase_atual)

#ações de execução
def carregar_fase(fase:Fase):
    board.reset()
    tools.finalizar.desativar()
    inven.atualizar(fases[fase_atual].inventario)
    tabela.atualizar(fase)

def render_fase():
    screen.fill(config.preto)
    board.render(screen, boardX, boardY)
    board.avaliar_conexoes()
    board.render_conexoes(screen)
    board.render_portas(screen)
    inven.render(screen, boardX - 16, boardY + board.altura + 16*2)
    ferramentas.render(screen, boardX + board.largura + 16*2, board.altura - ferramentas.altura + 16*4)
    tabela.simular()
    tabela.render(screen, boardX + board.largura + 16*2, board.altura - ferramentas.altura + 16*4 )
    tabela.render_info_fase(screen)

def render_menu():
    sprites = ['assets/iniciar1.png', 'assets/iniciar2.png'] #queria fazer pra ficar mudando mas deu preguiça
    iniciar = pygame.image.load(sprites[0]).convert_alpha()
    screen.fill(config.azul_escuro)
    screen.blit(title, ((W-title.get_width())//2, H//2-title.get_height()//2))
    screen.blit(iniciar, ((W-iniciar.get_width())//2, H//2-title.get_height()//2 +  title.get_height()))

def render_pause():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if opcoes.selecionar_cell(pos):
                opcao = opcoes.selecionar_cell(pos)
                match opcao.valor:
                    case "continuar":
                        pass
                    case "reiniciar":
                        fase_atual = 0
                    case "sair":
                        running = False
    render_fase()
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    screen.blit(overlay, (0, 0))
    opcoes.render(screen, (W-opcoes.largura)//2, (H-opcoes.altura)//2)

def render_fim():
    screen.fill(config.azul_escuro)
    text = f'fim'
    text_surface = font.render(text, True, config.branco)
    screen.blit(text_surface, (W//2, H//2))

#variaveis de controle da execução
selecionado = None
origem = None
running = True
estado = "menu"

#rodando o programa
while running:
    #checar selecionado

    for i in ferramentas_lista:
        if selecionado:
            if selecionado.valor==i.nome:
                i.selecionar()
            else:
                i.descelecionar()
        else:
            i.descelecionar()

    match estado:
        case "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    fase_atual = 0
                    carregar_fase(fase_atual)
                    estado = "fase"
            render_menu()

        case "fase":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        estado = "pause"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # pegar a posição do mouse
                    pos = pygame.mouse.get_pos()
                    # selecionar no board indicado
                    if board.selecionar_cell(pos):
                        if board.selecionar_cell(pos).vazio:
                            if selecionado:
                                if selecionado.porta:
                                    board.selecionar_cell(pos).inserir_porta(selecionado.porta(board.selecionar_cell(pos)))
                        else:
                            if selecionado:
                                if selecionado.valor=="borracha":
                                    board.limpar_cell(board.selecionar_cell(pos))
                                elif selecionado.valor=="conectar":
                                    if not origem:
                                        origem = board.selecionar_cell(pos).porta
                                    else:
                                        destino = board.selecionar_cell(pos).porta
                                        board.conectar(origem, destino)
                                        origem = None
                                elif selecionado.valor=="testar":
                                    if isinstance(board.selecionar_cell(pos).porta, Input):
                                        board.selecionar_cell(pos).porta.switch()
                    elif ferramentas.selecionar_cell(pos):
                        selecionado = ferramentas.selecionar_cell(pos)
                        if selecionado.valor=="finalizar":
                            if fases[fase_atual].vitoria:
                                fase_atual +=1
                                som_finalizar.play()
                                if fase_atual >= len(fases):
                                    estado="fim"
                                    pygame.mixer.music.stop()
                                    pygame.mixer.music.load('assets/audio/fim.mp3')
                                    pygame.mixer.music.play()
                                else:
                                    carregar_fase(fase_atual)
                    elif inven.selecionar_cell(pos):
                        selecionado = inven.selecionar_cell(pos)
                    else:
                        selecionado = None
            if estado=="fase":
                if fases[fase_atual].vitoria:
                    tools.finalizar.ativar()
                else:
                    tools.finalizar.desativar()
                render_fase()

        case "pause":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if opcoes.selecionar_cell(pos):
                        opcao = opcoes.selecionar_cell(pos)
                        match opcao.valor:
                            case "continuar":
                                estado = "fase"
                            case "reiniciar":
                                fase_atual = 0
                                carregar_fase(fase_atual)
                                estado = "fase"
                            case "sair":
                                running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        estado = "fase"
            render_pause()

        case "fim":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            render_fim()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
tabela.render_text()