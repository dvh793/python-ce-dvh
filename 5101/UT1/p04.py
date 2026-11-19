# p04.py
import numpy as np

#              lun  mar  mie  jue
m = np.array([[7.4, 7.1, 2.0, 7.6],     # Abona I
              [9.8, 9.5, 2.9, 9.9],     # Abona II
              [3.9, 3.8, 1.1, 4.0]])    # Guimar
#print(m.shape)                       # (filas, columnas) = (plantas, dias)
#print(m.sum().round(1))              # sin axis: todo -> un numero
#print(m.sum(axis=1).round(1))        # axis=1: un total por planta
#print(m.sum(axis=0).round(1))        # axis=0: un total por dia
#print(m.mean(axis=1).round(2))       # media diaria de cada planta
#print(m.argmax(axis=1))              # posicion del mejor dia de cada planta
#print(m.argmin(axis=0))              # que planta produjo menos cada dia

mw = np.array([1.8, 2.4, 0.95])

prod_dia = m.sum(axis=0)
print(prod_dia.argmax(), prod_dia.max())

miercoles = m[:,2]
print(miercoles)
resto = m[:,[0,1,3]].mean(axis=1)
porcentaje = ((miercoles-resto)/ resto * 100).round(1)
print(porcentaje)

m_mw = m / mw.reshape(-1,1)
print(m_mw)
print(m_mw.round(2)[:,3])
print(m_mw[:,3].argmax())