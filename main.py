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
        self.estado = False
        self.cor = vermelho

    def conectar(self, entrada, saida):
        self.entradas.append(entrada)
        self.saidas.append(saida) 

class Input(Porta):
    nome = "IN"
    qte_entradas = 0
    pode_saida = True
    def switch(self):
        self.estado = not self.estado
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor
    def avaliar(self):
        return
    
class Output(Porta):
    nome = "OUT"
    qte_entradas = 1
    pode_saida = False
    def avaliar(self):
        if len(self.entradas)==1:
            self.estado = self.entradas[0].estado
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class And(Porta):
    nome = "AND"
    qte_entradas = 2
    pode_saida = True
    def avaliar(self):
        if len(self.entradas)==2:
            self.estado = self.entradas[0].estado and self.entradas[1].estado
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class Not(Porta):
    nome = "NOT"
    qte_entradas = 1
    pode_saida = True
    def avaliar(self):
        if len(self.entradas)==1:
            self.estado = not self.entradas[0].estado
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class Or(Porta):
    nome = "OR"
    qte_entradas = 2
    pode_saida = True
    def avaliar(self):
        if len(self.entradas)==2:
            self.estado = self.entradas[0].estado or self.entradas[1].estado
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

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
        self.valor = None
    
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
        self.valor = None

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
        self.portas_ativas = []

    def render(self, screen, x, y): #desenhar o grid
        self.x = x
        self.y = y
        pygame.draw.rect(screen, self.corBorda, rect=(x, y, self.largura, self.altura)) #desenhar as bordas/fundo
        for li in range(self.linhas):
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                celula.x = x + (celula.largura + self.borda) * col
                celula.y = y + (celula.altura + self.borda) * li
                bloco = pygame.Rect((celula.x, celula.y, celula.largura, celula.altura))
                pygame.draw.rect(screen, celula.cor, bloco)

    def render_portas(self,screen):
        for li in range(self.linhas):
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                if celula.porta:
                    bloco = pygame.Rect((celula.x, celula.y, celula.largura, celula.altura))
                    pygame.draw.rect(screen, celula.cor, bloco)
                
                    text = celula.porta.nome
                    text_surface = font.render(text, True, branco)
                    text_rect = text_surface.get_rect()
                    text_rect.center = bloco.center
                    screen.blit(text_surface, text_rect)

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

    def limpar(self, cell:Celula):

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
            and c.destino != porta
        ]

        if porta in self.portas_ativas:
            self.portas_ativas.remove(porta) #remover porta da lista de portas ativas
        cell.limpar() #limpar a celula, porta, cor, vazio, valor

    def avaliar_conexoes(self):
        for porta in self.portas_ativas:
            porta.avaliar()

    def render_conexoes(self, screen):
        for conexao in self.conexoes:

            origem = conexao.origem.celula
            destino = conexao.destino.celula

            x1 = origem.x + origem.largura - 10
            y1 = origem.y + origem.altura/2

            x2 = destino.x + 10
            y2 = destino.y + destino.altura/2

            if origem.porta.estado:
                cor = verde
            else:
                cor = vermelho

            pygame.draw.line(
            screen,
            cor,
            (x1,y1),
            (x2,y2),
            10
            )

class Inventario(Grid): #vou ter q refazer esse aqui tudo provavelmente RIP
    def render(self, screen, x, y):
        portas = [Input, Output, And, Not, Or]
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
                    text = "borracha"
                    celula.valor = "borracha"
                    celula.cor = vermelho
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

class Fase():
    def __init__(self, inventario, limites, objetivo):
        pass

class Tabela_verdade():
    def __init__(self, inputs, outputs):
        pass

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
            if board.selecionar_cell(pos):
                if board.selecionar_cell(pos).vazio:
                    if selecionado:
                        if selecionado.porta:
                            board.selecionar_cell(pos).inserir_porta(selecionado.porta(board.selecionar_cell(pos)))
                else:
                    if selecionado:
                        if selecionado.valor=="borracha":
                            board.limpar(board.selecionar_cell(pos))
                        elif not origem:
                            origem = board.selecionar_cell(pos).porta
                        else:
                            destino = board.selecionar_cell(pos).porta
                            board.conectar(origem, destino)
                            origem = None
                    else:
                        if isinstance(board.selecionar_cell(pos).porta, Input):
                            board.selecionar_cell(pos).porta.switch()

            elif inven.selecionar_cell(pos):
                selecionado = inven.selecionar_cell(pos)
            else:
                selecionado = None

    board.render(screen, boardX, boardY)
    board.avaliar_conexoes()
    board.render_conexoes(screen)
    board.render_portas(screen)
    inven.render(screen, boardX, boardY + board.altura + 10)

    pygame.display.flip()

pygame.quit()