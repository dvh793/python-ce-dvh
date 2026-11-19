class Cliente:
    """Cliente de Alisios Renovables."""
    
    total_clientes = 0

    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo
        self.pedidos = []
        Cliente.total_clientes += 1
        
    @classmethod
    def desde_dict(cls, datos):
        cliente = cls(datos["nombre"], datos["correo"])
        for importe in datos["pedidos"]:
            cliente.registrar_pedido(importe)    
        return cliente

    def registrar_pedido(self, Pedido):
        self.pedidos.append(Pedido)

    def gasto_total(self):
        return sum(p.importe for p in self.pedidos)
    
    
datos = {"nombre": "Ana Pérez", "correo": "ana@correo.es", "pedidos": [120.0, 80.5]}
cliente = Cliente.desde_dict(datos)
print(cliente.nombre, cliente.pedidos, Cliente.total_clientes)