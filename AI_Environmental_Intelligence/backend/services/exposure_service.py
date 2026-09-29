"""
Personal Exposure History & Time-Series Logging Service.

Maintains persistent storage (SQLite) for:
- User travel history and route exposure records
- Time-series sensor observations
- User profile sensitivity configurations
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "exposure_history.db")


def _get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the SQLite schema for travel logs and exposure metrics."""
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trip_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        route_type TEXT NOT NULL,
        distance_km REAL,
        duration_mins REAL,
        avg_aqi REAL,
        cumulative_exposure REAL,
        aqi_category TEXT,
        health_profile TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sensor_readings_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        location_name TEXT,
        latitude REAL,
        longitude REAL,
        pm2_5 REAL,
        pm10 REAL,
        no2 REAL,
        so2 REAL,
        co REAL,
        o3 REAL,
        predicted_aqi REAL,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()


# Initialize database tables on import
init_db()


def save_trip_exposure(
    origin: str,
    destination: str,
    route_type: str,
    distance_km: float,
    duration_mins: float,
    avg_aqi: float,
    cumulative_exposure: float,
    aqi_category: str,
    health_profile: str = "normal"
) -> Dict[str, Any]:
    """Saves a completed trip's exposure metrics to the history log."""
    conn = _get_connection()
    cur = conn.cursor()
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M")

    cur.execute("""
    INSERT INTO trip_history (
        timestamp, origin, destination, route_type, distance_km,
        duration_mins, avg_aqi, cumulative_exposure, aqi_category, health_profile
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now_iso, origin, destination, route_type, distance_km,
        duration_mins, avg_aqi, cumulative_exposure, aqi_category, health_profile
    ))

    trip_id = cur.lastrowid
    conn.commit()
    conn.close()

    return {
        "success": True,
        "trip_id": trip_id,
        "timestamp": now_iso,
        "message": "Trip exposure logged successfully"
    }


def get_trip_history(limit: int = 15) -> List[Dict[str, Any]]:
    """Retrieves recent personal trip exposure logs."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM trip_history ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "origin": r["origin"],
            "destination": r["destination"],
            "route_type": r["route_type"],
            "distance_km": r["distance_km"],
            "duration_mins": r["duration_mins"],
            "avg_aqi": r["avg_aqi"],
            "cumulative_exposure": r["cumulative_exposure"],
            "aqi_category": r["aqi_category"],
            "health_profile": r["health_profile"]
        })
    return results


def get_daily_exposure_summary() -> Dict[str, Any]:
    """
    Computes cumulative daily particulate exposure dosage score:
    Dosage = sum(duration_hours * AQI).
    Safe threshold is approximately 250 AQI-hours per day.
    """
    history = get_trip_history(limit=50)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_trips = [t for t in history if t["timestamp"].startswith(today_str)]

    total_exposure = sum(t["cumulative_exposure"] or (t["avg_aqi"] * (t["duration_mins"] / 60.0)) for t in today_trips)
    total_km = sum(t["distance_km"] or 0 for t in today_trips)

    # Health safety threshold index
    safe_daily_limit = 250.0
    risk_level = "Low" if total_exposure < 150 else ("Moderate" if total_exposure < 250 else "High")

    return {
        "today_trips_count": len(today_trips),
        "total_distance_km": round(total_km, 1),
        "cumulative_aqi_exposure": round(total_exposure, 1),
        "safe_daily_limit": safe_daily_limit,
        "exposure_percentage": min(100, round((total_exposure / safe_daily_limit) * 100)),
        "risk_level": risk_level,
        "recommendation": "Well within safety threshold" if total_exposure < 150 else "Consider minimizing outdoor transit for the rest of today."
    }
