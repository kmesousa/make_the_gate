import pygame ; pygame.init()

#cores
vermelho = (255, 0, 0)
verde = (40, 160, 30)
azul = (0, 0, 255)
branco = (255, 255, 255)
preto = (0, 0, 0)

#configurações
W = 1280
H = 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('make the gate')
font = pygame.font.SysFont("Arial", 30)

#classes
class Porta():
    def __init__(self, celula):
        self.celula = celula
        self.entradas = []
        self.saidas = []

    def conectar(self, entrada, saida):
        self.entradas.append(entrada)
        self.saidas.append(saida) 

    def atualizar(self): #eu acho ????
        pass

class Input(Porta):
    nome = "IN"
    qte_entradas = 0
    #qte_saidas = 1

class Output(Porta):
    nome = "OUT"
    qte_entradas = 1
    qte_saidas = 0

class And(Porta):
    nome = "AND"
    qte_entradas = 2
    #qte_saidas = 1

class Not(Porta):
    nome = "NOT"
    qte_entradas = 1
    #qte_saidas = 1

class Conexao():
    def __init__(self, origem, destino):
        self.origem = origem
        self.destino = destino

class Celula():
    def __init__(self, cor, largura, altura):
        self.largura = largura
        self.altura = altura
        self.x = 0
        self.y = 0
        self.cor = cor
        self.vazio = True
        self.porta = None
    
    def inserir_porta(self, porta:Porta):
        self.porta = porta
        self.cor = vermelho
        self.vazio = False

    def checar(self):
        self.vazio = not self.vazio
        if not self.vazio:
            self.cor = verde
        else:
            self.cor = azul
            self.valor = None

    def limpar(self):
        self.vazio = True
        self.cor = azul
        self.porta = None

class Grid():
    def __init__(self, largura, altura, linhas, colunas, corBloco, corBorda):
        self.linhas = linhas
        self.colunas = colunas
        self.largura = largura
        self.altura = altura
        self.borda = 1
        self.corBloco = corBloco
        self.corBorda = corBorda

        #células
        larguraCell = largura/colunas - self.borda
        alturaCell = altura/linhas - self.borda

        #matriz do tabuleiro com as células
        self.matriz = [] # self.matrix = list[list[Celula]]
        for i in range(linhas):
            self.matriz.append([])
            for j in range(colunas):
                self.matriz[i].append(Celula(self.corBloco, larguraCell, alturaCell))

    def identificar_cell (self, li, col)-> Celula:
        return self.matriz[li][col]
    
    def checar(self): #imprimir a matriz
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                print(self.matriz[i][j].valor, end=' ')
            print('')
    
    def selecionar_cell(self, pos):
            # converter as cordenadas x/y da tela para cordenadas do tabuleiro
            col = (pos[0] - self.x)//(self.identificar_cell(0,0).largura + self.borda)
            li = (pos[1] - self.y)//(self.identificar_cell(0,0).altura + self.borda)
            # mudar a cor da célula selecionada
            if 0 <= li < self.linhas and 0 <= col < self.colunas:
                #self.identificar_cell(int(li), int(col)).mudar()
                return self.identificar_cell(int(li), int(col))
            
