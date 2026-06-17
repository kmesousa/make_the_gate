class gates():
    def __init__(self, name):
        #pode ser alterado pelo player
        self.name = name #string
        self.state = False #bool ON OFF 
        #nao pode ser alterado
    def switch(self):
        self.state = not self.state

notGate = gates('not')

print(notGate.state)
print(notGate.name)


notGate.switch()
print(notGate.state)

AND = lambda a, b: a and b
oi = AND(True, False)
print(oi)