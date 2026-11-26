import numpy as np
import pandas as pd

# Una cadena de cafeterías tiene tres locales: CEN (centro), PLA (playa) y UNI (universidad). Cada fila son las ventas de un local, en euros, y cada columna un día, de lunes a jueves.
ventas_dias = [
    [410, 455, 390, 470],
    [320, 360, 300, 385],
    [520, 540, 505, 560],
]

# Crea el array ventas a partir de ventas_dias. Muestra su forma y el tipo de sus elementos con el rótulo 1.1.
ventas = np.array(ventas_dias)
#print(f"1.1 Forma: {ventas.shape} | tipo: {ventas.dtype}")
# Muestra, como un único valor, las ventas de PLA el jueves.
ventas_jueves = ventas[1,3] 
#print(f"1.2 PLA el jueves: {ventas_jueves}")
# Extrae en un solo corte las ventas de PLA y UNI de lunes a miércoles, ambos incluidos. Muestra el bloque conservando filas y columnas.
ventas_semanal = ventas[1:3,0:3]
#print("1.3 PLA y UNI, Lunes a miercoles: ")
#print(ventas_semanal)

mesas = [12, 10, 16]
locales = ["CEN", "PLA", "UNI"]
dias = ["lunes", "martes", "miércoles", "jueves"]

# Calcula las ventas totales de cada local en los cuatro días y muéstralas identificando cada local.
ventas_total = ventas.sum(axis=1)
ventas_total = ventas_total.reshape(-1,1)
#print("2.1 Total por local: ")
#for n ,v in zip(locales,ventas_total):
    #print(n,v)

# Calcula las ventas medias de los tres locales en cada día y muéstralas identificando cada día.
#media_ventas = ventas.mean(axis=0).round(2)
#print("2.2 Media por dia: ")
#for n ,v in zip(dias,media_ventas):
    #print(n,v)

# Crea el array mesas_arr con las mesas. Mediante broadcasting, divide cada fila de ventas por las mesas de su local y muestra la matriz de euros por mesa redondeada a 2 decimales.
mesas_arr = np.array(mesas)
euros_mesa = ventas / mesas_arr.reshape(-1, 1)
#print("2.3 Euros por mesa:")
#print(euros_mesa.round(2))

# Crea y muestra una máscara que marque los valores de euros por mesa estrictamente inferiores a 32. Muestra también cuántas celdas la cumplen.
#print("2.4 Máscara (< 32 €/mesa): ")
#print(euros_mesa < 32)
#print(f"Celdas que cumplen: {(euros_mesa < 32).sum()}")


codigos = ["CEN", "PLA", "UNI", "AER", "MUE", "PAR"]
estados = ["abierto", "reforma", "abierto", "cerrado", "reforma", "abierto"]

# Construye la Series estado con los estados indexados por código de local y muéstrala.
estados_local = pd.Series(estados, index=codigos)
#print(estados_local)
# Muestra el estado de MUE mediante su etiqueta y el estado del tercer local mediante su posición.
#print(f"3.2 MUE: {estados_local.loc["MUE"]} | tercer local: {estados_local.iloc[2]}")
# Calcula y muestra cuántos locales hay en cada estado.
#print("3.3 Locales por estado:")
#print(estados_local.value_counts())

inventario = {
    "local": ["CEN", "PLA", "UNI", "AER", "MUE", "PAR"],
    "zona": ["centro", "costa", "centro", "costa", "costa", "centro"],
    "mesas": [12, 10, 16, 14, 10, 9],
    "ventas": [455, 379, 540, 610, 401, 330],
}

# Crea el DataFrame df a partir del diccionario y muestra sus dos primeras filas.
df = pd.DataFrame(inventario)
#print("4.1 Dos primeras filas:")
#print(df.head(2))
# Añade la columna por_mesa con las ventas de cada local divididas por sus mesas. No redondees: se necesita la precisión para ordenar.
#print("4.2 Columna por_mesa añadida: ")
df["por_mesa"] = df.ventas / df.mesas
#print(df)
# Selecciona los locales de la zona costa con ventas de al menos 380 euros. Muestra solo local, ventas y por_mesa, ordenados de mayor a menor por_mesa.
#print("4.3 Costa con ventas >= 380:")
#print(df.loc[(df.ventas >= 380) & (df.zona == "costa"),["local","ventas","por_mesa"]].sort_values("por_mesa",ascending=False))

# Carga ventas.csv con pandas convirtiendo fecha a tipo fecha. Muestra las dimensiones de la tabla y el tipo de la columna fecha.
df = pd.read_csv("ventas.csv", parse_dates=["fecha"])
print(f"5.1 Dimensiones: {df.shape} | tipo de fecha: {df.fecha.dtype}")

# Selecciona la ventana del 1 al 20 de febrero de 2026, ambos incluidos. Quédate solo con los registros de CEN o PLA con ventas de al menos 400. Muestra las filas seleccionadas.
print("5.2 Selección:")
df_febrero = df[df["fecha"].between("2026-02-01", "2026-02-20") & df["local"].isin(["CEN", "PLA"]) & (df["ventas"] >= 400)]
print(df_febrero)

# Trabaja sobre una copia de la selección. Añade la columna por_mesa (ventas entre mesas) y muestra las dos ventas de mayor por_mesa, de mayor a menor, con su fecha, local y por_mesa.
df_copy = df.copy()
df_copy["por_mesa"]= df_copy["ventas"] / df_copy["mesas"]
print("5.3 Las dos de mayor ventas por mesa:")
print(df_copy.nlargest(2, "por_mesa")[["fecha", "local", "por_mesa"]])