class Board(Grid):
    def __init__(self, largura, altura, linhas, colunas, corBloco, corBorda):
        super().__init__(largura, altura, linhas, colunas, corBloco, corBorda)
        #conexões entre blocos
        self.conexoes = []

    def render(self, screen, x, y): #desenhar o grid
        self.x = x
        self.y = y
        pygame.draw.rect(screen, self.corBorda, rect=(x, y, self.largura, self.altura)) #desenhar as bordas/fundo
        for li in range(self.linhas): #celulas
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                celula.x = x + (celula.largura + self.borda) * col
                celula.y = y + (celula.altura + self.borda) * li
                bloco = pygame.Rect((celula.x, celula.y, celula.largura, celula.altura))
                pygame.draw.rect(screen, celula.cor, bloco)
                if celula.porta:
                    text = celula.porta.nome
                    text_surface = font.render(text, True, branco)
                    text_rect = text_surface.get_rect()
                    text_rect.center = bloco.center
                    screen.blit(text_surface, text_rect)

    def conectar(self, origem, destino):
        if origem == destino:
            #print('nao conectou 1')
            return
        if len(destino.entradas) >= destino.qte_entradas:
            #print('nao conectou 2')
            return
        nova = Conexao(origem, destino)
        self.conexoes.append(nova)
        destino.entradas.append(origem)
        origem.saidas.append(destino)
        #print('conectou!')

    def limpar(self, cell:Celula):

        porta = cell.porta

        for entrada in porta.entradas: #remover a porta da lista de entrada de outras portas
            entrada.saidas.remove(porta)

        for saida in porta.saidas: #remover a porta da lista de saida de outras portas
            saida.entradas.remove(porta)

        #refazer a lista de conexoes excluindo as que tenham a porta removida como entrada ou saída
        board.conexoes = [
            c for c in board.conexoes
            if c.origem != porta
            and c.destino != porta
        ]

        cell.limpar() #limpar a celula

    def render_conexoes(self, screen):
        for conexao in self.conexoes:

            origem = conexao.origem.celula
            destino = conexao.destino.celula

            x1 = origem.x + origem.largura
            y1 = origem.y + origem.altura/2

            x2 = destino.x
            y2 = destino.y + destino.altura/2

            pygame.draw.line(
            screen,
            branco,
            (x1,y1),
            (x2,y2),
            3
            )

class Inventario(Grid): #vou ter q refazer esse aqui tudo provavelmente RIP
    def render(self, screen, x, y):
        portas = [Input, Output, And, Not]
        i = 0
        self.x = x
        self.y = y
        pygame.draw.rect(screen, self.corBorda, rect=(x, y, self.largura, self.altura)) #desenhar as bordas/fundo
        for li in range(self.linhas): #celulas
            for col in range(self.colunas):
                #retangulo
                celula = self.identificar_cell(li, col)
                xCell = x + (celula.largura + self.borda) * col
                yCell = y + (celula.altura + self.borda) * li
                bloco = pygame.Rect((xCell, yCell, celula.largura, celula.altura))
                #escolher porta
                if i < len(portas):
                    text = portas[i].nome
                    celula.inserir_porta(portas[i])
                else:
                    text = ''
                i+=1
                #renderizar texto em uma superfice
                text_surface = font.render(text, True, branco)
                #alinhas texto ao retantgulo 
                text_rect = text_surface.get_rect()
                text_rect.center = bloco.center
                #desenhar retangulo de fundo
                pygame.draw.rect(screen, celula.cor, bloco)
                #desenhar text surface em cima do retangulo
                screen.blit(text_surface, text_rect)

#criando os objetos - grid
board = Board(900, 600, 11, 8, azul, preto)
boardX = 20
boardY = 30

#criando os objetos - inventário
inven = Inventario(1120, board.identificar_cell(0,0).altura, 1, 10, azul, preto)
selecionado = None
origem = None

#rodando o programa
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pegar a posição do mouse
            pos = pygame.mouse.get_pos()
            # selecionar no board indicado
            if board.selecionar_cell(pos): #tenho que mudar isso aqui depois
                if board.selecionar_cell(pos).vazio:
                    if selecionado:
                        #grid.selecionar_cell(pos).inserir_valor(selecionado.valor)
                        board.selecionar_cell(pos).inserir_porta(selecionado.porta(board.selecionar_cell(pos)))
                else:
                    if not selecionado:
                        #board.selecionar_cell(pos).limpar()
                        board.limpar(board.selecionar_cell(pos))
                    elif not origem:
                        origem = board.selecionar_cell(pos).porta
                    else:
                        destino = board.selecionar_cell(pos).porta
                        board.conectar(origem, destino)
                        origem = None
            elif inven.selecionar_cell(pos):
                selecionado = inven.selecionar_cell(pos)
            else:
                selecionado = None

    board.render(screen, boardX, boardY)
    board.render_conexoes(screen)
    inven.render(screen, boardX, boardY + board.altura + 10)

    pygame.display.flip()

pygame.quit()