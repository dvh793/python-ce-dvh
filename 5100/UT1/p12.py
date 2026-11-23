class Pedido:

    def __init__(self,importe,concepto="varios"):
         self.importe = importe
         self.concepto = concepto
    def __str__(self):
        return f"{self.concepto}: {self.importe} €"
    def __repr__(self):                 # para programadores: el intérprete, las listas, el depurador
            return f"Pedido({self.importe}, {self.concepto.lower()!r})"

class Cliente:
    def __init__(self, nombre, correo):
        self.nombre, self.correo, self.pedidos = nombre, correo, []

    def gasto_total(self):
        return sum(p.importe for p in self.pedidos)
    
    def __str__(self):                  # para personas: lo usan print() y str()
        return f"{self.nombre} - {self.gasto_total():.2f} €"
    
    def __len__(self):                  # lo usa len()
        return len(self.pedidos)

p = Pedido(100,"papas")
p2 = Pedido(100)
print(p) #str
print([p]) #repr

c = Cliente("Pepe","pepe@pepe.pepe")
c.pedidos = [p,p2]
print(c)
print(len(c))

