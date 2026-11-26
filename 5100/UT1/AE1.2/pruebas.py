from cuenta import CuentaBancaria
from rectangulo import Rectangulo

cuenta1 = CuentaBancaria("Pepe", 1000)
print(cuenta1)
cuenta1.ingresar(500)
print(cuenta1)
cuenta1.retirar(200)
print(cuenta1)

cuenta2 = CuentaBancaria.desde_texto("Jose: 1500")
print(cuenta2)

print("IBAN válido:", CuentaBancaria.iban_valido("ES12345678901234567890123"))

print(len(cuenta1))  # Número de movimientos
print(cuenta1)  # Llamada a __str__ para cuenta1
print(repr(cuenta1))  # Llamada a __repr__ para cuenta1

try:
    cuenta1.retirar(2000)  # Intento de retirar más de lo disponible
    cuenta3 = CuentaBancaria("Juan", -100)
    cuenta3.ingresar(-50)
    cuenta3.retirar(2000)
except ValueError as e:
    print("Error:", e)

r1 = Rectangulo(3, 4)
print(r1)
print("Área:", r1.area())
print("Perímetro:", r1.perimetro())
print("Es cuadrado:", r1.es_cuadrado())
print("Diagonal válida para r1:", Rectangulo.desde_diagonal_valida(r1.base, r1.altura, 10))
print("Escalando por 2...")
r1.escalar(2)
print(r1)

r2 = Rectangulo.cuadrado(5)
print(r2)

print(r1)  # Llamada a __str__ para r1
print(repr(r1))  # Llamada a __repr__ para r2)

try:
    r1.escalar(-1)  # Intento de escalar con un factor negativo
    r3= Rectangulo(-1, 0)
    r4= Rectangulo(-1, -9)
    r5= Rectangulo(-1, "b")
except ValueError as e:
    print("Error:", e)
    
cuenta3 = CuentaBancaria("Ana", 500)
cuenta4 = cuenta3
del cuenta3
print("Cuenta3 eliminada, pero cuenta4 sigue existiendo:", cuenta4)
del cuenta4
print("Cuenta4 eliminada, ahora no hay referencias a la cuenta de Ana.")