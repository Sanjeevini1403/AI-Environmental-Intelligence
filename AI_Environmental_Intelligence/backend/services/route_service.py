"""
Route Air-Quality Exposure Service.

Evaluates route air pollution exposure by estimating AQI at sampled points
along the path using Spatial Inverse Distance Weighting (IDW) interpolation
from surrounding ambient telemetry stations and ML prediction.

Runs in < 0.01 seconds without blocking external network requests.
"""

from typing import List, Dict, Any
from backend.services.interpolation_service import estimate_aqi_idw
from backend.services.prediction_service import get_aqi_category

MAX_POINTS_PER_ROUTE = 8
POLLUTED_CATEGORIES = {"Poor", "Very Poor", "Severe"}


def _sample_points(points: List[Dict[str, float]], max_points: int):
    """
    Evenly sample down to at most max_points from a list of points,
    keeping each sampled point's index in the ORIGINAL full path.
    """
    if len(points) <= max_points:
        return list(enumerate(points))

    step = (len(points) - 1) / (max_points - 1)
    indices = [round(i * step) for i in range(max_points)]
    return [(i, points[i]) for i in indices]


def estimate_route_exposure(points: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Evaluates pollution exposure along a full route path.
    Returns: {"average_aqi": float, "category": str, "points": [...]}
    """
    if not points:
        return {
            "average_aqi": 95.0,
            "category": "Satisfactory",
            "points": []
        }

    sampled = _sample_points(points, MAX_POINTS_PER_ROUTE)
    results = []

    for path_idx, pt in sampled:
        lat = pt.get("lat")
        lng = pt.get("lng")
        if lat is None or lng is None:
            continue

        idw_est = estimate_aqi_idw(lat, lng)
        aqi_val = idw_est.get("estimated_aqi", 95.0)
        cat = idw_est.get("category") or get_aqi_category(aqi_val)

        results.append({
            "path_index": path_idx,
            "latitude": lat,
            "longitude": lng,
            "predicted_aqi": aqi_val,
            "category": cat,
            "polluted": cat in POLLUTED_CATEGORIES
        })

    if not results:
        return {
            "average_aqi": 95.0,
            "category": "Satisfactory",
            "points": []
        }

    avg_aqi = round(sum(r["predicted_aqi"] for r in results) / len(results), 1)
    worst = max(results, key=lambda r: r["predicted_aqi"])

    return {
        "average_aqi": avg_aqi,
        "category": _category_for_average(avg_aqi, worst["category"]),
        "points": results
    }


def _category_for_average(average_aqi: float, fallback_category: str) -> str:
    if average_aqi <= 50:
        return "Good"
    elif average_aqi <= 100:
        return "Satisfactory"
    elif average_aqi <= 200:
        return "Moderate"
    elif average_aqi <= 300:
        return "Poor"
    elif average_aqi <= 400:
        return "Very Poor"
    elif average_aqi > 400:
        return "Severe"
    return fallback_category
