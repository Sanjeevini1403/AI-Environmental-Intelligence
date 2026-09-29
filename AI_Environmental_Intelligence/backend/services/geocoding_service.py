"""
Geocoding service with Instant Local Place Registry & OpenStreetMap Nominatim fallback.

Supports rapid typeahead autocomplete for Indian cities, metros, and localities
without rate limits or query delays.
"""

import requests
from typing import List, Dict, Any, Optional
from backend.pune_bounds import KNOWN_PLACES, SUPPORTED_CITIES, is_valid_location

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {
    "User-Agent": "AI-Environmental-Intelligence-System/2.5"
}


def geocode_location(query: str) -> Optional[Dict[str, Any]]:
    """Geocodes a query into coordinates, prioritizing instant local places then Nominatim."""
    q_clean = query.strip().lower()
    if not q_clean:
        return None

    # 1. Exact or prefix match in KNOWN_PLACES
    for p in KNOWN_PLACES:
        p_name = p["name"].lower()
        p_city = p["city"].lower()
        if q_clean == p_name or q_clean == p_city or q_clean in p["display_name"].lower():
            return {
                "query": query,
                "display_name": p["display_name"],
                "latitude": p["lat"],
                "longitude": p["lon"]
            }

    # 2. Check SUPPORTED_CITIES
    for key, city in SUPPORTED_CITIES.items():
        if q_clean == key or q_clean in city["name"].lower():
            return {
                "query": query,
                "display_name": f"{city['name']}, {city['state']}, India",
                "latitude": city["center"]["latitude"],
                "longitude": city["center"]["longitude"]
            }

    # 3. Fallback to OpenStreetMap Nominatim
    results = _search_nominatim(query, limit=1)
    if results:
        place = results[0]
        return {
            "query": query,
            "display_name": place["display_name"],
            "latitude": place["latitude"],
            "longitude": place["longitude"]
        }

    return None


def geocode_suggestions(query: str, limit: int = 6) -> List[Dict[str, Any]]:
    """
    Returns real-time suggestions as the user types any city, area, or street.
    Prioritizes local known places first, followed by live Nominatim geocoding.
    """
    q_clean = query.strip().lower()
    if len(q_clean) < 1:
        return []

    results = []
    seen = set()

    # 1. Search in KNOWN_PLACES (Local Match - Instant 0ms)
    # First priority: starts with query
    for p in KNOWN_PLACES:
        p_name = p["name"].lower()
        p_city = p["city"].lower()
        if p_name.startswith(q_clean) or p_city.startswith(q_clean):
            key = f"{round(p['lat'], 4)},{round(p['lon'], 4)}"
            if key not in seen:
                seen.add(key)
                results.append({
                    "display_name": p["display_name"],
                    "latitude": p["lat"],
                    "longitude": p["lon"],
                    "source": "local"
                })
                if len(results) >= limit:
                    return results

    # Second priority: contains query anywhere
    for p in KNOWN_PLACES:
        p_name = p["name"].lower()
        p_city = p["city"].lower()
        p_disp = p["display_name"].lower()
        if (q_clean in p_name or q_clean in p_city or q_clean in p_disp):
            key = f"{round(p['lat'], 4)},{round(p['lon'], 4)}"
            if key not in seen:
                seen.add(key)
                results.append({
                    "display_name": p["display_name"],
                    "latitude": p["lat"],
                    "longitude": p["lon"],
                    "source": "local"
                })
                if len(results) >= limit:
                    return results

    # 2. If we already have 3 or more high-quality local matches, return them immediately
    if len(results) >= 3:
        return results[:limit]

    # 3. Augment with Nominatim for rare/specific street names
    if len(q_clean) >= 3:
        nominatim_res = _search_nominatim(query, limit=limit - len(results))
        for nr in nominatim_res:
            key = f"{round(nr['latitude'], 4)},{round(nr['longitude'], 4)}"
            if key not in seen:
                seen.add(key)
                results.append(nr)
                if len(results) >= limit:
                    break

    return results


def _search_nominatim(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    params = {
        "q": query,
        "format": "json",
        "limit": limit,
        "countrycodes": "in",
        "addressdetails": 1
    }

    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=3.0)
        if response.status_code != 200:
            return []
        data = response.json()
    except Exception:
        return []

    results = []
    for place in data:
        try:
            lat = float(place["lat"])
            lon = float(place["lon"])
            if is_valid_location(lat, lon):
                results.append({
                    "display_name": place.get("display_name", query),
                    "latitude": lat,
                    "longitude": lon,
                    "source": "osm"
                })
        except (ValueError, KeyError):
            continue

    return results
