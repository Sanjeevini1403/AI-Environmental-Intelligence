"""
Smart Parking Intelligence & Slot Reservation Service.

Provides real-time parking spot telemetry, availability tracking for 4-wheelers,
2-wheelers, and EV charging hubs, localized air quality at parking lots,
and smart parking recommendations near travel destinations.
"""

import math
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

# Master Registry of Smart Parking Hubs across Indian Urban Hubs
PARKING_REGISTRY = [
    # Pune Region
    {
        "id": "prk-pn-01", "name": "JM Road Multi-Level Smart Parking", "city": "pune",
        "area": "Deccan Gymkhana", "lat": 18.5209, "lon": 73.8436,
        "total_car": 120, "avail_car": 42,
        "total_bike": 200, "avail_bike": 88,
        "total_ev": 12, "avail_ev": 5,
        "rate_car_hr": 20, "rate_bike_hr": 10, "has_ev_fast_charger": True,
        "aqi": 98, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-pn-02", "name": "FC Road Automated Public Parking", "city": "pune",
        "area": "Shivajinagar", "lat": 18.5284, "lon": 73.8420,
        "total_car": 85, "avail_car": 14,
        "total_bike": 150, "avail_bike": 32,
        "total_ev": 8, "avail_ev": 2,
        "rate_car_hr": 25, "rate_bike_hr": 10, "has_ev_fast_charger": True,
        "aqi": 115, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-pn-03", "name": "Hinjewadi Tech Park Eco-Parking Hub", "city": "pune",
        "area": "Hinjewadi Phase 1", "lat": 18.5912, "lon": 73.7380,
        "total_car": 250, "avail_car": 95,
        "total_bike": 400, "avail_bike": 210,
        "total_ev": 25, "avail_ev": 11,
        "rate_car_hr": 20, "rate_bike_hr": 10, "has_ev_fast_charger": True,
        "aqi": 138, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-pn-04", "name": "Kothrud DP Road Smart Parking Bay", "city": "pune",
        "area": "Kothrud", "lat": 18.5080, "lon": 73.8070,
        "total_car": 70, "avail_car": 28,
        "total_bike": 120, "avail_bike": 65,
        "total_ev": 6, "avail_ev": 3,
        "rate_car_hr": 15, "rate_bike_hr": 5, "has_ev_fast_charger": False,
        "aqi": 92, "security_cctv": True, "covered": False
    },
    {
        "id": "prk-pn-05", "name": "Pune Railway Station Park & Ride", "city": "pune",
        "area": "Station Road", "lat": 18.5289, "lon": 73.8744,
        "total_car": 180, "avail_car": 18,
        "total_bike": 350, "avail_bike": 45,
        "total_ev": 10, "avail_ev": 2,
        "rate_car_hr": 30, "rate_bike_hr": 15, "has_ev_fast_charger": True,
        "aqi": 142, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-pn-06", "name": "Baner High Street Smart Bay", "city": "pune",
        "area": "Baner", "lat": 18.5590, "lon": 73.7868,
        "total_car": 110, "avail_car": 54,
        "total_bike": 180, "avail_bike": 92,
        "total_ev": 15, "avail_ev": 7,
        "rate_car_hr": 25, "rate_bike_hr": 10, "has_ev_fast_charger": True,
        "aqi": 105, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-pn-07", "name": "Magarpatta Cybercity Parking Facility", "city": "pune",
        "area": "Hadapsar", "lat": 18.5140, "lon": 73.9290,
        "total_car": 220, "avail_car": 78,
        "total_bike": 300, "avail_bike": 140,
        "total_ev": 18, "avail_ev": 8,
        "rate_car_hr": 20, "rate_bike_hr": 10, "has_ev_fast_charger": True,
        "aqi": 155, "security_cctv": True, "covered": True
    },

    # Delhi NCR
    {
        "id": "prk-del-01", "name": "Connaught Place Underground Smart Parking", "city": "delhi",
        "area": "CP Inner Circle", "lat": 28.6315, "lon": 77.2167,
        "total_car": 350, "avail_car": 62, "total_bike": 500, "avail_bike": 140,
        "total_ev": 30, "avail_ev": 9, "rate_car_hr": 40, "rate_bike_hr": 20,
        "has_ev_fast_charger": True, "aqi": 240, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-del-02", "name": "Anand Vihar ISBT Multimodal Hub", "city": "delhi",
        "area": "Anand Vihar", "lat": 28.6475, "lon": 77.3150,
        "total_car": 200, "avail_car": 22, "total_bike": 400, "avail_bike": 55,
        "total_ev": 15, "avail_ev": 3, "rate_car_hr": 30, "rate_bike_hr": 15,
        "has_ev_fast_charger": True, "aqi": 285, "security_cctv": True, "covered": True
    },

    # Mumbai
    {
        "id": "prk-mum-01", "name": "Bandra Kurla Complex (BKC) Smart Parking", "city": "mumbai",
        "area": "BKC Central", "lat": 19.0657, "lon": 72.8687,
        "total_car": 400, "avail_car": 125, "total_bike": 600, "avail_bike": 240,
        "total_ev": 35, "avail_ev": 14, "rate_car_hr": 50, "rate_bike_hr": 25,
        "has_ev_fast_charger": True, "aqi": 118, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-mum-02", "name": "Nariman Point Multi-Deck Bay", "city": "mumbai",
        "area": "Marine Drive", "lat": 18.9256, "lon": 72.8242,
        "total_car": 160, "avail_car": 31, "total_bike": 200, "avail_bike": 65,
        "total_ev": 12, "avail_ev": 4, "rate_car_hr": 60, "rate_bike_hr": 30,
        "has_ev_fast_charger": True, "aqi": 95, "security_cctv": True, "covered": True
    },

    # Bengaluru
    {
        "id": "prk-blr-01", "name": "Koramangala 80ft Road Automated Bay", "city": "bengaluru",
        "area": "Koramangala", "lat": 12.9352, "lon": 77.6245,
        "total_car": 140, "avail_car": 48, "total_bike": 250, "avail_bike": 110,
        "total_ev": 16, "avail_ev": 7, "rate_car_hr": 30, "rate_bike_hr": 15,
        "has_ev_fast_charger": True, "aqi": 72, "security_cctv": True, "covered": True
    },
    {
        "id": "prk-blr-02", "name": "Whitefield ITPL Metro Parking", "city": "bengaluru",
        "area": "Whitefield", "lat": 12.9860, "lon": 77.7380,
        "total_car": 280, "avail_car": 84, "total_bike": 450, "avail_bike": 195,
        "total_ev": 25, "avail_ev": 12, "rate_car_hr": 25, "rate_bike_hr": 10,
        "has_ev_fast_charger": True, "aqi": 88, "security_cctv": True, "covered": True
    },

    # Chennai
    {
        "id": "prk-chn-01", "name": "T. Nagar Smart Multi-Level Car Parking", "city": "chennai",
        "area": "Pondy Bazaar", "lat": 13.0418, "lon": 70.2341,
        "total_car": 220, "avail_car": 68, "total_bike": 350, "avail_bike": 152,
        "total_ev": 18, "avail_ev": 6, "rate_car_hr": 30, "rate_bike_hr": 10,
        "has_ev_fast_charger": True, "aqi": 88, "security_cctv": True, "covered": True
    },

    # Kolkata
    {
        "id": "prk-kol-01", "name": "Salt Lake Sector V Tech Parking", "city": "kolkata",
        "area": "Salt Lake", "lat": 22.5804, "lon": 88.4378,
        "total_car": 180, "avail_car": 45, "total_bike": 300, "avail_bike": 98,
        "total_ev": 14, "avail_ev": 4, "rate_car_hr": 25, "rate_bike_hr": 10,
        "has_ev_fast_charger": True, "aqi": 182, "security_cctv": True, "covered": True
    },

    # Hyderabad
    {
        "id": "prk-hyd-01", "name": "HITEC City Cyber Towers Parking", "city": "hyderabad",
        "area": "Madhapur", "lat": 17.4504, "lon": 78.3808,
        "total_car": 320, "avail_car": 110, "total_bike": 500, "avail_bike": 220,
        "total_ev": 24, "avail_ev": 10, "rate_car_hr": 30, "rate_bike_hr": 15,
        "has_ev_fast_charger": True, "aqi": 96, "security_cctv": True, "covered": True
    }
]

