import pygame

class Porta():
    def __init__(self, celula):
        self.celula = celula
        self.entradas = []
        self.saidas = []
        self.estado = False

class Input(Porta):
    nome = "IN"
    qte_entradas = 0
    pode_saida = True
    sprite_ON = pygame.image.load('assets/portas/IN_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/IN_OFF.png').convert_alpha()
    sprite = sprite_OFF
    def switch(self):
        self.estado = not self.estado
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite
    def avaliar(self):
        return

class Output(Porta):
    nome = "OUT"
    qte_entradas = 1
    pode_saida = False
    sprite_ON = pygame.image.load('assets/portas/OUT_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/OUT_OFF.png').convert_alpha()
    sprite = sprite_OFF
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.entradas[0].estado
        else:
            self.estado = False
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite

class And(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "AND"
    pode_saida = True
    sprite_ON = pygame.image.load('assets/portas/AND_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/AND_OFF.png').convert_alpha()
    sprite = sprite_OFF
    @staticmethod
    def avaliacao(a,b):
        return a and b
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite

class Not(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 1
    nome = "NOT"
    pode_saida = True
    sprite_ON = pygame.image.load('assets/portas/NOT_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/NOT_OFF.png').convert_alpha()
    sprite = sprite_OFF
    @staticmethod
    def avaliacao(a):
        return not a
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado)
        else:
            self.estado = False
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite

class Or(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "OR"
    pode_saida = True
    sprite_ON = pygame.image.load('assets/portas/OR_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/OR_OFF.png').convert_alpha()
    sprite = sprite_OFF
    @staticmethod
    def avaliacao(a,b):
        return a or b
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite

class Xor(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "XOR"
    pode_saida = True
    sprite_ON = pygame.image.load('assets/portas/XOR_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/XOR_OFF.png').convert_alpha()
    sprite = sprite_OFF
    @staticmethod
    def avaliacao(a,b):
        return (a or b) and not(a and b)
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite

class Nand(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "NAND"
    pode_saida = True
    sprite_ON = pygame.image.load('assets/portas/NAND_ON.png').convert_alpha()
    sprite_OFF = pygame.image.load('assets/portas/NAND_OFF.png').convert_alpha()
    sprite = sprite_OFF
    @staticmethod
    def avaliacao(a,b):
        return not(a and b)
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.sprite = self.sprite_ON
        else:
            self.sprite = self.sprite_OFF
        self.celula.sprite = self.sprite