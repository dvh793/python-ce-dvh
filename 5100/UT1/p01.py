nombre, gasto, n = "Ana Pérez", 214.536, 3

#print(f"{nombre}: {gasto} €")            # sin formato: todos los decimales
#print(f"{nombre}: {gasto:.2f} €")        # :.2f → dos decimales
#print(f"[{nombre:<12}] [{n:>3}] [{gasto:>10.2f}]")   # <, > alinean en un ancho
#print(f"{nombre!r} tiene {n} pedidos")   # !r → la representación "de programador" (con comillas)

def alta(nombre, correo, pedidos=None):      # pedidos es opcional
    if pedidos is None:                      # None como "no me han pasado nada"
        pedidos = []
    return {"nombre": nombre, "correo": correo, "pedidos": pedidos}

#print(alta("Ana", "ana@correo.es"))
#print(alta("Luis", "luis@correo.es", [120.0]))
#print(alta(correo="hotel@teidemar.es", nombre="Hotel Teide Mar"))   # con nombre: el orden da igual

#for texto in ("120", "80,5", "abc"):
    #try:
        #importe = float(texto)
        #print(texto, "→", importe)
    #except ValueError as e:                  # e es el objeto del error
        #print(texto, "→ no es un número:", e)
#print("el programa sigue")

linea = "Luis Yeray;luis@correo.es;120;80.5"
nombre, correo, *importes = linea.split(";")   # * recoge "todo lo que sobra" en una lista
#print(nombre, "|", correo, "|", importes)

pedidos = [float(x) for x in importes]          # comprensión: una lista a partir de otra
#print(pedidos, sum(pedidos))

total = sum(p * 1.07 for p in pedidos)          # lo mismo sin corchetes: un generador, se consume al vuelo
#print(round(total, 2))

gasto = 640
categoria = "oro" if gasto >= 1000 else "plata"   # if/else en una línea (solo para casos simples)
#print(categoria)

clientes = [("Ana", 214.54), ("Hotel Teide Mar", 1348.2), ("Bodegas", 0.0)]
#print(sorted(clientes, key=lambda c: c[1], reverse=True))   # ordenar por el segundo campo

def gasto_total(pedidos: list[float], igic: float = 0.07) -> float:
    """Suma con IGIC, a dos decimales."""
    return round(sum(pedidos) * (1 + igic), 2)

#print(gasto_total([120.0, 80.5]))
#print(gasto_total(["120", "80.5"]))     # la anotación NO comprueba nada: esto falla más abajo, no aquí

# p01.py (final del fichero)
def saluda():
    return "hola desde p01"

if __name__ == "__main__":        # solo cuando se ejecuta ESTE fichero directamente
    print(__name__)
    print(saluda())


def ficha(registro):
    nombre, correo, *textos = registro.split(";")
    try:
        importes = [float(t) for t in textos]
    except ValueError as e:
        return f"{nombre}: importes no válidos ({e})"
    total = sum(importes) * 1.07
    return f"{nombre} <{correo}>: {len(importes)} pedidos, {total:.2f} €"

print(ficha("Hotel Teide Mar;compras@teidemar.es;950;310"))
print(ficha("X;x@x.es;abc"))
