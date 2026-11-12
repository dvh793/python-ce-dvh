#!/usr/bin/env python3
"""Generador del paquete de datos sintéticos de Alisios Renovables, S.L.
Módulo 5101 Análisis de datos con Python · CIFP César Manrique.

Produce, de forma reproducible (semilla fija):
  alisios/limpio/   datos correctos (CSV + Parquet) y alisios.db (SQLite)
  alisios/sucio/    los mismos datos con defectos inyectados (CSV, XLSX, JSON) para la UT2
  alisios/docente/  defectos_inyectados.md (verdad conocida) y resumen

Dependencias: numpy, pandas, openpyxl, pyarrow (opcional: sin pyarrow no se escribe Parquet).
Uso:  python generar_alisios.py [--salida alisios] [--anio-inicio 2024] [--anio-fin 2025]
"""
import argparse, json, math, sqlite3, textwrap
from pathlib import Path
import numpy as np, pandas as pd

SEED = 5101
rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ catálogo
INSTALACIONES = [
    # id, nombre, municipio, lat, lon, kWp, tipo, fecha_alta
    (1, 'Planta Abona I', 'Granadilla de Abona', 28.078, -16.520, 1800, 'fotovoltaica', '2019-03-12'),
    (2, 'Planta Abona II', 'Granadilla de Abona', 28.082, -16.515, 2400, 'fotovoltaica', '2020-06-01'),
    (3, 'Cubierta Polígono Güímar', 'Güímar', 28.306, -16.389, 950, 'fotovoltaica', '2021-02-15'),
    (4, 'Planta Arico Sur', 'Arico', 28.095, -16.470, 1500, 'fotovoltaica', '2021-09-20'),
    (5, 'Cubierta Mercatenerife', 'Santa Cruz de Tenerife', 28.456, -16.278, 600, 'fotovoltaica', '2022-04-04'),
    (6, 'Planta La Guancha', 'La Guancha', 28.371, -16.653, 700, 'fotovoltaica', '2022-11-11'),
    (7, 'Planta Fasnia', 'Fasnia', 28.235, -16.432, 1200, 'fotovoltaica', '2023-05-30'),
    (8, 'Cubierta Las Chafiras', 'San Miguel de Abona', 28.037, -16.616, 450, 'fotovoltaica', '2023-10-02'),
]
MUNICIPIOS_TF = ['Santa Cruz de Tenerife', 'San Cristóbal de La Laguna', 'Arona', 'Adeje', 'Granadilla de Abona',
                 'La Orotava', 'Los Realejos', 'Puerto de la Cruz', 'Candelaria', 'Guía de Isora', 'Icod de los Vinos',
                 'Tacoronte', 'Güímar', 'El Rosario', 'Santiago del Teide', 'Arico', 'Fasnia', 'La Guancha',
                 'San Miguel de Abona', 'Tegueste']
MUNICIPIOS_GC = ['Las Palmas de Gran Canaria', 'Telde', 'Santa Lucía de Tirajana', 'San Bartolomé de Tirajana', 'Arucas']
CP = {'Santa Cruz de Tenerife': '38001', 'San Cristóbal de La Laguna': '38201', 'Arona': '38640', 'Adeje': '38670',
      'Granadilla de Abona': '38600', 'La Orotava': '38300', 'Los Realejos': '38410', 'Puerto de la Cruz': '38400',
      'Candelaria': '38530', 'Guía de Isora': '38680', 'Icod de los Vinos': '38430', 'Tacoronte': '38350', 'Güímar': '38500',
      'El Rosario': '38290', 'Santiago del Teide': '38690', 'Arico': '38580', 'Fasnia': '38570', 'La Guancha': '38440',
      'San Miguel de Abona': '38620', 'Tegueste': '38280', 'Las Palmas de Gran Canaria': '35001', 'Telde': '35200',
      'Santa Lucía de Tirajana': '35110', 'San Bartolomé de Tirajana': '35100', 'Arucas': '35400'}
