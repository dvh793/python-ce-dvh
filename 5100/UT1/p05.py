class Cliente:
    def presentar(self):
        return f"{self.nombre} <{self.correo}>"

    def registrar_pedido(self, importe):
        self.pedidos.append(importe)

    def gasto_total(self):
        return sum(self.pedidos)

    def numero_pedidos(self):
        return len(self.pedidos)

    def pedido_mayor(self):
        return max(self.pedidos)

    def categoria(self):
        total = self.gasto_total
        if total >= 1000:
            return "oro"
        elif total >= 500:
            return "plata"
        else:
            return "bronce"

c = Cliente()
c.nombre, c.correo, c.pedidos = "Ana Pérez", "ana@correo.es", []
c.registrar_pedido(120.0)
c.registrar_pedido(80.5)
c.registrar_pedido(900)

print(c.numero_pedidos())
print(c.pedido_mayor())
print(c.categoria())
