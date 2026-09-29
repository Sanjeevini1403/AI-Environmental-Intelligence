"""
Route Directions, Multi-Modal Mobility & Traffic-Aware Service.

Supports realistic mode-specific speed, duration, traffic delay, and health exposure modeling for:
- Car / Cab: standard driving speed with congestion delay
- Two-Wheeler (Motorcycle / Scooter): weaves through traffic (faster in jams, but direct exhaust exposure)
- Cycling: ~15 km/h, bypasses vehicle gridlock, physical ventilation rate multiplier, calorie burn
- Walking: ~4.8 km/h, bypasses traffic, calorie burn, physical inhalation dosage

Includes a High-Resilience Fallback Geometry Engine that guarantees realistic route paths
even if public OSRM servers are offline or rate-limited.
"""

import math
import requests
from typing import Optional, Dict, Any, List
from backend.services.route_service import estimate_route_exposure
from backend.services.traffic_service import evaluate_route_traffic
from backend.services.parking_service import find_nearest_parking
from backend.services.interpolation_service import haversine_distance_km

OSRM_URL = "http://router.project-osrm.org/route/v1/driving/{coords}"

MAX_ROUTES = 3
DETOUR_FRACTION = 0.18


def _format_distance(meters: float) -> str:
    km = meters / 1000.0
    return f"{km:.1f} km"


def _format_duration(seconds: float) -> str:
    minutes = max(1, round(seconds / 60.0))
    if minutes < 60:
        return f"{minutes} mins"
    hours = minutes // 60
    remaining = minutes % 60
    return f"{hours} hr {remaining} min" if remaining else f"{hours} hr"


def _osrm_request(coords: str, alternatives: str = "true") -> Optional[Dict[str, Any]]:
    url = OSRM_URL.format(coords=coords)
    params = {
        "alternatives": alternatives,
        "overview": "full",
        "geometries": "geojson"
    }
    try:
        response = requests.get(url, params=params, timeout=3.5)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and data.get("routes"):
                return data
    except Exception:
        pass
    return None


def _generate_detour_route(origin_lat, origin_lon, dest_lat, dest_lon, side):
    mid_lat = (origin_lat + dest_lat) / 2
    mid_lon = (origin_lon + dest_lon) / 2
    dlat = dest_lat - origin_lat
    dlon = dest_lon - origin_lon

    waypoint_lat = mid_lat + (-dlon) * side * DETOUR_FRACTION
    waypoint_lon = mid_lon + dlat * side * DETOUR_FRACTION

    coords = (
        f"{origin_lon},{origin_lat};"
        f"{waypoint_lon},{waypoint_lat};"
        f"{dest_lon},{dest_lat}"
    )

    data = _osrm_request(coords, alternatives="false")
    if data and data.get("routes"):
        return data["routes"][0]
    return None


def _is_meaningfully_different(candidate, existing_routes, threshold=0.04):
    for route in existing_routes:
        if route.get("distance", 0) == 0:
            continue
        relative_diff = abs(candidate["distance"] - route["distance"]) / route["distance"]
        if relative_diff < threshold:
            return False
    return True


def compute_mode_metrics(distance_km: float, base_car_duration_sec: float, traffic_delay_sec: float, avg_aqi: float, mode: str = "driving") -> Dict[str, Any]:
    """
    Computes mode-specific travel duration, traffic delays, physical exertion, and inhalation dosage.
    """
    m = mode.lower().strip()

    if "motorcycle" in m or "two" in m or "bike" in m:
        traffic_delay = traffic_delay_sec * 0.45
        duration_sec = (base_car_duration_sec * 0.90) + traffic_delay
        delay_mins = round(traffic_delay / 60.0)
        speed_kmh = round(distance_km / (duration_sec / 3600.0), 1) if duration_sec > 0 else 45.0
        exposure_hrs = duration_sec / 3600.0
        cumulative_exposure = round(avg_aqi * exposure_hrs * 1.35, 1)
        calories = round(distance_km * 7.5)
        health_note = "Direct exposure to vehicular exhaust. N95 respirator mask recommended."

    elif "cycling" in m or "cycle" in m:
        speed_kmh = 15.0
        duration_sec = (distance_km / speed_kmh) * 3600.0
        delay_mins = 0
        exposure_hrs = duration_sec / 3600.0
        cumulative_exposure = round(avg_aqi * exposure_hrs * 2.2, 1)
        calories = round(distance_km * 32.0)
        health_note = "Zero traffic delay. Aerobic inhalation is elevated; avoid heavy exhaust corridors."

    elif "walking" in m or "walk" in m:
        speed_kmh = 4.8
        duration_sec = (distance_km / speed_kmh) * 3600.0
        delay_mins = 0
        exposure_hrs = duration_sec / 3600.0
        cumulative_exposure = round(avg_aqi * exposure_hrs * 1.6, 1)
        calories = round(distance_km * 55.0)
        health_note = "Healthy cardio walk. Protect lungs with an eco-corridor path."

    else:  # Car / Cab (driving)
        duration_sec = base_car_duration_sec + traffic_delay_sec
        delay_mins = round(traffic_delay_sec / 60.0)
        speed_kmh = round(distance_km / (duration_sec / 3600.0), 1) if duration_sec > 0 else 38.0
        exposure_hrs = duration_sec / 3600.0
        cumulative_exposure = round(avg_aqi * exposure_hrs * 1.0, 1)
        calories = round(distance_km * 2.0)
        health_note = "Enclosed cabin. Keep AC on air-recirculation mode during traffic congestion."

    return {
        "mode": m,
        "speed_kmh": speed_kmh,
        "duration_sec": max(60, round(duration_sec)),
        "duration_text": _format_duration(duration_sec),
        "delay_minutes": delay_mins,
        "cumulative_exposure": cumulative_exposure,
        "calories_burned": calories,
        "health_note": health_note
    }


