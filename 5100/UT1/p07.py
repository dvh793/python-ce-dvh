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
        if not isinstance(importe, (int, float)) or importe < 0:
            raise ValueError("El importe debe ser numérico y no negativo")
        self.importe = importe
        concepto = concepto.strip()
        if not concepto:
            self.concepto = "varios"
        else:
            self.concepto = concepto
        self.pagado = False
        
try:
    p1 = Pedido(-5, "instalación de paneles") #Error: El importe es negativo
except ValueError as e:
    print("Error:", e)

try:
    p2 = Pedido("120", "instalación de paneles") #Error: El importe no es numérico
except ValueError as e:
    print("Error:", e)
    
try:
    p3 = Pedido(900) #Correcto: El importe es positivo y el concepto es opcional
except ValueError as e:
    print("Error:", e)
