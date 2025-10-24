"""
y por ejemplo, si tengo la informacion de la concentracion de SO2 por cada hora en 13 puntos distintos de la ciudad, y tengo esa api que me permite ver en un momento exacto de tiempo como se mueve el viento, como plantearias que puedo determinar la contribucion que tienen a la contaminacion de toda un area
"""
import folium
from folium import Map, Circle, Marker

# Coordenadas de estaciones (latitud, longitud, elevación)
stations_dd_elev = {
    "SE":  (25.665278, -100.243611, 500),
    "NE":  (25.744722, -100.253056, 474),
    "CE":  (25.675833, -100.338333, 562),
    "NO":  (25.762778, -100.369167, 568),
    "SO":  (25.675556, -100.458056, 674),
    "NO2": (25.800278, -100.584444, 702),
    "NTE": (25.798611, -100.327222, 503),
    "NE2": (25.777222, -100.188056, 432),
    "SE2": (25.645833, -100.095278, 387),
    "SO2": (25.665000, -100.412778, 636),
    "SE3": (25.601111, -99.999167, 334),
    "SUR": (25.616944, -100.273889, 555),
    "NTE2":(25.729722, -100.310000, 520),
    "NE3": (25.790556, -100.078333, 346),
    "NO3": (25.768333, -100.463611, 607),
}

# Coordenadas de focos de emisión (nombre, lat, lon, elevación)
emission_sources = {
    "Refinería Cadereyta": (25.58890383518717, -99.94429923536717, 360),
    "Foco San Nicolás (Zinc Nacional)": (25.756029481005335, -100.32114422585992, 400),
}

# Crear el mapa centrado en Monterrey
map_center = [25.68, -100.32]
m = Map(location=map_center, zoom_start=11, tiles='cartodbpositron')

# Añadir círculos de 2 km a cada estación
for station, (lat, lon, elev) in stations_dd_elev.items():
    Circle(
        location=(lat, lon),
        radius=5000,  # 2 km
        color='blue',
        fill=True,
        fill_opacity=0.2,
        popup=station
    ).add_to(m)

# Añadir marcadores para focos de emisión
for name, (lat, lon, elev) in emission_sources.items():
    Marker(
        location=(lat, lon),
        popup=name,
        icon=folium.Icon(color='red', icon='fire', prefix='fa')
    ).add_to(m)

# Guardar como archivo HTML
m.save("estaciones_y_focos_emision.html")
