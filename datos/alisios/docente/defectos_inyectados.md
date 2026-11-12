# Defectos inyectados en alisios/sucio (verdad conocida para el docente)

Semilla: 5101. Generado con generar_alisios.py.

| Tabla | Tipo de defecto | Detalle |
|---|---|---|
| clientes | duplicados | 18 filas exactas + 18 con nombre/correo en mayúsculas (54 filas afectadas) |
| clientes | espacios | 28 nombres con espacios al principio/final |
| clientes | mayúsculas | 21 municipios en minúsculas |
| clientes | variantes de nombre | 18 municipios con abreviaturas (La Laguna, S/C de Tenerife) |
| clientes | nulos | 25 correos vacíos |
| clientes | NIF inválido | 14 letras de NIF incorrectas (X) |
| clientes | formato de fecha | 107 fechas de alta en dd/mm/aaaa (el resto ISO) |
| clientes | unidades | 18 potencias en W en lugar de kW (valores atípicos) |
| clientes | formato teléfono | 36 teléfonos con espacios |
| clientes | tipo | código postal guardado como entero (se pierde el carácter de texto) |
| pedidos | importe como texto | 1300 totales con formato "1.234,56 €" |
| pedidos | signo | 156 bases imponibles negativas |
| pedidos | categoría inconsistente | 104 estados "PAGADO " (mayúsculas y espacio) |
| pedidos | integridad | 52 pedidos con cliente_id inexistente (9999) |
| pedidos | duplicados | 40 pedidos repetidos |
| pedidos | atípicos | 105 totales multiplicados por 100 |
| incidencias | formato de fecha | 156 aperturas en dd/mm/aaaa HH:MM |
| incidencias | centinela | 39 cierres con la fecha centinela 31/12/9999 |
| incidencias | categoría inconsistente | 23 prioridades capitalizadas |
| incidencias | espacios | 16 tipos "inversor " con espacio final |
| produccion_2025-06 | nulos | 115 lecturas de energía vacías |
| produccion_2025-06 | atípicos | 29 lecturas en Wh en lugar de kWh |
| produccion_2025-06 | centinela | 58 temperaturas -99 (sensor sin dato) |
| produccion_2025-06 | duplicados | 60 lecturas repetidas |
| clientes | fichero | CSV con separador ";", decimal "," y codificación latin-1 |
| clientes_y_pedidos.xlsx | fichero | libro con hoja Portada, cabeceras en las 3 primeras filas (datos desde la fila 5) y hoja Notas |
| pedidos | fichero | CSV estándar (UTF-8, coma) |
| incidencias | fichero | JSON de registros (orient=records) |
| produccion_2025-06 | fichero | TSV (tabulador), fechas dd/mm/aaaa HH:MM |

## Paradas reales de producción (coinciden con incidencias con parada=True en limpio/incidencias.csv)

79 paradas entre 2024 y 2025; durante ellas la energía horaria es 0.
