import numpy as np

clientes = np.array([4, 9, 15, 12, 7])      # de 9:00 a 14:00, una cifra por hora
dia = np.zeros(24)

dia[9:14] = clientes
dia[20:] = -1
print(dia)
print(len(dia))

print("==================")

pasos = np.array([3200, 4100, 1500,     # día 1: mañana, tarde, noche
                  2800, 5200, 900,      # día 2
                  4000, 3900, 2100,     # día 3
                  1200, 2500, 600,      # día 4
                  3600, 4800, 1700])    # día 5

print(pasos.shape)
dias = pasos.reshape(5,3)
print(dias.shape)
print(dias[2])