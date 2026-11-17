# p01.py
meses = ["ene", "feb", "mar", "abr", "may", "jun"]
#print(meses[0], meses[-1])        # primero y ultimo
#print(meses[1:4])                 # posiciones 1, 2 y 3 (la 4 no entra)
#print(meses[:2], meses[4:])       # desde el principio / hasta el final
#print(meses[::2])                 # de dos en dos
#print(len(meses))                 # cuantos elementos hay

forma = (4, 24)                   # tupla: valores fijos entre parentesis (4 filas, 24 columnas)
filas, columnas = forma           # desempaquetar: una variable por elemento
#print(filas, columnas)
uno = (5,)                        # tupla de UN elemento: la coma es obligatoria
#print(type(uno), type((5)))       # (5) sin coma es solo el numero 5

planta = {"nombre": "Abona I", "kwp": 1800}     # diccionario: clave -> valor
#print(planta["kwp"], list(planta.keys()))
#for clave, valor in planta.items():             # recorrer claves y valores
    #print(clave, "->", valor)

nombre, kwh, cuota = "Abona I", 7392.4567, 0.2731
print(f"{nombre}: {kwh} kWh")                 # las llaves insertan el valor
print(f"{kwh:.1f} kWh")                       # .1f  -> un decimal
print(f"{kwh:,.0f} kWh")                      # ,    -> separador de miles
print(f"{cuota:.1%}")                         # %    -> porcentaje
print(f"[{nombre:<12}] [{kwh:>10.2f}]")       # <12 alinea a la izquierda en 12 huecos; >10 a la derecha

#try:
#    numero = int("12,5")                      # int no entiende la coma: lanza ValueError
#except ValueError as e:                       # 'e' es el objeto con el error
    #print("No se pudo convertir:", e)
    #print(type(e).__name__)                   # el nombre de la clase del error

#meses = ["ene", "feb", "mar"]
#try:
    #print(meses[10])                          # no hay posicion 10
#except IndexError as e:
    #print(type(e).__name__, "->", e)

from pathlib import Path

ruta = Path("datos/alisios/limpio") / "instalaciones.csv"      # / une trozos de ruta
#print(ruta, "|", ruta.name, "|", ruta.suffix, "|", ruta.exists())

with open(ruta, encoding="utf-8") as f:       # f es el fichero abierto; se cierra al salir del bloque
    primera = f.readline()                    # lee una linea
    segunda = f.readline()
#print(primera.strip())                        # strip() quita el salto de linea final
#print(segunda.strip())

def a_mwh(kwh, decimales=1):                  # 'decimales' tiene valor por defecto
    """Convierte kWh a MWh (esto es un docstring: la documentacion de la funcion)."""
    return round(kwh / 1000, decimales)

#print(a_mwh(7392.4567), a_mwh(7392.4567, 3), a_mwh(kwh=500, decimales=2))

doble = lambda x: x * 2                       # lambda: una funcion pequena sin nombre propio
#print(doble(21))

cuadrados = [n * n for n in range(5)]         # lista por comprension
#print(cuadrados)

print("=======================================")
planta = {"nombre": "Planta Arico Sur", "kwp": 1500, "kwh_dia": 6140.27}
print(f"{planta["nombre"]} | {planta["kwp"]:,.0f} kWp | {planta["kwh_dia"]/1000:.1f} MWh | {planta["kwh_dia"]/planta['kwp']:.2f} kWh/kWp")
try:
    planta["municipio"]
except KeyError as e:
    print(type(e).__name__, "->", e)