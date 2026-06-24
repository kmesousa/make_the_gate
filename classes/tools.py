import pygame

class Tool():
    def __init__(self, nome, spriteON, usar:bool, selecionavel, spriteOFF=None):
        self.nome = nome
        self.usar = usar
        self.selecionavel = selecionavel
        self.spriteON = spriteON
        self.spriteOFF = spriteOFF
        if usar:
            self.sprite = spriteON
        else:
            self.sprite = spriteOFF
        self.selecionado = False

    def ativar(self):
        self.usar = True
        self.sprite = self.spriteON

    def desativar(self):
        self.usar = False
        self.sprite = self.spriteOFF

    def selecionar(self):
        if self.selecionavel:
            self.selecionado = True

    def descelecionar(self):
        self.selecionado = False

limpar_tudo = Tool("limpar_tudo", pygame.image.load('assets/tools/LIMPAR_TUDO.png').convert_alpha(), True, False) #NOT DEFINED
borracha = Tool("borracha", pygame.image.load('assets/tools/BORRACHA.png').convert_alpha(), True, True)
conectar = Tool("conectar", pygame.image.load('assets/tools/CONECTAR.png').convert_alpha(), True, True)
testar = Tool("testar", pygame.image.load('assets/tools/TESTAR.png').convert_alpha(), True, True)
finalizar = Tool("finalizar", pygame.image.load('assets/tools/FINALIZAR_ON.png').convert_alpha(), False, False, pygame.image.load('assets/tools/FINALIZAR_OFF.png').convert_alpha())
tools_lista = [borracha, conectar, testar, finalizar]

continuar = Tool("continuar", pygame.image.load('assets/opcoes/CONTINUAR.png').convert_alpha(), True, False)
reiniciar = Tool("reiniciar", pygame.image.load('assets/opcoes/REINICIAR.png').convert_alpha(), True, False)
#controles = Tool("controles", pygame.image.load('assets/opcoes/REINICIAR.png').convert_alpha(), True)
sair = Tool("sair", pygame.image.load('assets/opcoes/SAIR.png').convert_alpha(), True, False)
opcoes_lista = [conectar, reiniciar , sair]