"""
Pollution Heatmap / Zone Service.

Builds a small lat/lon grid around a center point and reuses the existing
air_quality_service + ML model (prediction_service) to get a predicted AQI
category at each grid point. This gives a "pollution zone" view without
needing any paid heatmap/mapping API.

Grid size is deliberately kept small (max 5x5) to be polite to the free
Open-Meteo API and keep response times reasonable for a live demo.
"""

import math
from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.services.air_quality_service import get_air_quality
from backend.services.prediction_service import predict_aqi


def _generate_grid(center_lat, center_lon, radius_km, grid_size):

    if grid_size <= 1:
        return [(center_lat, center_lon)]

    lat_step = (radius_km / 111.0) * 2 / (grid_size - 1)
    lon_step = (radius_km / (111.0 * math.cos(math.radians(center_lat)))) * 2 / (grid_size - 1)

    half = (grid_size - 1) / 2
    points = []

    for i in range(grid_size):
        for j in range(grid_size):
            lat = center_lat + (i - half) * lat_step
            lon = center_lon + (j - half) * lon_step
            points.append((lat, lon))

    return points


def _fetch_point(lat, lon):

    try:
        air = get_air_quality(latitude=lat, longitude=lon)

        if air["pm2_5"] is None:
            return None

        prediction = predict_aqi(
            pm25=air["pm2_5"],
            pm10=air["pm10"],
            no2=air["nitrogen_dioxide"],
            so2=air["sulphur_dioxide"],
            co=air["carbon_monoxide"],
            o3=air["ozone"]
        )

        return {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "predicted_aqi": prediction["predicted_aqi"],
            "category": prediction["category"],
            "pm2_5": air["pm2_5"],
            "pm10": air["pm10"]
        }

    except Exception:
        return None


def get_pollution_grid(center_lat, center_lon, radius_km=10, grid_size=4):

    grid_size = max(2, min(grid_size, 5))
    points = _generate_grid(center_lat, center_lon, radius_km, grid_size)

    results = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(_fetch_point, lat, lon) for lat, lon in points]

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results
