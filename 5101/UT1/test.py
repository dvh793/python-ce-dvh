import numpy as np,time

a = np.array([3.5, 2.1, 0.0, 4.8])      # desde una lista
b = np.arange(0, 24)                     # 0, 1, ..., 23
c = np.zeros((3, 4))                     # matriz 3x4 de ceros
d = np.linspace(0, 1, 5)                 # 5 valores entre 0 y 1

print(a.dtype, a.shape, a.ndim)
print(b.reshape(2, 12).shape)
print(d)
print("---------------------------------")

kwh = np.random.default_rng(1).random(1_000_000) * 100

t = time.perf_counter()
total = 0
for v in kwh:            # bucle Python
    total += v
t_bucle = time.perf_counter() - t

t = time.perf_counter()
total_np = kwh.sum()     # vectorizado
t_np = time.perf_counter() - t

print(f"bucle: {t_bucle*1000:.0f} ms  numpy: {t_np*1000:.1f} ms  x{t_bucle/t_np:.0f} mas rapido")