class Cliente:
    pass                       # cuerpo vacío, de momento

c = Cliente()                  # instanciamos: creamos un objeto llamando a la clase
print(type(c))

c.nombre = "Ana Pérez"         # atributos de instancia, creados "desde fuera"
c.correo = "ana@correo.es"
c.pedidos = []
print(c.nombre)
print(c.__dict__)              # el estado del objeto, tal cual lo guarda Python

c1 = Cliente()
c1.nombre = "Ana Pérez"
c2 = Cliente()
c2.nombre = "Luis Yeray"
c3 = c1                        # ¡no es un objeto nuevo!

print(c1.nombre, "|", c2.nombre, "|", c3.nombre)
print(c1 is c2, c1 is c3)      # identidad: ¿son el mismo objeto?

cliente1 = Cliente()
cliente1.nombre = "PEPE"
cliente1.correo = "pepe@pepe.pepe"
cliente1.pedidos = [10,50]

cliente2 = Cliente()
cliente2.nombre = "JOSE"
cliente2.correo = "jose@jose.jose"
cliente2.pedidos = []


print(cliente1.nombre,len(cliente1.pedidos))
print(cliente1.__dict__)

print(cliente2.nombre, len(cliente2.pedidos))
print(cliente2.__dict__)

print(cliente1 is cliente2)