NOMBRES = ['Yeray', 'Marta', 'Aday', 'Nira', 'Airam', 'Idaira', 'Jonay', 'Guacimara', 'Carlos', 'Lucía', 'Pedro', 'Ana',
           'Sergio', 'Elena', 'Juan', 'María', 'Daniel', 'Laura', 'Javier', 'Carmen', 'Francisco', 'Paula', 'Antonio',
           'Sara', 'José', 'Raquel', 'Miguel', 'Cristina', 'David', 'Patricia']
APELLIDOS = ['Hernández', 'González', 'Rodríguez', 'Pérez', 'Martín', 'García', 'Díaz', 'Dorta', 'Delgado', 'Afonso',
             'Trujillo', 'Melián', 'Cabrera', 'Siverio', 'Méndez', 'Acosta', 'Rivero', 'Expósito', 'Padrón', 'Bethencourt']
EMPRESAS = ['Bodegas Teide Alto S.L.', 'Supermercados Guanche S.A.', 'Hotel Mar y Sol S.L.', 'Aparcamientos Anaga S.L.',
            'Plátanos del Valle S.A.T.', 'Comunidad de Propietarios Edificio Alisios', 'Talleres Hermanos Dorta S.L.',
            'Clínica Dental Tabaiba', 'Panadería La Milagrosa', 'Transportes Chasna S.L.', 'Colegio San Andrés',
            'Residencia Los Dragos', 'Ferretería El Volcán', 'Lavandería Industrial Sur S.L.', 'Finca La Caldera']
TIPOS_CLIENTE = ['residencial', 'empresa', 'comunidad']
TIPO_INC = ['inversor', 'comunicaciones', 'suciedad paneles', 'vandalismo', 'red eléctrica', 'cableado', 'monitorización']
PRIORIDAD = ['baja', 'media', 'alta', 'crítica']
TECNICOS = ['Yeray Dorta', 'Nira Afonso', 'Aday Melián', 'Idaira Rivero']
IGIC = 0.07


def letra_nif(num):
    return 'TRWAGMYFPDXBNJZSQVHLCKE'[num % 23]


# ------------------------------------------------------------------ producción
def irradiancia_horaria(lat, fechas_hora):
    """Irradiancia global sobre plano horizontal (W/m2) con modelo de cielo claro simplificado.
    fechas_hora: DatetimeIndex en hora local (UTC+0 en Canarias en invierno; se ignora el horario de verano
    a propósito: lo documenta el README como simplificación)."""
    doy = fechas_hora.dayofyear.values
    hora = fechas_hora.hour.values + 0.5
    decl = np.radians(23.44) * np.sin(2 * np.pi * (284 + doy) / 365)
    h = np.radians(15 * (hora - 12.6))           # ángulo horario; mediodía solar ~12:36 en Tenerife
    latr = np.radians(lat)
    sen_elev = np.sin(latr) * np.sin(decl) + np.cos(latr) * np.cos(decl) * np.cos(h)
    sen_elev = np.clip(sen_elev, 0, None)
    am = 1 / np.clip(sen_elev, 0.05, None)       # masa de aire aproximada
    return 1050 * sen_elev * (0.7 ** (am ** 0.678))  # W/m2 (modelo Meinel)


