from math import radians, sin, cos, asin, sqrt
import pandas as pd

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
    "SE3": (25.601111,  -99.999167, 334),
    "SUR": (25.616944, -100.273889, 555),
    "NTE2":(25.729722, -100.310000, 520),
    "NE3": (25.790556, -100.078333, 346),
    "NO3": (25.768333, -100.463611, 607),
}

refineria = (25.58890383518717, -99.94429923536717, 360)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088  # Mean Earth radius in kilometers (IUGG)
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2.0)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2.0)**2
    c = 2 * asin(sqrt(a))
    return R * c

rows = []
for name, (lat, lon, elev) in stations_dd_elev.items():
    dist_km = haversine_km(refineria[0], refineria[1], lat, lon)
    delta_elev_m = elev - refineria[2]
    rows.append({
        "station": name,
        "lat": lat,
        "lon": lon,
        "elev_m": elev,
        "distance_km": round(dist_km, 4),
        "delta_elev_m": delta_elev_m
    })

df = pd.DataFrame(rows).sort_values("distance_km").reset_index(drop=True)

csv_path = "distancias_a_refineria.csv"
df.to_csv(csv_path, index=False)
