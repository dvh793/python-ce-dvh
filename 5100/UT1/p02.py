# p02.py · usar gestor_v0 desde fuera y romperlo sin querer
import gestor_v0 as g

g.alta("Ana Pérez", "ana@correo.es")
g.registrar_pedido("ana@correo.es", 120.0)
g.registrar_pedido("ana@correo.es", 80.5)
print(g.gasto_total("ana@correo.es"))

g.agenda["ana@correo.es"]["pedidos"] = "borrado sin querer"   # nadie lo impide
print(g.gasto_total("ana@correo.es"))

nombre = "alisios renovables"
pedidos = [120.0, 80.5]

print(type(nombre), type(pedidos))
print(nombre.title())          # un método del objeto str
pedidos.append(45.0)           # un método del objeto list: cambia el estado de la lista
print(len(pedidos), pedidos)
print(type(len), type(type))   # hasta las funciones y las clases son objetos

# EMPRESA *da de alta* CLIENTES con su CORREO; cada CLIENTE *registra* PEDIDOS
# con un IMPORTE y la EMPRESA quiere *listar* los CLIENTES ordenados por GASTO.
#
#EMPRESA
#clientes[]
#alta(),listar()
#CLIENTE
#nombre, correo, pedidos
#crear_pedido(),total_pedidos(),
#PEDIDO
#importe