def generar_produccion(anio_ini, anio_fin):
    idx = pd.date_range(f'{anio_ini}-01-01', f'{anio_fin}-12-31 23:00', freq='h')
    dias = pd.date_range(f'{anio_ini}-01-01', f'{anio_fin}-12-31', freq='D')
    # nubosidad diaria con persistencia (AR1) y estacionalidad: más nubes en invierno y en el norte
    n = len(dias); ar = np.zeros(n); e = rng.normal(0, 0.35, n)
    for i in range(1, n): ar[i] = 0.6 * ar[i - 1] + e[i]
    estac = 0.08 * np.cos(2 * np.pi * (dias.dayofyear.values - 15) / 365)   # +0.15 en enero, -0.15 en julio
    nubes_dia = pd.Series(np.clip(0.12 + estac + 0.15 * ar, 0, 0.85), index=dias)   # fracción de pérdida
    temp_dia = pd.Series(21 + 4.5 * np.sin(2 * np.pi * (dias.dayofyear.values - 110) / 365) + rng.normal(0, 1.5, n), index=dias)
    filas = []
    incidencias_paradas = []  # (inst, inicio, fin)
    for (iid, nombre, muni, lat, lon, kwp, tipo, alta) in INSTALACIONES:
        norte = 1.25 if lat > 28.3 else 1.0           # el norte es más nuboso
        g = irradiancia_horaria(lat, idx) * (1.15 + 0.25 * np.cos(2 * np.pi * (idx.dayofyear.values - 15) / 365))  # ganancia por inclinación (mayor en invierno)
        nub = np.clip(nubes_dia.reindex(idx.normalize()).values * norte + rng.normal(0, 0.05, len(idx)), 0, 0.95)
        t_amb = temp_dia.reindex(idx.normalize()).values + 4 * np.sin(2 * np.pi * (idx.hour.values - 9) / 24)
        t_cel = t_amb + 0.03 * g * (1 - nub)
        rendimiento = 0.86 * (1 - 0.004 * np.clip(t_cel - 25, 0, None))
        kwh = kwp * (g * (1 - nub) / 1000) * rendimiento
        kwh *= np.clip(1 - 0.004 * (idx.year.values - int(alta[:4])), 0.9, 1)   # degradación anual 0,4 %
        # paradas por incidencia: 3-6 por año y planta, de 2 a 72 h
        activa = np.ones(len(idx))
        for anio in range(anio_ini, anio_fin + 1):
            for _ in range(rng.integers(3, 7)):
                ini = pd.Timestamp(f'{anio}-01-01') + pd.Timedelta(hours=int(rng.integers(0, 8760)))
                dur = int(rng.integers(2, 73)); fin = ini + pd.Timedelta(hours=dur)
                activa[(idx >= ini) & (idx < fin)] = 0
                incidencias_paradas.append((iid, ini, fin))
        kwh = kwh * activa + rng.normal(0, 0.5, len(idx)) * (g > 0)
        kwh = np.where(pd.DatetimeIndex(idx) < pd.Timestamp(alta), np.nan, np.clip(kwh, 0, None))
        filas.append(pd.DataFrame({'instalacion_id': iid, 'fecha_hora': idx, 'irradiancia_wm2': np.round(g * (1 - nub), 1),
                                   'temperatura_c': np.round(t_amb, 1), 'energia_kwh': np.round(kwh, 2)}))
    prod = pd.concat(filas, ignore_index=True).dropna(subset=['energia_kwh']).reset_index(drop=True)
    return prod, incidencias_paradas


