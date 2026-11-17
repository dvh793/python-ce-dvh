# p02.py
import numpy as np  # np es el alias que usa todo el mundo

kwh = np.array([0.0, 12.5, 48.0, 95.3, 120.0, 88.4, 30.2, 0.0])   # 8 horas de una planta
#print(kwh)
#print(type(kwh))
#print(kwh.dtype)                     # tipo de los elementos
#print(kwh.shape)                     # forma: cuantos elementos en cada dimension
#print(kwh.ndim, kwh.size)            # numero de dimensiones y total de elementos


#print(np.arange(8))                  # enteros 0..7, como range (el 8 no entra)
#print(np.arange(0, 1, 0.25))         # inicio, fin (excluido), paso
#print(np.linspace(0, 1, 5))          # 5 valores equiespaciados; el final SI entra
#print(np.zeros(3))                   # tres ceros (float)
#print(np.ones((2, 3)))               # la forma se pasa como tupla: 2 filas x 3 columnas


kwh = np.array([0.0, 12.5, 48.0, 95.3, 120.0, 88.4, 30.2, 0.0])
#print(kwh[0], kwh[-1])               # primero y ultimo
#print(kwh[2:5])                      # posiciones 2, 3 y 4 (la 5 no entra)
#print(kwh[::2])                      # de dos en dos

dia = np.zeros(24)                   # un dia entero, 24 horas a cero
dia[8:16] = kwh                      # ASIGNAR a un corte: los 8 valores van a las horas 8..15
#print(dia[6:18])
dia[20:] = -1                        # un solo valor rellena todo el corte
#print(dia[18:])


kwh = np.array([0.0, 12.5, 48.0, 95.3, 120.0, 88.4, 30.2, 0.0])
m = kwh.reshape(2, 4)                # los mismos 8 valores, vistos como 2 filas x 4 columnas
#print(m)
#print(m.shape, m.ndim, m.size)
#print(m[1, 0])                       # fila 1, columna 0
#print(m[0])                          # la fila 0 entera
#print(m[:, 0])                       # todas las filas, columna 0
#print(m[:, 1:3])                     # todas las filas, columnas 1 y 2
#print(m.T.shape)                     # traspuesta: filas <-> columnas


vec = np.arange(0, 60, 10)           # [ 0 10 20 30 40 50]
col = vec.reshape(6, 1)              # matriz columna: 6 filas x 1 columna
fila = vec.reshape(1, 6)             # matriz fila: 1 fila x 6 columnas
#print(vec.shape, col.shape, fila.shape)
#print(vec[4], col[4, 0], fila[0, 4]) # el mismo valor, indexado de tres maneras
#print(col[4])                        # una fila de la columna: es un array de un elemento
#print(vec.reshape(-1, 1).shape)      # -1: "calcula tu cuantas filas hacen falta"
#print(col.ravel().shape)             # ravel: vuelve a una dimension


enteros = np.array([1, 2, 3])
#print(enteros.dtype, (enteros / 2).dtype)      # la division produce float64

enteros[0] = 2.7                               # el array es de enteros: 2.7 se trunca SIN AVISO
#print(enteros)

mezcla = np.array([1, 2.5, "3"])               # un texto convierte todo a texto
#print(mezcla, mezcla.dtype)

#print(np.array([1, 2, 3], dtype=float))        # el tipo se puede forzar al crear
#print(np.array(["38001", "35002"]).dtype)      # texto de hasta 5 caracteres

irr = np.linspace(0,1000,13)
print(irr.round(1))
print(irr.mean(),irr[-1],irr.shape)
col = irr.reshape(13, 1)
print(col.shape, col[6, 0])