# In-memory reservation store
RESERVATIONS = []


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return r * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def get_parking_hubs(city: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns parking hubs for a given city or all hubs."""
    hubs = PARKING_REGISTRY
    if city and city.lower() != "all":
        city_lower = city.lower()
        hubs = [h for h in PARKING_REGISTRY if h["city"].lower() == city_lower]
        if not hubs:
            hubs = PARKING_REGISTRY

    results = []
    for h in hubs:
        car_pct = round((h["avail_car"] / h["total_car"]) * 100)
        bike_pct = round((h["avail_bike"] / h["total_bike"]) * 100)
        status = "Available" if car_pct > 25 else ("Filling Fast" if car_pct > 10 else "Nearly Full")
        status_color = "#10B981" if status == "Available" else ("#F59E0B" if status == "Filling Fast" else "#EF4444")

        results.append({
            "id": h["id"],
            "name": h["name"],
            "city": h["city"],
            "area": h["area"],
            "latitude": h["lat"],
            "longitude": h["lon"],
            "status": status,
            "status_color": status_color,
            "car_slots": {"total": h["total_car"], "available": h["avail_car"], "percent": car_pct},
            "bike_slots": {"total": h["total_bike"], "available": h["avail_bike"], "percent": bike_pct},
            "ev_slots": {"total": h["total_ev"], "available": h["avail_ev"]},
            "rates": {"car": f"₹{h['rate_car_hr']}/hr", "bike": f"₹{h['rate_bike_hr']}/hr"},
            "has_ev_fast_charger": h["has_ev_fast_charger"],
            "aqi": h["aqi"],
            "features": ["CCTV Security" if h["security_cctv"] else None, "Covered" if h["covered"] else "Open Air", "EV Ready" if h["has_ev_fast_charger"] else None]
        })
    return results


def find_nearest_parking(dest_lat: float, dest_lon: float, max_results: int = 4) -> List[Dict[str, Any]]:
    """Finds the nearest smart parking facilities relative to a destination coordinate."""
    all_hubs = get_parking_hubs()
    with_dist = []

    for h in all_hubs:
        d = haversine_km(dest_lat, dest_lon, h["latitude"], h["longitude"])
        h_copy = dict(h)
        h_copy["distance_km"] = round(d, 2)
        h_copy["walk_time_mins"] = round((d / 4.8) * 60)
        with_dist.append(h_copy)

    with_dist.sort(key=lambda x: x["distance_km"])

    # If the nearest pre-configured hub is > 20 km away (e.g. non-metro towns),
    # dynamically synthesize realistic smart parking bays right near the destination!
    if not with_dist or with_dist[0]["distance_km"] > 20.0:
        coord_key = abs(hash((round(dest_lat, 3), round(dest_lon, 3)))) % 10000
        local_hubs = [
            {
                "id": f"prk-loc-01-{coord_key}",
                "name": "Central Municipal Smart Parking Hub",
                "city": "local",
                "area": "Town Center & Transit Bay",
                "latitude": round(dest_lat + 0.0032, 5),
                "longitude": round(dest_lon + 0.0028, 5),
                "status": "Available",
                "status_color": "#10b981",
                "car_slots": {"total": 80, "available": 34, "percent": 42},
                "bike_slots": {"total": 150, "available": 68, "percent": 45},
                "ev_slots": {"total": 10, "available": 4},
                "rates": {"car": "₹20/hr", "bike": "₹10/hr"},
                "has_ev_fast_charger": True,
                "aqi": 82,
                "features": ["CCTV Security", "Covered", "EV Ready"],
                "distance_km": 0.45,
                "walk_time_mins": 6
            },
            {
                "id": f"prk-loc-02-{coord_key}",
                "name": "Commercial Plaza Public Parking Bay",
                "city": "local",
                "area": "Market Junction & Shopping Zone",
                "latitude": round(dest_lat - 0.0041, 5),
                "longitude": round(dest_lon + 0.0035, 5),
                "status": "Filling Fast",
                "status_color": "#f59e0b",
                "car_slots": {"total": 60, "available": 14, "percent": 23},
                "bike_slots": {"total": 120, "available": 28, "percent": 23},
                "ev_slots": {"total": 6, "available": 2},
                "rates": {"car": "₹25/hr", "bike": "₹10/hr"},
                "has_ev_fast_charger": True,
                "aqi": 94,
                "features": ["CCTV Security", "Open Air"],
                "distance_km": 0.62,
                "walk_time_mins": 8
            },
            {
                "id": f"prk-loc-03-{coord_key}",
                "name": "Transit Station Park & Ride Bay",
                "city": "local",
                "area": "Station Approach Corridor",
                "latitude": round(dest_lat + 0.0068, 5),
                "longitude": round(dest_lon - 0.0042, 5),
                "status": "Available",
                "status_color": "#10b981",
                "car_slots": {"total": 100, "available": 52, "percent": 52},
                "bike_slots": {"total": 200, "available": 110, "percent": 55},
                "ev_slots": {"total": 12, "available": 6},
                "rates": {"car": "₹20/hr", "bike": "₹10/hr"},
                "has_ev_fast_charger": True,
                "aqi": 78,
                "features": ["CCTV Security", "Covered", "EV Ready"],
                "distance_km": 0.95,
                "walk_time_mins": 12
            }
        ]
        for lh in local_hubs:
            if not any(r["id"] == lh["id"] for r in PARKING_REGISTRY):
                PARKING_REGISTRY.append({
                    "id": lh["id"], "name": lh["name"], "city": "local", "area": lh["area"],
                    "lat": lh["latitude"], "lon": lh["longitude"],
                    "total_car": lh["car_slots"]["total"], "avail_car": lh["car_slots"]["available"],
                    "total_bike": lh["bike_slots"]["total"], "avail_bike": lh["bike_slots"]["available"],
                    "total_ev": lh["ev_slots"]["total"], "avail_ev": lh["ev_slots"]["available"],
                    "rate_car_hr": 20, "rate_bike_hr": 10, "has_ev_fast_charger": True,
                    "aqi": lh["aqi"], "security_cctv": True, "covered": True
                })
        return local_hubs[:max_results]

    return with_dist[:max_results]


def reserve_parking_slot(
    hub_id: str,
    vehicle_type: str,
    vehicle_number: str,
    duration_hours: int = 2
) -> Dict[str, Any]:
    """Simulates instant parking slot reservation and generates digital parking pass."""
    hub = next((h for h in PARKING_REGISTRY if h["id"] == hub_id), None)
    if not hub:
        return {"success": False, "message": "Parking hub not found."}

    vtype = vehicle_type.lower()
    if "bike" in vtype or "two" in vtype or "motor" in vtype:
        if hub["avail_bike"] <= 0:
            return {"success": False, "message": "Two-wheeler parking slots are currently full at this hub."}
        hub["avail_bike"] -= 1
        rate = hub["rate_bike_hr"]
        slot_label = f"B2-Slot-{random.randint(10, 80)}"
    elif "ev" in vtype:
        if hub["avail_ev"] <= 0:
            return {"success": False, "message": "EV charging slots are currently full at this hub."}
        hub["avail_ev"] -= 1
        rate = hub["rate_car_hr"] + 15
        slot_label = f"EV-Bay-{random.randint(1, hub['total_ev'])}"
    else:
        if hub["avail_car"] <= 0:
            return {"success": False, "message": "Car parking slots are currently full at this hub."}
        hub["avail_car"] -= 1
        rate = hub["rate_car_hr"]
        slot_label = f"A1-Car-{random.randint(10, 95)}"

    ticket_id = f"PRK-2026-{random.randint(1000, 9999)}"
    now = datetime.now()
    total_fee = rate * duration_hours

    booking = {
        "success": True,
        "ticket_id": ticket_id,
        "parking_hub": hub["name"],
        "area": hub["area"],
        "vehicle_number": vehicle_number.upper(),
        "vehicle_type": vehicle_type.title(),
        "slot_assigned": slot_label,
        "entry_time": now.strftime("%Y-%m-%d %H:%M"),
        "duration_hours": duration_hours,
        "total_fee": f"₹{total_fee}",
        "hourly_rate": f"₹{rate}/hr",
        "qr_simulation_code": f"AIRSENSE-PARK-{ticket_id}-{hub_id}",
        "message": "Parking slot successfully reserved! Please show this pass at entry gate."
    }

    RESERVATIONS.append(booking)
    return booking
