# Paquete de datos del módulo 5101 · Análisis de datos con Python

Carpeta `AN3/datos/` · CIFP César Manrique · curso de especialización 961NTA.
Criterio (decisión del 14/10/2026): **datos conocidos para aprender la herramienta, datos reales y sintéticos con
defectos controlados para aprender a analizar**. El módulo no depende de ningún otro: todo lo que usa está aquí
o se descarga con un script.

## Contenido

| Carpeta | Qué es | Origen / licencia |
|---|---|---|
| `bd/chinook.db` | Tienda de música (11 tablas, 59 clientes, 412 facturas). SQLite. `Chinook_MySql.sql` para cargarla en MySQL/MariaDB | [lerocha/chinook-database](https://github.com/lerocha/chinook-database) · MIT |
| `bd/northwind.db` | Northwind ampliada: 93 clientes, 77 productos, **16 282 pedidos / 609 283 líneas** con fechas 2012–2023. SQLite (23 MB) | [jpwhite3/northwind-SQLite3](https://github.com/jpwhite3/northwind-SQLite3) · MIT |
| `alisios/limpio/` | Datos sintéticos **correctos** de Alisios Renovables, S.L.: 8 instalaciones FV, 320 clientes, 10 productos, 5 200 pedidos y 13 028 líneas, 779 incidencias, producción **horaria** 2024-2025 (140 352 filas) y diaria. CSV + Parquet + `alisios.db` (SQLite con las 8 tablas) | `generar_alisios.py` (semilla 5101) · uso docente libre |
| `alisios/sucio/` | Los mismos clientes, pedidos, incidencias y un mes de producción **con 29 tipos de defecto inyectados** y en formatos incómodos: CSV `;` latin-1, XLSX con portada y cabeceras desplazadas, JSON de registros, TSV con fechas `dd/mm/aaaa` | ídem |
| `alisios/docente/` | `defectos_inyectados.md`: lista exacta de cada defecto y cuántas filas afecta (verdad conocida para corregir la UT2). `resumen.json` | ídem |
| `reales/` | Datos abiertos reales, descargados y **congelados** por `descargar_datos.py` (ver abajo). Se crea al ejecutar el script | Cabildo de Tenerife (CC BY), ISTAC / Open Data Canarias (CC BY 4.0), Red Eléctrica (REData, uso libre con cita), JRC PVGIS (uso libre con cita), Open-Meteo (CC BY 4.0, uso no comercial) |

## Datos reales: qué descarga `descargar_datos.py`

Ejecutar **una vez** desde esta carpeta, con conexión a internet (`python descargar_datos.py`, o solo algunos bloques:
`python descargar_datos.py iter meteo ree`). Es idempotente y deja `reales/fuentes.json` con URL y fecha de cada fichero.

| Bloque | Ficheros | Para qué |
|---|---|---|
| `iter` | Energía **mensual exportada/importada de 12 plantas FV y parques eólicos** gestionados por el ITER en Tenerife (03/2021 → hoy), un CSV por planta + `energia_mensual_todas_las_plantas.csv` + ubicaciones (CSV/GeoJSON) + diccionario de datos | UT3 (estacionalidad, FV frente a eólica, ranking de plantas), UT4 (producción ~ meteorología), proyecto |
| `meteo` | **Datos meteorológicos diarios por sensor** (media/mín/máx/total) de 4–6 estaciones de AgroCabildo cercanas a las plantas, años 2021–2025, un CSV por estación y año; `estaciones_disponibles.json` lista las 139 | UT2 (formato largo → ancho, BOM, filas `total` vacías, un fichero por año), UT3, UT4 |
| `ree` | **Demanda eléctrica diaria de Canarias** 2023–2025 y **generación mensual por tecnología** (REData, JSON aplanado a CSV) | UT3 (series temporales, estacionalidad semanal/anual), UT4 (demanda ~ temperatura y calendario) |
| `istac` | Indicadores **por municipio y año** (población total/hombres/mujeres, saldo migratorio, mortalidad, sociedades) en JSON de la API del ISTAC y aplanados a CSV; catálogo de 402 indicadores. La carpeta incluye además `municipios_canarias.csv` (código INE, municipio, isla y provincia de los 88 municipios; elaborado por el profesorado, no se descarga) | UT1 (JSON con estructura dimensión/observación: ANE1.1), UT3 (cruce con clientes por municipio) |
| `pvgis` | Radiación horaria + temperatura + viento + producción FV simulada (1 kWp, 20° sur) 2021–2023 en tres emplazamientos (PVGIS v5.3, CSV) | UT4 (modelo producción ~ irradiancia), comparación con la producción real del ITER |
| `meteo_api` | Horario 2021–2025 de temperatura, radiación, viento, nubosidad y lluvia en los mismos tres puntos (Open-Meteo, ERA5, CSV) | UT4, proyecto |
| `odc` | Producción neta de electricidad según fuentes por islas (ISTAC vía Open Data Canarias, CSV/XLSX) | UT1 (lectura de XLSX con varias hojas), UT3 |

Comprobado el 14/10/2026: `iter`, `meteo`, `ree`, `istac` y `odc` responden sin clave. `pvgis` y `meteo_api` no requieren clave
según su documentación, pero no se pudieron probar desde el entorno de preparación: si fallan, el bloque se salta y el
resto continúa.

## Reparto por unidad de trabajo

| UT | Para aprender la herramienta | Para aprender a analizar |
|---|---|---|
| UT0 | `bd/chinook.db` (primer `read_sql` en el primer cuaderno) | — |
| UT1 Carga, exportación, BD | `bd/northwind.db` y `bd/chinook.db` (SQLite y MySQL): `read_sql`, `to_sql`, CRUD con SQLAlchemy | `alisios/sucio/*` para leer CSV con `;`/latin-1, XLSX con cabeceras desplazadas, JSON; `reales/istac/*.data.json` (JSON no tabular); Parquet de `alisios/limpio` |
| UT2 Limpieza | — | `alisios/sucio/*` con `docente/defectos_inyectados.md` como solución; `reales/meteo/*.csv` (formato largo, BOM, nulos) |
| UT3 EDA | Northwind (groupby, pivot, merge con resultados comprobables) | `reales/iter`, `reales/ree`, `reales/istac`, `alisios/limpio/produccion_diaria` |
| UT4 Modelado | — | `alisios/limpio/produccion_diaria` (energía ~ irradiación + temperatura; correlación ≈ 0,95 por planta), `reales/iter` + `reales/meteo` o `reales/pvgis`, `reales/ree` (demanda ~ temperatura) |
| Proyecto | — | cualquier combinación de `reales/*`; la aplicación de 5100 presenta los resultados |

## Notas sobre los datos sintéticos

- Producción horaria: modelo de cielo claro (Meinel) con ganancia por inclinación, nubosidad diaria con persistencia
  (más en invierno y en el norte), pérdida por temperatura de célula, degradación anual del 0,4 % y **79 paradas** que
  coinciden con las incidencias marcadas `parada=True`. Rendimiento ≈ 1 180 kWh/kWp·año; verano ≈ 2 × invierno.
  Se ignora el cambio de hora a propósito (simplificación documentada).
- Claves foráneas: `pedidos.cliente_id → clientes`, `lineas_pedido.pedido_id → pedidos`, `lineas_pedido.producto_id → productos`,
  `incidencias.instalacion_id → instalaciones`, `produccion_*.instalacion_id → instalaciones`. IGIC 7 %.
- Para regenerar (cambia la semilla en el script si se quiere otra versión): `python generar_alisios.py`.
  Dependencias: `pandas numpy openpyxl pyarrow`.

## Cómo cargar Northwind/Chinook en MySQL (UT1, opcional)

`Chinook_MySql.sql` se ejecuta tal cual en MySQL/MariaDB. Northwind: exportar desde SQLite con pandas (`read_sql` → `to_sql`
con SQLAlchemy), que es precisamente el ejercicio de la UT1.
