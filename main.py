import pygame
import sys

pygame.init()

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
class Celula():
    def __init__(self, cor, largura, altura):
        self.valor = None
        self.vazio = True
        self.largura = largura
        self.altura = altura
        self.cor = cor
    
    def inserir_valor(self, valor):
        self.valor = valor
        self.cor = vermelho
        self.vazio = False

    def mudar(self):
        self.vazio = not self.vazio
        if not self.vazio:
            self.cor = verde
        else:
            self.cor = azul
            self.valor = None
    def limpar(self):
        self.valor = None
        self.cor = azul

class Board():
    def __init__(self, largura, altura, linhas, colunas, corBloco, corBorda):
        self.linhas = linhas
        self.colunas = colunas
        self.largura = largura
        self.altura = altura
        self.borda = 0
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
    
    def render(self, screen, x, y): #desenhar o grid
        self.x = x
        self.y = y
        pygame.draw.rect(screen, self.corBorda, rect=(x, y, self.largura, self.altura)) #desenhar as bordas/fundo
        for li in range(self.linhas): #celulas
            for col in range(self.colunas):
                celula = self.identificar_cell(li, col)
                xCell = x + (celula.largura + self.borda) * col
                yCell = y + (celula.altura + self.borda) * li
                bloco = pygame.Rect((xCell, yCell, celula.largura, celula.altura))
                pygame.draw.rect(screen, celula.cor, bloco)
                if celula.valor:
                    text = celula.valor
                    text_surface = font.render(text, True, branco)
                    text_rect = text_surface.get_rect()
                    text_rect.center = bloco.center
                    screen.blit(text_surface, text_rect)
    
    def selecionar_cell(self, pos):
            # converter as cordenadas x/y da tela para cordenadas do tabuleiro
            col = (pos[0] - self.x)//(self.identificar_cell(0,0).largura + self.borda)
            li = (pos[1] - self.y)//(self.identificar_cell(0,0).altura + self.borda)
            # mudar a cor da célula selecionada
            if 0 <= li < self.linhas and 0 <= col < self.colunas:
                #self.identificar_cell(int(li), int(col)).mudar()
                return self.identificar_cell(int(li), int(col))

class Inventario(Board):
    def render_inven(self, screen, x, y):
        portas = ['AND', 'NOT', 'IN', 'OUT']
        #fios = ['horizontal', 'vertical', 'LtT', 'LtB', 'RtT', 'RtB']
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
                #escolher fio/porta
                if i < len(portas):
                    text = portas[i]
                else:
                    text = '--'
                i+=1
                #atualizar atributos na célula
                celula.inserir_valor(text)
                #renderizar texto em uma superfice
                text_surface = font.render(text, True, branco)
                #alinhas texto ao retantgulo 
                text_rect = text_surface.get_rect()
                text_rect.center = bloco.center
                #desenhar retangulo de fundo
                pygame.draw.rect(screen, celula.cor, bloco)
                #desenhar text surface em cima do retangulo
                screen.blit(text_surface, text_rect)
    def selecionado(self, cell):
        pass

#criando os objetos - grid
grid = Board(900, 600, 11, 8, azul, preto)
gridX = 20
gridY = 30

# cell = grid.identificar_cell(0,0)
# cell.inserir_valor('AND')
# grid.identificar_cell(7,3).inserir_valor('NOT')

#criando os objetos - inventário
inven = Inventario(1120, grid.identificar_cell(0,0).altura, 1, 10, azul, preto)
selecionado = None

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
            if grid.selecionar_cell(pos):
                if grid.selecionar_cell(pos).vazio:
                    if selecionado:
                        grid.selecionar_cell(pos).inserir_valor(selecionado.valor)
                    else:
                        grid.selecionar_cell(pos).mudar()
                else:
                    grid.selecionar_cell(pos).mudar()
            elif inven.selecionar_cell(pos):
                selecionado = inven.selecionar_cell(pos)
            else:
                selecionado = None

    grid.render(screen, gridX, gridY)
    inven.render_inven(screen, gridX, gridY + grid.altura + 10)

    pygame.display.flip()

pygame.quit()

'''

'''
    