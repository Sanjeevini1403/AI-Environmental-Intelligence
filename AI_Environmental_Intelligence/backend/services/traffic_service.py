"""
Traffic Density & Congestion Service.

Simulates and computes real-time traffic congestion levels, traffic delay factors,
and segment-by-segment congestion profiles for routes and city grids.
Correlates urban traffic density with vehicular pollutant emission hot spots.
"""

from datetime import datetime
import math
from typing import List, Dict, Any


def get_current_traffic_factor() -> Dict[str, Any]:
    """
    Determines baseline city-wide traffic condition based on time-of-day peak hours:
    - Morning Rush (08:30 - 11:30): Heavy
    - Midday Normal (11:30 - 17:00): Moderate
    - Evening Rush (17:00 - 21:00): Heavy / Severe
    - Night / Early Morning (21:00 - 08:30): Light
    """
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    time_float = hour + (minute / 60.0)

    if 8.5 <= time_float <= 11.5:
        return {
            "period": "Morning Peak",
            "congestion_level": "heavy",
            "base_delay_factor": 1.45,
            "avg_speed_kmh": 22,
            "description": "High vehicular congestion during morning office commute."
        }
    elif 17.0 <= time_float <= 21.0:
        return {
            "period": "Evening Peak",
            "congestion_level": "heavy",
            "base_delay_factor": 1.60,
            "avg_speed_kmh": 18,
            "description": "Severe traffic congestion during evening commute hours."
        }
    elif 11.5 < time_float < 17.0:
        return {
            "period": "Midday Normal",
            "congestion_level": "moderate",
            "base_delay_factor": 1.15,
            "avg_speed_kmh": 32,
            "description": "Moderate traffic flow with sporadic junction delays."
        }
    else:
        return {
            "period": "Off-Peak / Night",
            "congestion_level": "light",
            "base_delay_factor": 1.00,
            "avg_speed_kmh": 45,
            "description": "Free-flowing traffic across city corridors."
        }


def evaluate_route_traffic(path_points: List[Dict[str, float]], base_duration_sec: float) -> Dict[str, Any]:
    """
    Evaluates traffic congestion segment-by-segment along a route's path.
    Returns:
    - overall congestion level (light, moderate, heavy)
    - duration_in_traffic_seconds
    - duration_in_traffic_text
    - traffic_delay_minutes
    - colored traffic segments for Leaflet polylines (green, orange, red)
    """
    if not path_points:
        return {
            "congestion_level": "moderate",
            "duration_in_traffic_sec": base_duration_sec,
            "duration_in_traffic_text": f"{round(base_duration_sec / 60)} mins",
            "delay_mins": 0,
            "traffic_segments": []
        }

    curr_traffic = get_current_traffic_factor()
    base_factor = curr_traffic["base_delay_factor"]

    # Segment path into 3-8 logical chunks to show varying congestion
    n_points = len(path_points)
    n_segments = min(6, max(3, n_points // 10))
    chunk_size = max(1, n_points // n_segments)

    traffic_segments = []
    total_weighted_delay = 0.0

    traffic_profiles = [
        {"status": "light", "color": "#10B981", "delay": 1.02, "label": "Free Flow"},
        {"status": "moderate", "color": "#F59E0B", "delay": 1.25, "label": "Moderate Traffic"},
        {"status": "heavy", "color": "#EF4444", "delay": 1.70, "label": "Heavy Congestion"}
    ]

    for s_idx in range(n_segments):
        start_i = s_idx * chunk_size
        end_i = (s_idx + 1) * chunk_size if s_idx < n_segments - 1 else n_points - 1
        
        # Pseudo-deterministic pseudo-random variation based on coordinates & peak factor
        pt = path_points[start_i]
        hash_val = int((abs(pt["lat"] * 1000) + abs(pt["lng"] * 1000)) * 7) % 100

        if base_factor > 1.4:  # Rush hour
            if hash_val < 50:
                prof = traffic_profiles[2] # heavy
            elif hash_val < 85:
                prof = traffic_profiles[1] # moderate
            else:
                prof = traffic_profiles[0] # light
        elif base_factor > 1.1: # Midday
            if hash_val < 25:
                prof = traffic_profiles[2]
            elif hash_val < 70:
                prof = traffic_profiles[1]
            else:
                prof = traffic_profiles[0]
        else: # Off-peak
            if hash_val < 80:
                prof = traffic_profiles[0]
            else:
                prof = traffic_profiles[1]

        total_weighted_delay += prof["delay"]
        traffic_segments.append({
            "start_index": start_i,
            "end_index": end_i,
            "status": prof["status"],
            "color": prof["color"],
            "label": prof["label"],
            "speed_kmh": round(40 / prof["delay"])
        })

    avg_delay_factor = total_weighted_delay / n_segments
    duration_in_traffic = round(base_duration_sec * avg_delay_factor)
    delay_sec = max(0, duration_in_traffic - base_duration_sec)
    delay_mins = round(delay_sec / 60)

    # Format duration string
    mins = round(duration_in_traffic / 60)
    if mins < 60:
        duration_text = f"{mins} mins"
    else:
        hrs = mins // 60
        rem = mins % 60
        duration_text = f"{hrs} hr {rem} min" if rem else f"{hrs} hr"

    overall_status = "heavy" if avg_delay_factor >= 1.4 else ("moderate" if avg_delay_factor >= 1.15 else "light")

    return {
        "congestion_level": overall_status,
        "duration_in_traffic_sec": duration_in_traffic,
        "duration_in_traffic_text": duration_text,
        "delay_minutes": delay_mins,
        "traffic_segments": traffic_segments,
        "current_peak_status": curr_traffic["period"]
    }


def get_city_traffic_hotspots(center_lat: float, center_lon: float) -> List[Dict[str, Any]]:
    """
    Returns prominent traffic bottleneck points around a city center for map visualization.
    """
    curr = get_current_traffic_factor()
    hotspots = [
        {"name": "University Circle / Flyover Junction", "lat_offset": 0.015, "lon_offset": -0.012, "level": curr["congestion_level"]},
        {"name": "Railway Station & Bus Terminal", "lat_offset": 0.008, "lon_offset": 0.018, "level": "heavy"},
        {"name": "Bypass Highway Interchange", "lat_offset": -0.024, "lon_offset": -0.035, "level": "heavy" if curr["congestion_level"] == "heavy" else "moderate"},
        {"name": "City Center Market / Commercial Hub", "lat_offset": -0.005, "lon_offset": 0.004, "level": "moderate"},
        {"name": "IT Tech Corridor Entry", "lat_offset": 0.042, "lon_offset": -0.051, "level": curr["congestion_level"]}
    ]

    results = []
    for h in hotspots:
        results.append({
            "name": h["name"],
            "latitude": round(center_lat + h["lat_offset"], 4),
            "longitude": round(center_lon + h["lon_offset"], 4),
            "congestion": h["level"],
            "color": "#EF4444" if h["level"] == "heavy" else "#F59E0B"
        })
    return results
