class Pedido:
    IGIC = 0.07
    emitidos = 0
    
    def __init__(self, importe):
        self.importe = importe
        Pedido.emitidos += 1
    
    def total(self):
        return round(self.importe * (1 + Pedido.IGIC), 2)
        
p1 = Pedido(100)
p2 = Pedido(200)
p3 = Pedido(300)
print(Pedido.emitidos)
print(vars(p1))
print(vars(p2))
print(vars(p3))
Pedido.IGIC = 0.03
print(p1.total())
print(p2.total())
print(p3.total())
