class Feramenta():
    def __init__(self, nome, cor):
        self.estado = True
        self.nome = nome
        self.cor = cor

    def ativar_uso(self):
        self.estado = True