# ------------------------------------------------------------------ clientes, pedidos, incidencias
def generar_clientes(n=320):
    rows = []
    for i in range(1, n + 1):
        tipo = rng.choice(TIPOS_CLIENTE, p=[0.6, 0.3, 0.1])
        if tipo == 'residencial':
            nombre = f'{rng.choice(NOMBRES)} {rng.choice(APELLIDOS)} {rng.choice(APELLIDOS)}'
            num = int(rng.integers(10_000_000, 79_999_999)); nif = f'{num}{letra_nif(num)}'
        elif tipo == 'empresa':
            nombre = rng.choice(EMPRESAS) if rng.random() < 0.3 else f'{rng.choice(APELLIDOS)} y {rng.choice(APELLIDOS)} S.L.'
            nif = f'B{int(rng.integers(10_000_000, 99_999_999))}'
        else:
            nombre = f'Comunidad de Propietarios {rng.choice(["Calle", "Avenida", "Edificio"])} {rng.choice(APELLIDOS)} {int(rng.integers(1, 90))}'
            nif = f'H{int(rng.integers(10_000_000, 99_999_999))}'
        muni = rng.choice(MUNICIPIOS_TF) if rng.random() < 0.85 else rng.choice(MUNICIPIOS_GC)
        prov = 'Santa Cruz de Tenerife' if muni in MUNICIPIOS_TF else 'Las Palmas'
        alta = pd.Timestamp('2019-01-01') + pd.Timedelta(days=int(rng.integers(0, 2400)))
        pot = float(rng.choice([3.45, 4.6, 5.75, 6.9, 9.2, 15, 20, 30, 50], p=[.15, .2, .15, .15, .1, .1, .07, .05, .03]))
        correo = (nombre.split()[0] + '.' + nombre.split()[1]).lower().replace('ñ', 'n').replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') + f'{i}@' + rng.choice(['gmail.com', 'hotmail.com', 'outlook.es', 'alisios.example'])
        rows.append(dict(cliente_id=i, nombre=nombre, nif=nif, tipo=tipo, correo=correo, telefono=f'{rng.choice([6, 9, 8])}{int(rng.integers(10_000_000, 99_999_999))}',
                         municipio=muni, provincia=prov, codigo_postal=CP[muni], fecha_alta=alta.date(), potencia_contratada_kw=pot,
                         activo=bool(rng.random() < 0.93)))
    return pd.DataFrame(rows)


def generar_pedidos(clientes, anio_ini, anio_fin, n=5200):
    productos = pd.DataFrame([
        (1, 'Panel 450 Wp monocristalino', 'material', 165.0), (2, 'Inversor híbrido 5 kW', 'material', 1250.0),
        (3, 'Batería 5 kWh', 'material', 2100.0), (4, 'Estructura coplanar (ud)', 'material', 38.0),
        (5, 'Instalación residencial (h)', 'servicio', 42.0), (6, 'Mantenimiento anual', 'servicio', 180.0),
        (7, 'Limpieza de paneles (kWp)', 'servicio', 9.5), (8, 'Legalización y boletín', 'servicio', 320.0),
        (9, 'Monitorización (año)', 'servicio', 96.0), (10, 'Cargador vehículo 7,4 kW', 'material', 890.0)],
        columns=['producto_id', 'descripcion', 'categoria', 'precio_unitario'])
    ped, lineas = [], []
    pid = 0
    for _ in range(n):
        pid += 1
        c = clientes.sample(1, random_state=int(rng.integers(0, 2**31))).iloc[0]
        fecha = pd.Timestamp(f'{anio_ini}-01-01') + pd.Timedelta(days=int(rng.integers(0, 365 * (anio_fin - anio_ini + 1))))
        fecha = max(fecha, pd.Timestamp(c.fecha_alta))
        estado = rng.choice(['pagado', 'pendiente', 'anulado'], p=[.82, .13, .05])
        nl = int(rng.integers(1, 5)); total = 0
        for prod in productos.sample(nl, random_state=int(rng.integers(0, 2**31))).itertuples():
            cant = int(rng.integers(1, 13)) if prod.categoria == 'material' else int(rng.integers(1, 4))
            if prod.producto_id == 7: cant = int(c.potencia_contratada_kw)
            imp = round(cant * prod.precio_unitario * float(rng.choice([1, 0.95, 0.9], p=[.8, .15, .05])), 2)
            lineas.append(dict(pedido_id=pid, producto_id=prod.producto_id, cantidad=cant, precio_unitario=prod.precio_unitario, importe=imp))
            total += imp
        ped.append(dict(pedido_id=pid, cliente_id=int(c.cliente_id), fecha=fecha.date(), estado=estado,
                        base_imponible=round(total, 2), igic=round(total * IGIC, 2), total=round(total * (1 + IGIC), 2),
                        canal=rng.choice(['web', 'oficina', 'comercial'], p=[.5, .3, .2])))
    return productos, pd.DataFrame(ped), pd.DataFrame(lineas)


