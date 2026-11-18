#class Cliente:
#    """Cliente de Alisios Renovables (todavía sin métodos propios)."""

#c = Cliente()
#c.nombre = "Ana Pérez"
#c.pedidos = [120.0]

#print(type(c))                    # de qué clase es
#print(type(c).__name__)           # solo el nombre, sin adornos
#print(isinstance(c, Cliente), isinstance(c, str))
#print(vars(c))                    # atributos ahora mismo (= c.__dict__)
#print([n for n in dir(c) if not n.startswith("__")])   # tras el punto
#print(Cliente.__doc__)            # el docstring de la clase

#pedidos = [120.0, 80.5]
#print(type(pedidos).__name__, isinstance(pedidos, list))
#print([n for n in dir(pedidos) if not n.startswith("__")])
#help(pedidos.append)


class Cliente:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo
        self.pedidos = []

    def registrar_pedido(self, importe):
        self.pedidos.append(importe)

c = Cliente("Ana Pérez", "ana@correo.es")
c.registrar_pedido(120.0)
print(vars(c))