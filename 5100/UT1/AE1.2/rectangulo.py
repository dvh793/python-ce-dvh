class Rectangulo:
    def __init__(self, base, altura):
        if base <= 0 or altura <= 0:
            raise ValueError("La base y la altura deben ser mayores que cero")
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)
    
    def es_cuadrado(self):
        return self.base == self.altura
    
    def escalar(self, factor):
        if factor <= 0:
            raise ValueError("El factor de escalado debe ser mayor que cero")
        self.base *= factor
        self.altura *= factor
        return self
    
    @classmethod
    def cuadrado(cls, lado):
        if lado <= 0:
            raise ValueError("El lado debe ser mayor que cero")
        return cls(lado, lado) 
    
    @staticmethod
    def desde_diagonal_valida(base,altura,diagonal):
        if base <= 0 or altura <= 0 or diagonal <= 0:
            raise ValueError("Todos los parámetros deben ser mayores que cero")
        if (base**2 + altura**2 == diagonal**2):
            return True
        else:
            return False
        
    def __str__(self):  #__str__ para representar el objeto como cadena de texto
        return "Rectángulo de base {} y altura {}".format(self.base, self.altura)
    
    def __repr__(self): #__repr__ para representar el objeto de manera más detallada
        return "Rectangulo({}, {})".format(self.base, self.altura) 
    

