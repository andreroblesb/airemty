import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import numpy as np

# Archivos
archivo_estaciones = "distancias_a_refineria.csv"
archivo_manzanas = "manzanas_urbanas/2020_1_19_M.shp"
archivo_poblacion = "RESAGEBURB_19XLSX20.xlsx"

# --- 1) Cargar manzanas urbanas ---
manzanas = gpd.read_file(archivo_manzanas)
if manzanas.crs is None or manzanas.crs.to_string().upper() != "EPSG:4326":
    manzanas = manzanas.to_crs(epsg=4326)

# --- 2) Cargar población por manzana ---
cols = ['ENTIDAD', 'MUN', 'LOC', 'AGEB', 'MZA']
data = pd.read_excel(
    archivo_poblacion,
    dtype={**{c: 'string' for c in cols}, 'POBTOT': 'Int64'},
    keep_default_na=False
)
data['CVEGEO'] = data[cols].agg(''.join, axis=1)
df_pob = data[['CVEGEO', 'POBTOT']].copy()

# --- 3) Crear círculo geográfico de 2km ---
def crear_circulo(lat, lon, radio_m=2000, n_puntos=32):
    # Aproximación de 1 grado latitud = 111.32 km
    # Convertimos el radio a grados
    radio_grados = radio_m / 1000.0 / 111.32
    angulos = np.linspace(0, 2*np.pi, n_puntos, endpoint=False)
    puntos = [
        Point(
            lon + radio_grados * np.cos(a) / np.cos(np.radians(lat)),  # corrige longitudinalmente por latitud
            lat + radio_grados * np.sin(a)
        ) for a in angulos
    ]
    return Polygon([[p.x, p.y] for p in puntos])

# --- 4) Cargar estaciones ---
df_estaciones = pd.read_csv(archivo_estaciones)

# --- 5) Calcular población dentro del círculo ---
def poblacion_en_poligono(geom, manzanas, df_pob):
    dentro = manzanas[manzanas.within(geom)][['CVEGEO']].copy()
    res = dentro.merge(df_pob, on='CVEGEO', how='left')
    total = res['POBTOT'].fillna(0).sum()
    return int(total)

# --- 6) Iterar por estaciones y calcular población ---
resultados = []

for _, row in df_estaciones.iterrows():
    poligono = crear_circulo(row['lat'], row['lon'])
    total = poblacion_en_poligono(poligono, manzanas, df_pob)
    resultados.append({
        "estacion": row['station'],
        "poblacion_2km": total
    })
    print(f"{row['station']}: {total:,} personas")

# --- 7) Guardar resultado ---
df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv("poblacion_por_estacion_2km.csv", index=False, encoding="utf-8-sig")
print("\n✅ CSV generado: poblacion_por_estacion_2km.csv")
print(df_resultado.head())