def _generate_synthetic_routes(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float) -> List[Dict[str, Any]]:
    """
    Generates 3 realistic road-corridor route options using smooth multi-waypoint spline arcs
    when external OSRM routing is unreachable.
    """
    direct_dist_km = haversine_distance_km(origin_lat, origin_lon, dest_lat, dest_lon)
    direct_dist_km = max(0.5, direct_dist_km)

    dlat = dest_lat - origin_lat
    dlon = dest_lon - origin_lon

    # Lateral offsets for 3 distinct corridors:
    # 0: Cleanest (arc through greener peripheral corridor)
    # 1: Fastest (direct highway/arterial road)
    # 2: Balanced (intermediate city avenue)
    profiles = [
        {"name": "Clean Corridor", "offset": 0.16, "road_winding": 1.28, "speed": 42.0},
        {"name": "Express Corridor", "offset": 0.00, "road_winding": 1.18, "speed": 48.0},
        {"name": "City Arterial", "offset": -0.14, "road_winding": 1.24, "speed": 38.0}
    ]

    synthetic_routes = []
    num_steps = 22

    for p in profiles:
        offset = p["offset"]
        dist_km = direct_dist_km * p["road_winding"]
        dist_meters = dist_km * 1000.0
        duration_sec = (dist_km / p["speed"]) * 3600.0

        coords = []
        for i in range(num_steps + 1):
            t = i / float(num_steps)
            # Quadratic curve offset
            curve_factor = 4.0 * t * (1.0 - t) * offset
            # Perpendicular vector (-dlon, dlat)
            pt_lat = origin_lat + (t * dlat) + (-dlon * curve_factor)
            pt_lon = origin_lon + (t * dlon) + (dlat * curve_factor)
            # Add slight realistic road micro-wiggles
            wiggle = math.sin(t * math.pi * 5) * 0.0008
            coords.append([pt_lon + wiggle, pt_lat + wiggle])

        synthetic_routes.append({
            "distance": dist_meters,
            "duration": duration_sec,
            "geometry": {
                "coordinates": coords
            }
        })

    return synthetic_routes


