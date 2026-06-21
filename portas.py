from config import verde, vermelho

class Porta():
    def __init__(self, celula):
        self.celula = celula
        self.entradas = []
        self.saidas = []
        self.estado = False
        self.cor = vermelho

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
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.entradas[0].estado
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class And(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "AND"
    pode_saida = True
    @staticmethod
    def avaliacao(a,b):
        return a and b
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class Not(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 1
    nome = "NOT"
    pode_saida = True
    @staticmethod
    def avaliacao(a):
        return not a
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado)
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class Or(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "OR"
    pode_saida = True
    @staticmethod
    def avaliacao(a,b):
        return a or b
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class Xor(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "XOR"
    pode_saida = True
    @staticmethod
    def avaliacao(a,b):
        return (a or b) and not(a and b)
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor

class Nand(Porta):
    def __init__(self, celula):
        super().__init__(celula)
        self.qte_entradas = 2
    nome = "NAND"
    pode_saida = True
    @staticmethod
    def avaliacao(a,b):
        return not (a and b)
    def avaliar(self):
        if len(self.entradas)==self.qte_entradas:
            self.estado = self.avaliacao(self.entradas[0].estado, self.entradas[1].estado)
        else:
            self.estado = False
        if self.estado:
            self.cor = verde
        else:
            self.cor = vermelho
        self.celula.cor = self.cor