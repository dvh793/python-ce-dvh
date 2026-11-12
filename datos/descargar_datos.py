#!/usr/bin/env python3
"""Descarga y congela los conjuntos de datos abiertos reales del paquete de datos del módulo 5101.
Solo usa la biblioteca estándar (urllib) + pandas para aplanar algunos JSON a CSV.

Uso (desde la carpeta datos/):   python descargar_datos.py            # todo
                                 python descargar_datos.py iter meteo  # solo algunos bloques
Bloques: iter  meteo  ree  istac  pvgis  meteo_api(open-meteo)  odc(Open Data Canarias: electricidad ISTAC)

Los ficheros se guardan en reales/<bloque>/ junto con un fuentes.json (URL, fecha de descarga, licencia).
Es idempotente: no vuelve a descargar lo que ya existe (borra el fichero para forzar).
"""
import json, sys, time, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent / 'reales'
UA = {'User-Agent': 'Mozilla/5.0 (paquete de datos docente CIFP Cesar Manrique; 5101 Analisis de datos)'}
REGISTRO = []


def get(url, destino=None, binario=True, reintentos=3):
    """Descarga url en destino (si se indica) y devuelve bytes. Registra la fuente."""
    if destino and Path(destino).exists():
        print('  ya existe', Path(destino).name); return Path(destino).read_bytes()
    for i in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={**UA, 'Accept': 'application/json, text/csv, */*'})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            break
        except Exception as e:
            print('  error', e, '· reintento', i + 1); time.sleep(3 * (i + 1))
    else:
        raise RuntimeError(f'No se pudo descargar {url}')
    if destino:
        Path(destino).parent.mkdir(parents=True, exist_ok=True); Path(destino).write_bytes(data)
        REGISTRO.append({'fichero': str(Path(destino).relative_to(RAIZ)), 'url': url, 'descargado': date.today().isoformat(), 'bytes': len(data)})
        print(f'  {Path(destino).name}  ({len(data)//1024} KB)')
    return data


def ckan_package(base, package_id):
    return json.loads(get(f'{base}/api/3/action/package_show?id={package_id}'))['result']


def ckan_search(base, q, rows=100):
    return json.loads(get(f'{base}/api/3/action/package_search?q={urllib.parse.quote(q)}&rows={rows}'))['result']


# --------------------------------------------------------------------------- bloques
TENERIFE = 'https://datos.tenerife.es/ckan'


def bloque_iter():
    """Energía mensual de 12 plantas FV / parques eólicos del ITER (Cabildo de Tenerife, CC BY) + ubicaciones."""
    d = RAIZ / 'iter'
    for pkg in ['energia-producida-y-consumida-en-plantas-fotovoltaicas-y-parques-eolicos-en-tenerife',
                'infraestructuras-de-generacion-de-energia-en-tenerife']:
        p = ckan_package(TENERIFE, pkg)
        (d / f'{pkg}.package.json').parent.mkdir(parents=True, exist_ok=True)
        (d / f'{pkg}.package.json').write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding='utf-8')
        for r in p['resources']:
            if r['format'].upper() in ('CSV', 'JSON', 'GEOJSON'):
                nombre = r['url'].rsplit('/', 1)[-1]
                get(r['url'], d / nombre)
    # tabla única con todas las plantas (CSV)
    try:
        import pandas as pd
        csvs = sorted(d.glob('datos-mensuales-de-energia-de-*.csv'))
        if csvs:
            df = pd.concat([pd.read_csv(f).assign(fichero=f.name) for f in csvs], ignore_index=True)
            df.to_csv(d / 'energia_mensual_todas_las_plantas.csv', index=False); print('  energia_mensual_todas_las_plantas.csv', df.shape)
    except Exception as e: print('  (no se pudo unir:', e, ')')


ESTACIONES_PREFERIDAS = ['GRANADILLA', 'ABONA', 'MEDANO', 'ARICO', 'GUIMAR', 'GÜIMAR', 'FASNIA', 'ARAFO', 'LA LAGUNA', 'TACORONTE', 'VILAFLOR']
ANIOS_METEO = [2021, 2022, 2023, 2024, 2025]