def generar_incidencias(paradas, anio_ini, anio_fin, n_extra=700):
    rows = []
    for (iid, ini, fin) in paradas:
        rows.append(dict(instalacion_id=iid, fecha_apertura=ini, fecha_cierre=fin, tipo=rng.choice(TIPO_INC[:2] + TIPO_INC[4:6]),
                         prioridad=rng.choice(PRIORIDAD[1:], p=[.3, .45, .25]), parada=True))
    for _ in range(n_extra):
        iid = int(rng.integers(1, len(INSTALACIONES) + 1))
        ini = pd.Timestamp(f'{anio_ini}-01-01') + pd.Timedelta(hours=int(rng.integers(0, 8760 * (anio_fin - anio_ini + 1))))
        dur = float(rng.lognormal(2.5, 0.9))  # horas
        cierre = ini + pd.Timedelta(hours=dur) if rng.random() < 0.9 else pd.NaT
        rows.append(dict(instalacion_id=iid, fecha_apertura=ini, fecha_cierre=cierre, tipo=rng.choice(TIPO_INC),
                         prioridad=rng.choice(PRIORIDAD, p=[.4, .35, .2, .05]), parada=False))
    inc = pd.DataFrame(rows).sort_values('fecha_apertura').reset_index(drop=True)
    inc.insert(0, 'incidencia_id', range(1, len(inc) + 1))
    inc['tecnico'] = rng.choice(TECNICOS, len(inc))
    inc['descripcion'] = [f'{t.capitalize()}: {rng.choice(["aviso del SCADA", "llamada del cliente", "revisión programada", "alarma de comunicaciones", "inspección visual"])}' for t in inc.tipo]
    inc['fecha_apertura'] = inc.fecha_apertura.dt.floor('min'); inc['fecha_cierre'] = inc.fecha_cierre.dt.floor('min')
    return inc


