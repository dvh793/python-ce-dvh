import pandas as pd

lin = pd.read_csv("datos/alisios/limpio/lineas_pedido.csv")
print(lin.columns.tolist())                                # mira primero

lin["bruto"] = lin.cantidad * lin.precio_unitario          # columna calculada
lin["con_descuento"] = lin.importe < lin.bruto
top = lin.sort_values("importe", ascending=False).head(3)
print(top[["pedido_id", "producto_id", "cantidad", "importe"]])
print(lin.importe.sum().round(2), lin.con_descuento.mean().round(3))
print(lin.info())