def bloque_meteo():
    """Datos meteorológicos diarios por sensor de las estaciones de AgroCabildo (Cabildo de Tenerife, CC BY)."""
    d = RAIZ / 'meteo'; d.mkdir(parents=True, exist_ok=True)
    res = ckan_search(TENERIFE, 'datos meteorologicos diarios', rows=300)
    pkgs = [p for p in res['results'] if p['name'].startswith('datos-meteorologicos-diarios')]
    listado = [{'name': p['name'], 'title': p['title'], 'recursos': len(p['resources'])} for p in pkgs]
    (d / 'estaciones_disponibles.json').write_text(json.dumps(listado, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'  {len(pkgs)} estaciones disponibles (lista en estaciones_disponibles.json)')
    elegidas = [p for p in pkgs if any(k in p['title'].upper() for k in ESTACIONES_PREFERIDAS)]
    if len(elegidas) < 3: elegidas = (elegidas + pkgs)[:4]
    for p in elegidas[:6]:
        print(' estación:', p['title'])
        for r in p['resources']:
            if r['format'].upper() == 'CSV' and any(str(a) in r['name'] for a in ANIOS_METEO):
                get(r['url'], d / r['url'].rsplit('/', 1)[-1])
            if 'iccionario' in r['name'] and not (d / 'diccionario-de-datos-de-datos-meteorologicos-diarios.json').exists():
                get(r['url'], d / 'diccionario-de-datos-de-datos-meteorologicos-diarios.json')


REE = 'https://apidatos.ree.es/es/datos'


def bloque_ree(anio_ini=2023, anio_fin=2025):
    """REData (Red Eléctrica): demanda diaria y estructura de generación mensual del sistema canario."""
    import pandas as pd
    d = RAIZ / 'ree'; d.mkdir(parents=True, exist_ok=True)
    geo = 'geo_trunc=electric_system&geo_limit=canarias&geo_ids=8742'
    filas = []
    for anio in range(anio_ini, anio_fin + 1):
        for mes in range(1, 13):
            fin = pd.Timestamp(anio, mes, 1) + pd.offsets.MonthEnd(0)
            if fin > pd.Timestamp.today(): break
            url = f'{REE}/demanda/evolucion?start_date={anio}-{mes:02d}-01T00:00&end_date={fin:%Y-%m-%d}T23:59&time_trunc=day&{geo}'
            js = json.loads(get(url, d / 'json' / f'demanda_diaria_{anio}-{mes:02d}.json'))
            for serie in js['included']:
                for v in serie['attributes']['values']:
                    filas.append({'serie': serie['attributes']['title'], 'fecha': v['datetime'][:10], 'valor_mwh': v['value']})
    pd.DataFrame(filas).to_csv(d / 'demanda_diaria_canarias.csv', index=False); print('  demanda_diaria_canarias.csv', len(filas), 'filas')
    filas = []
    for anio in range(anio_ini, anio_fin + 1):
        url = f'{REE}/generacion/estructura-generacion?start_date={anio}-01-01T00:00&end_date={anio}-12-31T23:59&time_trunc=month&{geo}'
        js = json.loads(get(url, d / 'json' / f'generacion_mensual_{anio}.json'))
        for serie in js['included']:
            for v in serie['attributes']['values']:
                filas.append({'tecnologia': serie['attributes']['title'], 'tipo': serie['attributes'].get('type'), 'mes': v['datetime'][:7], 'valor_mwh': v['value'], 'porcentaje': v['percentage']})
    pd.DataFrame(filas).to_csv(d / 'generacion_mensual_canarias.csv', index=False); print('  generacion_mensual_canarias.csv', len(filas), 'filas')


ISTAC = 'https://datos.canarias.es/api/estadisticas/indicators/v1.0'
INDICADORES_ISTAC = ['POBLACION', 'POBLACION_HOMBRES', 'POBLACION_MUJERES', 'MIGRACIONES_SALDO', 'TASA_MORTALIDAD', 'SOCIEDADES_MERCANTILES_AMPLIADAS']


def bloque_istac():
    """ISTAC: indicadores por municipio y año (API de indicadores, JSON) aplanados a CSV."""
    import pandas as pd
    d = RAIZ / 'istac'; d.mkdir(parents=True, exist_ok=True)
    get(f'{ISTAC}/indicators?limit=1000', d / 'catalogo_indicadores.json')
    for ind in INDICADORES_ISTAC:
        try:
            meta = json.loads(get(f'{ISTAC}/indicators/{ind}', d / f'{ind}.meta.json'))
            js = json.loads(get(f'{ISTAC}/indicators/{ind}/data?granularity=GEOGRAPHICAL[MUNICIPALITIES],TIME[YEARLY]&representation=MEASURE[ABSOLUTE]', d / f'{ind}.data.json'))
            dims = js['dimension']; geo = dims['GEOGRAPHICAL']['representation']['index']; tiempo = dims['TIME']['representation']['index']
            geo = sorted(geo, key=geo.get); tiempo = sorted(tiempo, key=tiempo.get); obs = js['observation']
            # el orden habitual de la API es GEOGRAPHICAL > TIME > MEASURE
            filas = [{'indicador': ind, 'codigo_municipio': g, 'anio': t, 'valor': obs[i * len(tiempo) + j]} for i, g in enumerate(geo) for j, t in enumerate(tiempo)]
            df = pd.DataFrame(filas); df['valor'] = pd.to_numeric(df.valor, errors='coerce')
            df.to_csv(d / f'{ind}_municipios.csv', index=False); print(f'  {ind}_municipios.csv', df.shape)
        except Exception as e:
            print('  indicador', ind, 'no descargado:', e)
    # nombres de municipios (valores geográficos)
    try:
        get(f'{ISTAC}/geographicalValues?granularityCode=MUNICIPALITIES&limit=1000', d / 'municipios.json')
    except Exception as e: print('  municipios.json no disponible:', e)


PLANTAS = [('abona', 28.078, -16.520), ('guimar', 28.306, -16.389), ('la_guancha', 28.371, -16.653)]


def bloque_pvgis(anio_ini=2021, anio_fin=2023):
    """PVGIS (JRC): radiación horaria y producción FV simulada (1 kWp) en las coordenadas de tres plantas."""
    d = RAIZ / 'pvgis'; d.mkdir(parents=True, exist_ok=True)
    for nombre, lat, lon in PLANTAS:
        url = f'https://re.jrc.ec.europa.eu/api/v5_3/seriescalc?lat={lat}&lon={lon}&startyear={anio_ini}&endyear={anio_fin}&outputformat=csv&pvcalculation=1&peakpower=1&loss=14&angle=20&aspect=0'
        get(url, d / f'pvgis_horario_{nombre}_{anio_ini}-{anio_fin}.csv')


def bloque_meteo_api(ini='2021-01-01', fin='2025-12-31'):
    """Open-Meteo (archivo ERA5): horario de temperatura, radiación y viento en las coordenadas de tres plantas."""
    d = RAIZ / 'open-meteo'; d.mkdir(parents=True, exist_ok=True)
    for nombre, lat, lon in PLANTAS:
        url = (f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={ini}&end_date={fin}'
               f'&hourly=temperature_2m,shortwave_radiation,direct_radiation,wind_speed_10m,cloud_cover,precipitation&timezone=Atlantic%2FCanary&format=csv')
        get(url, d / f'openmeteo_horario_{nombre}_{ini[:4]}-{fin[:4]}.csv')


ODC = 'https://datos.canarias.es/catalogos/general'


def bloque_odc():
    """Open Data Canarias: producción neta de electricidad según fuentes por islas (ISTAC)."""
    d = RAIZ / 'open-data-canarias'; d.mkdir(parents=True, exist_ok=True)
    res = ckan_search(ODC, 'Producción neta de electricidad según fuentes de energía', rows=5)
    for p in res['results'][:2]:
        (d / f"{p['name']}.package.json").write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding='utf-8')
        for r in p['resources']:
            if r['format'].upper() in ('CSV', 'XLSX', 'JSON', 'TSV'):
                get(r['url'], d / f"{p['name'][:40]}.{r['format'].lower()}")


BLOQUES = {'iter': bloque_iter, 'meteo': bloque_meteo, 'ree': bloque_ree, 'istac': bloque_istac, 'pvgis': bloque_pvgis, 'meteo_api': bloque_meteo_api, 'odc': bloque_odc}

if __name__ == '__main__':
    pedidos = sys.argv[1:] or list(BLOQUES)
    RAIZ.mkdir(exist_ok=True)
    for b in pedidos:
        print(f'== {b}: {BLOQUES[b].__doc__.strip()}')
        try: BLOQUES[b]()
        except Exception as e: print('  BLOQUE FALLIDO:', e)
    fuentes = RAIZ / 'fuentes.json'
    previas = json.loads(fuentes.read_text(encoding='utf-8')) if fuentes.exists() else []
    fuentes.write_text(json.dumps(previas + REGISTRO, ensure_ascii=False, indent=1), encoding='utf-8')
    print('Registro de fuentes en', fuentes)
