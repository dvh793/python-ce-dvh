class Cliente:
    """Cliente de Alisios Renovables."""

    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo
        self.pedidos = []            # siempre empieza vacío: no es un parámetro

    def registrar_pedido(self, Pedido):
        self.pedidos.append(Pedido)

    def gasto_total(self):
        return sum(p.importe for p in self.pedidos)

c = Cliente("Ana Pérez", "ana@correo.es")   # los argumentos van a __init__
#c.registrar_pedido(120.0)
#print(c.nombre, c.correo, c.pedidos, c.gasto_total())
#print(vars(c))


class Pedido:
    """Pedido de Alisios Renovables."""

    def __init__(self, importe, concepto="varios"):
        self.importe = importe
        self.concepto = concepto
        self.pagado = False
        
p1 = Pedido(120.0, "instalación de paneles")
p2 = Pedido(80.5, "mantenimiento")
p3 = Pedido(900)
print(vars(p1), vars(p2), vars(p3))
c.registrar_pedido(p1)
c.registrar_pedido(p2)
print(c.gasto_total())
