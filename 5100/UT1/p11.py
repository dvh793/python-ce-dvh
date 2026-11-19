#registrar_pedido(importe) # metodo de instancia. recibe un importe y lo añade a la lista de pedidos
#desde_linea(linea) # metodo de clase. recibe una linea de texto y devuelve un cliente
#es_correo_valido(correo) # metodo estatico. solo necesita el correo
#categoria() #metodo de instancia. devuelve oro/plata/bronce segun el gasto total del cliente
#categoria_de(gasto)        # recibe un importe y devuelve oro/plata/bronce, sin necesitar un cliente. metodo estatico
#cambiar_igic(nuevo)        # modifica el IGIC de TODOS los clientes. metodo de clase

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
    
    @classmethod
    def desde_linea(cls, linea):
        nombre, correo = linea.strip().split(";")
        cliente = cls(nombre, correo)
        return cliente
    
    @classmethod
    def cambiar_igic(cls, nuevo):
        cls.IGIC = nuevo

    def registrar_pedido(self, Pedido):
        self.pedidos.append(Pedido)

    def gasto_total(self):
        return sum(p.importe for p in self.pedidos)
    
    def categoria(self):
        return Cliente.categoria_de(self.gasto_total())   
    
    @staticmethod
    def categoría_de(gasto):
        if gasto >= 1000:
            return "oro"
        elif gasto >= 500:
            return "plata"
        else:
            return "bronce"
    
    @staticmethod
    def es_correo_valido(correo):
        return correo.count("@") == 1 and "." in correo.split("@")[1]    