# ------------------------------------------------------------------ defectos (UT2)
def ensuciar(clientes, pedidos, incidencias, prod, log):
    r = np.random.default_rng(SEED + 1)
    # --- clientes
    c = clientes.copy().astype({'fecha_alta': 'object', 'nombre': 'object', 'correo': 'object', 'municipio': 'object', 'nif': 'object', 'telefono': 'object'})
    dup = c.sample(18, random_state=1); dup2 = dup.copy(); dup2['nombre'] = dup2.nombre.str.upper(); dup2['correo'] = dup2.correo.str.upper()
    c = pd.concat([c, dup, dup2], ignore_index=True); log('clientes', 'duplicados', '18 filas exactas + 18 con nombre/correo en mayúsculas (54 filas afectadas)')
    i = c.sample(frac=0.08, random_state=2).index; c.loc[i, 'nombre'] = '  ' + c.loc[i, 'nombre'] + ' '; log('clientes', 'espacios', f'{len(i)} nombres con espacios al principio/final')
    i = c.sample(frac=0.06, random_state=3).index; c.loc[i, 'municipio'] = c.loc[i, 'municipio'].str.lower(); log('clientes', 'mayúsculas', f'{len(i)} municipios en minúsculas')
    i = c.sample(frac=0.05, random_state=4).index; c.loc[i, 'municipio'] = c.loc[i, 'municipio'].str.replace('San Cristóbal de La Laguna', 'La Laguna').str.replace('Santa Cruz de Tenerife', 'S/C de Tenerife'); log('clientes', 'variantes de nombre', f'{len(i)} municipios con abreviaturas (La Laguna, S/C de Tenerife)')
    i = c.sample(frac=0.07, random_state=5).index; c.loc[i, 'correo'] = None; log('clientes', 'nulos', f'{len(i)} correos vacíos')
    i = c.sample(frac=0.04, random_state=6).index; c.loc[i, 'nif'] = c.loc[i, 'nif'].str[:-1] + 'X'; log('clientes', 'NIF inválido', f'{len(i)} letras de NIF incorrectas (X)')
    i = c.sample(frac=0.3, random_state=7).index; c.loc[i, 'fecha_alta'] = pd.to_datetime(c.loc[i, 'fecha_alta']).dt.strftime('%d/%m/%Y'); log('clientes', 'formato de fecha', f'{len(i)} fechas de alta en dd/mm/aaaa (el resto ISO)')
    i = c.sample(frac=0.05, random_state=8).index; c.loc[i, 'potencia_contratada_kw'] = c.loc[i, 'potencia_contratada_kw'] * 1000; log('clientes', 'unidades', f'{len(i)} potencias en W en lugar de kW (valores atípicos)')
    i = c.sample(frac=0.1, random_state=9).index; c.loc[i, 'telefono'] = c.loc[i, 'telefono'].str.replace(r'(\d{3})(\d{3})(\d{3})', r'\1 \2 \3', regex=True); log('clientes', 'formato teléfono', f'{len(i)} teléfonos con espacios')
    c['codigo_postal'] = c.codigo_postal.astype(int); log('clientes', 'tipo', 'código postal guardado como entero (se pierde el carácter de texto)')
    c = c.sample(frac=1, random_state=10).reset_index(drop=True)
    # --- pedidos
    p = pedidos.copy().astype({'fecha': 'string', 'total': 'object', 'estado': 'object'})
    i = p.sample(frac=0.25, random_state=11).index; p.loc[i, 'total'] = p.loc[i, 'total'].map(lambda v: f'{v:,.2f} €'.replace(',', 'X').replace('.', ',').replace('X', '.')); log('pedidos', 'importe como texto', f'{len(i)} totales con formato "1.234,56 €"')
    i = p.sample(frac=0.03, random_state=12).index; p.loc[i, 'base_imponible'] = -p.loc[i, 'base_imponible']; log('pedidos', 'signo', f'{len(i)} bases imponibles negativas')
    i = p.sample(frac=0.02, random_state=13).index; p.loc[i, 'estado'] = 'PAGADO '; log('pedidos', 'categoría inconsistente', f'{len(i)} estados "PAGADO " (mayúsculas y espacio)')
    i = p.sample(frac=0.01, random_state=14).index; p.loc[i, 'cliente_id'] = 9999; log('pedidos', 'integridad', f'{len(i)} pedidos con cliente_id inexistente (9999)')
    dup = p.sample(40, random_state=15); p = pd.concat([p, dup], ignore_index=True); log('pedidos', 'duplicados', '40 pedidos repetidos')
    i = p.sample(frac=0.02, random_state=16).index; p.loc[i, 'total'] = p.loc[i, 'base_imponible'].astype(float).abs() * 100; log('pedidos', 'atípicos', f'{len(i)} totales multiplicados por 100')
    # --- incidencias
    q = incidencias.copy().astype({'tipo': 'object', 'prioridad': 'object'})
    q['fecha_apertura'] = q.fecha_apertura.dt.strftime('%Y-%m-%d %H:%M').astype(object); q['fecha_cierre'] = q.fecha_cierre.dt.strftime('%Y-%m-%d %H:%M').astype(object)
    i = q.sample(frac=0.2, random_state=17).index; q.loc[i, 'fecha_apertura'] = pd.to_datetime(q.loc[i, 'fecha_apertura']).dt.strftime('%d/%m/%Y %H:%M'); log('incidencias', 'formato de fecha', f'{len(i)} aperturas en dd/mm/aaaa HH:MM')
    i = q.sample(frac=0.05, random_state=18).index; q.loc[i, 'fecha_cierre'] = '31/12/9999'; log('incidencias', 'centinela', f'{len(i)} cierres con la fecha centinela 31/12/9999')
    i = q.sample(frac=0.03, random_state=19).index; q.loc[i, 'prioridad'] = q.loc[i, 'prioridad'].str.capitalize(); log('incidencias', 'categoría inconsistente', f'{len(i)} prioridades capitalizadas')
    i = q.sample(frac=0.02, random_state=20).index; q.loc[i, 'tipo'] = 'inversor '; log('incidencias', 'espacios', f'{len(i)} tipos "inversor " con espacio final')
    q = q.drop(columns=['parada'])
    # --- producción (solo versión sucia reducida: un mes por instalación)
    pr = prod[(prod.fecha_hora >= '2025-06-01') & (prod.fecha_hora < '2025-07-01')].copy().astype({'temperatura_c': 'float64', 'energia_kwh': 'float64'})
    i = pr.sample(frac=0.02, random_state=21).index; pr.loc[i, 'energia_kwh'] = np.nan; log('produccion_2025-06', 'nulos', f'{len(i)} lecturas de energía vacías')
    i = pr.sample(frac=0.005, random_state=22).index; pr.loc[i, 'energia_kwh'] = pr.loc[i, 'energia_kwh'] * 1000; log('produccion_2025-06', 'atípicos', f'{len(i)} lecturas en Wh en lugar de kWh')
    i = pr.sample(frac=0.01, random_state=23).index; pr.loc[i, 'temperatura_c'] = -99; log('produccion_2025-06', 'centinela', f'{len(i)} temperaturas -99 (sensor sin dato)')
    pr = pd.concat([pr, pr.sample(60, random_state=24)]).sort_values(['instalacion_id', 'fecha_hora']); log('produccion_2025-06', 'duplicados', '60 lecturas repetidas')
    pr['fecha_hora'] = pr.fecha_hora.dt.strftime('%d/%m/%Y %H:%M')
    return c, p, q, pr


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--salida', default='alisios'); ap.add_argument('--anio-inicio', type=int, default=2024); ap.add_argument('--anio-fin', type=int, default=2025)
    a = ap.parse_args(); out = Path(a.salida); limpio, sucio, doc = out / 'limpio', out / 'sucio', out / 'docente'
    for d in (limpio, sucio, doc): d.mkdir(parents=True, exist_ok=True)
    registro = []
    def log(tabla, tipo, detalle): registro.append((tabla, tipo, detalle))

    inst = pd.DataFrame(INSTALACIONES, columns=['instalacion_id', 'nombre', 'municipio', 'latitud', 'longitud', 'potencia_kwp', 'tipo', 'fecha_alta'])
    prod, paradas = generar_produccion(a.anio_inicio, a.anio_fin)
    clientes = generar_clientes(); productos, pedidos, lineas = generar_pedidos(clientes, a.anio_inicio, a.anio_fin)
    inc = generar_incidencias(paradas, a.anio_inicio, a.anio_fin)
    prod_diaria = prod.assign(fecha=prod.fecha_hora.dt.date).groupby(['instalacion_id', 'fecha'], as_index=False).agg(energia_kwh=('energia_kwh', 'sum'), irradiacion_wh_m2=('irradiancia_wm2', 'sum'), temperatura_media_c=('temperatura_c', 'mean'), temperatura_max_c=('temperatura_c', 'max')).round(2)

    # limpio
    tablas = {'instalaciones': inst, 'clientes': clientes, 'productos': productos, 'pedidos': pedidos, 'lineas_pedido': lineas, 'incidencias': inc, 'produccion_diaria': prod_diaria}
    for n, df in tablas.items(): df.to_csv(limpio / f'{n}.csv', index=False, encoding='utf-8')
    prod.to_csv(limpio / 'produccion_horaria.csv', index=False)
    try:
        prod.to_parquet(limpio / 'produccion_horaria.parquet', index=False); prod_diaria.to_parquet(limpio / 'produccion_diaria.parquet', index=False)
    except Exception as e: print('Parquet no escrito (instala pyarrow):', e)
    db = limpio / 'alisios.db'; db.unlink(missing_ok=True)
    with sqlite3.connect(db) as con:
        for n, df in tablas.items():
            d = df.copy()
            for col in d.columns:
                if str(d[col].dtype).startswith('datetime'): d[col] = d[col].dt.strftime('%Y-%m-%d %H:%M:%S')
                elif d[col].dtype == object and len(d) and isinstance(d[col].dropna().iloc[0] if len(d[col].dropna()) else '', pd.Timestamp.date.__class__): d[col] = d[col].astype(str)
                elif d[col].dtype == bool: d[col] = d[col].astype(int)
            d.astype({c: str for c in d.columns if d[c].dtype == object}).to_sql(n, con, index=False, if_exists='replace')
        prod.assign(fecha_hora=prod.fecha_hora.dt.strftime('%Y-%m-%d %H:%M:%S')).to_sql('produccion_horaria', con, index=False, if_exists='replace')
        con.executescript('CREATE INDEX IF NOT EXISTS ix_ped_cli ON pedidos(cliente_id); CREATE INDEX IF NOT EXISTS ix_prod ON produccion_horaria(instalacion_id, fecha_hora);')

    # sucio
    c, p, q, pr = ensuciar(clientes, pedidos, inc, prod, log)
    c.to_csv(sucio / 'clientes.csv', index=False, sep=';', decimal=',', encoding='latin-1', errors='replace'); log('clientes', 'fichero', 'CSV con separador ";", decimal "," y codificación latin-1')
    with pd.ExcelWriter(sucio / 'clientes_y_pedidos.xlsx', engine='openpyxl') as xw:
        pd.DataFrame({'Alisios Renovables, S.L.': ['Exportación de clientes y pedidos', 'Generado por el ERP el 01/07/2025', '']}).to_excel(xw, sheet_name='Portada', index=False)
        c.to_excel(xw, sheet_name='Clientes', index=False, startrow=3)
        p.to_excel(xw, sheet_name='Pedidos', index=False, startrow=3)
        pd.DataFrame({'nota': ['Las tres filas superiores de cada hoja son cabecera del ERP; los datos empiezan en la fila 5.']}).to_excel(xw, sheet_name='Notas', index=False)
    log('clientes_y_pedidos.xlsx', 'fichero', 'libro con hoja Portada, cabeceras en las 3 primeras filas (datos desde la fila 5) y hoja Notas')
    p.to_csv(sucio / 'pedidos.csv', index=False); log('pedidos', 'fichero', 'CSV estándar (UTF-8, coma)')
    q.to_json(sucio / 'incidencias.json', orient='records', force_ascii=False, indent=1); log('incidencias', 'fichero', 'JSON de registros (orient=records)')
    pr.to_csv(sucio / 'produccion_2025-06.csv', index=False, sep='\t'); log('produccion_2025-06', 'fichero', 'TSV (tabulador), fechas dd/mm/aaaa HH:MM')

    # docente
    with open(doc / 'defectos_inyectados.md', 'w', encoding='utf-8') as f:
        f.write('# Defectos inyectados en alisios/sucio (verdad conocida para el docente)\n\nSemilla: %d. Generado con generar_alisios.py.\n\n| Tabla | Tipo de defecto | Detalle |\n|---|---|---|\n' % SEED)
        for t in registro: f.write(f'| {t[0]} | {t[1]} | {t[2]} |\n')
        f.write('\n## Paradas reales de producción (coinciden con incidencias con parada=True en limpio/incidencias.csv)\n\n')
        f.write(f'{len(paradas)} paradas entre {a.anio_inicio} y {a.anio_fin}; durante ellas la energía horaria es 0.\n')
    resumen = {n: len(df) for n, df in tablas.items()}; resumen['produccion_horaria'] = len(prod)
    (doc / 'resumen.json').write_text(json.dumps(resumen, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(resumen, indent=1, ensure_ascii=False)); print('defectos registrados:', len(registro))


if __name__ == '__main__':
    main()
