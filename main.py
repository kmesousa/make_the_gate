import pygame ; pygame.init()
import config
from portas import Porta, Input, Output, And, Not, Nand, Or, Xor

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
                cor = verde
            else:
                cor = vermelho
            pygame.draw.line(screen,cor,(x1,y1),(x2,y2),10)

    def reset(self):
        pass

class Inventario(Grid): #vou ter q refazer esse aqui tudo provavelmente RIP
    def __init__(self, largura, altura, linhas, colunas, corBloco, corBorda, itens):
        super().__init__(largura, altura, linhas, colunas, corBloco, corBorda)

        self.itens = itens

    def render(self, screen, x, y):
        i = 0
        self.x = x
        self.y = y
        portas = [Input, Output, Not, And, Or]
        pygame.draw.rect(screen, self.corBorda, rect=(x, y, self.largura, self.altura)) #desenhar as bordas/fundo
        for li in range(self.linhas): #celulas
            for col in range(self.colunas):
                #retangulo
                celula = self.identificar_cell(li, col)
                xCell = x + (celula.largura + self.borda) * col
                yCell = y + (celula.altura + self.borda) * li
                bloco = pygame.Rect((xCell, yCell, celula.largura, celula.altura))
                #escolher porta
                if i < len(self.itens):
                    if self.itens[i] in portas:
                        text = self.itens[i].nome
                        celula.inserir_porta(self.itens[i])
                    else:
                        text = self.itens[i]
                        celula.valor = self.itens[i]
                        celula.cor = verde
                else:
                    text = "-"
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
    def __init__(self, inventario:list[Porta], limites:dict[Porta:int], objetivo:Porta, nome:str):
        #inventario = [In, Out, Not], limites = [In: 2, Out: 1], objetivo = Nand
        self.inventario = inventario
        self.limites = limites
        self.objetivo = objetivo
        self.nome = nome
        self.vitoria = False

class Tabela():
    def __init__(self, board:Board, fase:Fase):
        self.board = board
        self.fase = fase
        self.resultados = []
        self.combinacoes = []
        self.avaliacao = fase.objetivo.avaliacao

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

        self.inputs = [] #pode ser os inputs atuais ou os inputs dados na fase
        self.outputs = []
        for porta in self.board.portas_ativas:
            if isinstance(porta, Input):
                self.inputs.append(porta)
            if isinstance(porta, Output):
                self.outputs.append(porta)

        if len(self.inputs)==0 or len(self.outputs)==0:
            return

        #combinacoes = gerar_combinacoes(len(self.inputs))
        combinacoes = gerar_combinacoes(self.fase.limites[Input])
        dados = []
        vitoria = True
        for i in range(len(combinacoes)):
            resultado = self.board.simular(combinacoes[i])
            desejado = self.avaliacao(*combinacoes[i])
            comparacao = resultado==desejado

            dados.append(combinacoes[i])
            dados.append(desejado)
            dados.append(resultado)
            dados.append(comparacao)
            if not comparacao:
                vitoria = False

        self.dados = dados
        self.fase.vitoria = vitoria

    def render(self, screen, x, y):
        print(self.dados)

#criando os objetos - grid
board = Board(900, 600, 11, 8, azul, preto)
boardX = 20
boardY = 30

#criando os objetos - inventário
inven_lista = [Input, Output, Not, And, Or]
inven = Inventario(1200, board.identificar_cell(0,0).altura, 1, 9, azul, preto, inven_lista )
ferramentas_lista = ["limpar", "conectar", "testar", "finalizar"]
ferramentas = Inventario(320, board.identificar_cell(0,0).altura*4, 4, 1, vermelho, preto, ferramentas_lista)
selecionado = None
origem = None

#fases
fase_not = Fase([Input, Output, Not, And], {Input:1, Output:1}, Not, "Fase 1: Not")
fase_and = Fase([Input, Output, Not, And], {Input:2, Output:1}, And, "Fase 2: And")
fase_nand = Fase([Input, Output, Not, And], {Input:2, Output:1}, Nand, "Fase 3: Nand")
fase_or = Fase([Input, Output, Not, And, Nand], {Input:2, Output:1}, Or, "Fase 4: Or")
fase_xor = Fase([Input, Output, Not, And, Nand, Or], {Input:2, Output:1}, Xor, "Fase 4: Xor")

fases = [fase_not, fase_and, fase_nand, fase_or, fase_xor]

fase = fases[0]

tabela = Tabela(board, fase)

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
                        if selecionado.valor=="limpar":
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
                        elif selecionado.valor=="finalizar":
                            if fase.vitoria:
                                running = False
            elif ferramentas.selecionar_cell(pos):
                selecionado = ferramentas.selecionar_cell(pos)
            elif inven.selecionar_cell(pos):
                selecionado = inven.selecionar_cell(pos)
            else:
                selecionado = None

    board.render(screen, boardX, boardY)
    board.avaliar_conexoes()
    board.render_conexoes(screen)
    board.render_portas(screen)
    inven.render(screen, boardX, boardY + board.altura + 10)
    ferramentas.render(screen, boardX + board.largura + 10, board.altura- ferramentas.altura)
    tabela.simular()

    pygame.display.flip()

pygame.quit()
print(tabela.dados)
print(fase.vitoria)