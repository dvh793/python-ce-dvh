# p03.py
import numpy as np

kwh = np.array([0.0, 12.5, 48.0, 95.3, 120.0, 88.4, 30.2, 0.0])
#print(kwh * 1000)                    # cada elemento por 1000 (a Wh)
#print(kwh + 10)                      # cada elemento mas 10
precio = np.array([0.08, 0.08, 0.10, 0.12, 0.12, 0.12, 0.10, 0.08])   # EUR/kWh de cada hora
#print(kwh * precio)                  # elemento a elemento: ingresos de cada hora
#print((kwh * precio).sum().round(2)) # y su suma


horas = np.arange(8,16)
print((kwh / kwh.sum() * 100).round(1))
media = kwh > kwh.mean()
print(kwh.mean())
print(media.sum())
print(horas[kwh.argmax()])
print(kwh[media].sum())
print(horas[media])
