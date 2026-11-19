class Cliente:

    def __init__(self, nombre):
        self.nombre = nombre
        self.pedidos = []            # siempre empieza vacío: no es un parámetro

pepe = Cliente("Pepe")
activos = [pepe]
morosos = [pepe]
activos[0].pedidos.append(1000)
print(morosos[0].pedidos)
print(activos[0] is morosos[0]) # Apuntan al mismo objeto

jose = Cliente("Jose")
morosos[0] = jose
activos[0].pedidos.append(2000)
print(activos[0].pedidos)
print(morosos[0].pedidos) # Jose no tiene pedidos, no apunta al mismo objeto que Pepe
print(activos[0] is morosos[0]) # Apuntan a objetos distintos