def get_route_options(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float, mode: str = "driving"):
    coords = f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}"

    osrm_routes = []
    # 1. Try public OSRM router
    data = _osrm_request(coords, alternatives="true")
    if data and data.get("routes"):
        osrm_routes = data["routes"]
        if len(osrm_routes) < 2:
            for side in (1, -1):
                if len(osrm_routes) >= MAX_ROUTES:
                    break
                detour = _generate_detour_route(origin_lat, origin_lon, dest_lat, dest_lon, side)
                if detour and _is_meaningfully_different(detour, osrm_routes):
                    osrm_routes.append(detour)

    # 2. Fallback to resilient synthetic routes if OSRM failed or returned 0 routes
    if not osrm_routes:
        osrm_routes = _generate_synthetic_routes(origin_lat, origin_lon, dest_lat, dest_lon)

    osrm_routes = osrm_routes[:MAX_ROUTES]
    routes = []

    for osrm_route in osrm_routes:
        path_points = [(lat, lon) for lon, lat in osrm_route["geometry"]["coordinates"]]
        sample_points = [{"lat": lat, "lng": lng} for lat, lng in path_points]

        # 1. Evaluate Air Quality Exposure
        exposure = estimate_route_exposure(sample_points)
        avg_aqi = exposure["average_aqi"] or 95.0

        # 2. Evaluate Traffic Density & Congestion along path
        traffic_info = evaluate_route_traffic(sample_points, osrm_route["duration"])
        base_dur = osrm_route["duration"]
        traffic_delay = max(0, traffic_info["duration_in_traffic_sec"] - base_dur)
        dist_km = round(osrm_route["distance"] / 1000.0, 2)

        # 3. Compute Mode Metrics for Selected Mode
        mode_data = compute_mode_metrics(dist_km, base_dur, traffic_delay, avg_aqi, mode=mode)

        # 4. Multi-Modal Comparison across ALL 4 modes for this route
        all_modes_comparison = {
            "car": compute_mode_metrics(dist_km, base_dur, traffic_delay, avg_aqi, mode="driving"),
            "motorcycle": compute_mode_metrics(dist_km, base_dur, traffic_delay, avg_aqi, mode="motorcycle"),
            "cycling": compute_mode_metrics(dist_km, base_dur, traffic_delay, avg_aqi, mode="cycling"),
            "walking": compute_mode_metrics(dist_km, base_dur, traffic_delay, avg_aqi, mode="walking")
        }

        routes.append({
            "path": [{"lat": lat, "lng": lng} for lat, lng in path_points],
            "segments": _build_segments(len(path_points), exposure["points"]),
            "traffic_segments": traffic_info["traffic_segments"],
            "distance_text": _format_distance(osrm_route["distance"]),
            "distance_value": osrm_route["distance"],
            "distance_km": dist_km,
            # Active mode metrics
            "mode": mode,
            "duration_text": mode_data["duration_text"],
            "duration_value": mode_data["duration_sec"],
            "duration_in_traffic_text": mode_data["duration_text"],
            "duration_in_traffic_value": mode_data["duration_sec"],
            "delay_minutes": mode_data["delay_minutes"],
            "congestion_level": traffic_info["congestion_level"],
            "calories_burned": mode_data["calories_burned"],
            "health_note": mode_data["health_note"],
            # Exposure metrics
            "avg_aqi": avg_aqi,
            "cumulative_exposure": mode_data["cumulative_exposure"],
            "aqi_category": exposure["category"],
            # Multi-modal comparison matrix
            "multi_modal_comparison": all_modes_comparison
        })

    labeled_routes = _label_routes(routes)

    # 5. Smart Parking Hubs near destination
    nearby_parking = find_nearest_parking(dest_lat, dest_lon, max_results=3)

    return {
        "routes": labeled_routes,
        "nearby_parking": nearby_parking
    }


def _build_segments(path_length, exposure_points):
    if not exposure_points or path_length < 2:
        return [{"start_index": 0, "end_index": max(path_length - 1, 0), "polluted": False}]

    segments = []
    first = exposure_points[0]
    if first["path_index"] > 0:
        segments.append({
            "start_index": 0,
            "end_index": first["path_index"],
            "polluted": first["polluted"]
        })

    for a, b in zip(exposure_points, exposure_points[1:]):
        segments.append({
            "start_index": a["path_index"],
            "end_index": b["path_index"],
            "polluted": a["polluted"]
        })

    last = exposure_points[-1]
    if last["path_index"] < path_length - 1:
        segments.append({
            "start_index": last["path_index"],
            "end_index": path_length - 1,
            "polluted": last["polluted"]
        })

    return segments


def _label_routes(routes):
    if not routes:
        return routes

    def travel_time(route):
        return route.get("duration_in_traffic_value") or route["duration_value"]

    def exposure_score(route):
        return route["cumulative_exposure"]

    fastest_idx = min(range(len(routes)), key=lambda i: travel_time(routes[i]))
    cleanest_idx = min(range(len(routes)), key=lambda i: exposure_score(routes[i]))

    durations = [travel_time(r) for r in routes]
    exposures = [exposure_score(r) for r in routes]
    min_d, max_d = min(durations), max(durations)
    min_e, max_e = min(exposures), max(exposures)

    def normalize(value, lo, hi):
        return 0.0 if hi == lo else (value - lo) / (hi - lo)

    scores = [
        0.55 * normalize(durations[i], min_d, max_d) + 0.45 * normalize(exposures[i], min_e, max_e)
        for i in range(len(routes))
    ]
    balanced_idx = min(range(len(routes)), key=lambda i: scores[i])

    for i, route in enumerate(routes):
        labels = []
        if i == cleanest_idx:
            labels.append("cleanest")
        if i == fastest_idx:
            labels.append("fastest")
        if i == balanced_idx and "cleanest" not in labels:
            labels.append("balanced")
        if not labels:
            labels.append("alternative")

        route["labels"] = labels
        route["recommended"] = (i == balanced_idx or i == cleanest_idx)

    return routes
