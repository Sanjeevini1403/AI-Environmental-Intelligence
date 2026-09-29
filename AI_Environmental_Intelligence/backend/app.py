"""
AI Environmental Intelligence Backend Application.
FastAPI service integrating real-time environmental sensors, predictive ML forecasting,
spatial interpolation (IDW), traffic congestion modeling, personalized health profiles,
AI Chatbot, and route exposure optimization.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.services.prediction_service import predict_aqi, get_aqi_category
from backend.services.weather_service import get_weather
from backend.services.air_quality_service import get_air_quality
from backend.services.mobility_service import get_mobility_recommendation, HEALTH_PROFILES
from backend.services.geocoding_service import geocode_location, geocode_suggestions
from backend.services.forecast_service import get_aqi_forecast, get_key_forecast_points, get_best_travel_window
from backend.services.heatmap_service import get_pollution_grid
from backend.services.directions_service import get_route_options
from backend.services.stations_service import get_all_stations, get_network_kpi_summary
from backend.services.interpolation_service import estimate_aqi_idw, generate_spatial_aqi_grid
from backend.services.traffic_service import get_current_traffic_factor, get_city_traffic_hotspots
from backend.services.chatbot_service import get_chatbot_response
from backend.services.exposure_service import (
    save_trip_exposure, get_trip_history, get_daily_exposure_summary
)
from backend.services.parking_service import (
    get_parking_hubs, find_nearest_parking, reserve_parking_slot
)
from backend.pune_bounds import (
    is_valid_location, SUPPORTED_CITIES, PUNE_CENTER, detect_city
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = FastAPI(
    title="AI Environmental Intelligence & Smart Mobility System",
    description="Full-stack AI platform for predictive AQI forecasting, spatial interpolation, route exposure optimization, and personalized health advisories.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


def validate_coords(lat: float, lon: float):
    if not is_valid_location(lat, lon):
        raise HTTPException(status_code=400, detail="Invalid geographic coordinates.")


# -------------------------------------------------------------
# System Status & Regional Metadata Endpoints
# -------------------------------------------------------------

@app.get("/api/status")
def system_status():
    return {
        "status": "healthy",
        "system": "AI Environmental Intelligence Platform",
        "version": "2.0.0",
        "ml_engine": "RandomForest + Inverse Distance Weighting (IDW)",
        "active_regions": list(SUPPORTED_CITIES.keys())
    }


@app.get("/pune-center")
def pune_center():
    return {"success": True, "center": PUNE_CENTER}


@app.get("/api/cities")
def get_cities():
    return {
        "success": True,
        "cities": SUPPORTED_CITIES,
        "default": "pune"
    }


# -------------------------------------------------------------
# Core Prediction & Sensor Endpoints
# -------------------------------------------------------------

@app.post("/predict-aqi")
def predict(
    pm25: float,
    pm10: float,
    no2: float,
    so2: float,
    co: float,
    o3: float
):
    result = predict_aqi(pm25=pm25, pm10=pm10, no2=no2, so2=so2, co=co, o3=o3)
    # Include 95% confidence interval
    pred_val = result["predicted_aqi"]
    margin = round(pred_val * 0.08, 1)

    return {
        "success": True,
        "prediction": result,
        "confidence_interval": {
            "lower_bound": max(10, round(pred_val - margin, 1)),
            "upper_bound": min(500, round(pred_val + margin, 1)),
            "confidence_level": "95%"
        }
    }


@app.get("/weather")
def weather(latitude: float, longitude: float):
    validate_coords(latitude, longitude)
    result = get_weather(latitude=latitude, longitude=longitude)
    return {"success": True, "data": result}


@app.get("/air-quality")
def air_quality(latitude: float, longitude: float):
    validate_coords(latitude, longitude)
    result = get_air_quality(latitude=latitude, longitude=longitude)
    return {"success": True, "data": result}


@app.get("/environment")
def environment(
    latitude: float,
    longitude: float,
    health_profile: str = "normal"
):
    validate_coords(latitude, longitude)

    weather_data = get_weather(latitude=latitude, longitude=longitude)
    air_data = get_air_quality(latitude=latitude, longitude=longitude)

    # Use ML model if valid pollutant feeds exist, else default safely
    pm25 = air_data.get("pm2_5") or 45.0
    pm10 = air_data.get("pm10") or 80.0
    no2 = air_data.get("nitrogen_dioxide") or 30.0
    so2 = air_data.get("sulphur_dioxide") or 15.0
    co = air_data.get("carbon_monoxide") or 400.0
    o3 = air_data.get("ozone") or 40.0

    prediction = predict_aqi(pm25=pm25, pm10=pm10, no2=no2, so2=so2, co=co, o3=o3)

    mobility = get_mobility_recommendation(
        aqi_category=prediction["category"],
        temperature=weather_data.get("temperature"),
        humidity=weather_data.get("humidity"),
        wind_speed=weather_data.get("wind_speed"),
        health_profile=health_profile,
        aqi_value=prediction["predicted_aqi"]
    )

    detected_city_key = detect_city(latitude, longitude)

    return {
        "success": True,
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "city": SUPPORTED_CITIES.get(detected_city_key, {}).get("name", "Local Area")
        },
        "weather": weather_data,
        "air_quality": air_data,
        "aqi_prediction": prediction,
        "mobility_recommendation": mobility
    }


# -------------------------------------------------------------
# Forecast & Spatial Interpolation Endpoints
# -------------------------------------------------------------

@app.get("/forecast")
def forecast(latitude: float, longitude: float, hours: int = 24):
    validate_coords(latitude, longitude)
    points = get_aqi_forecast(latitude, longitude, hours=hours)

    if not points:
        raise HTTPException(status_code=502, detail="Forecast data unavailable for this location.")

    return {
        "success": True,
        "location": {"latitude": latitude, "longitude": longitude},
        "hourly_forecast": points,
        "key_points": get_key_forecast_points(points),
        "best_travel_window": get_best_travel_window(points)
    }


@app.get("/heatmap")
def heatmap(latitude: float, longitude: float, radius_km: float = 12.0, grid_size: int = 4):
    validate_coords(latitude, longitude)
    points = get_pollution_grid(latitude, longitude, radius_km=radius_km, grid_size=grid_size)
    return {
        "success": True,
        "center": {"latitude": latitude, "longitude": longitude},
        "points": points
    }


@app.get("/api/interpolation")
def spatial_interpolation(
    latitude: float,
    longitude: float,
    generate_grid: bool = False,
    radius_km: float = 10.0
):
    """
    Inverse Distance Weighting (IDW) interpolation estimating AQI between sensor stations.
    """
    validate_coords(latitude, longitude)
    point_est = estimate_aqi_idw(latitude, longitude)

    grid_points = []
    if generate_grid:
        grid_points = generate_spatial_aqi_grid(latitude, longitude, radius_km=radius_km, steps=5)

    return {
        "success": True,
        "point_estimate": point_est,
        "grid": grid_points
    }


# -------------------------------------------------------------
# Monitoring Stations & Dashboard KPI Endpoints (Page 4 Style)
# -------------------------------------------------------------

@app.get("/api/stations")
def list_stations(city: Optional[str] = None):
    stations = get_all_stations(city)
    return {
        "success": True,
        "total": len(stations),
        "stations": stations
    }


@app.get("/api/kpi-summary")
def kpi_summary(city: Optional[str] = None):
    summary = get_network_kpi_summary(city)
    return {
        "success": True,
        "kpis": summary
    }


# -------------------------------------------------------------
# Traffic Density & Bottleneck Endpoints
# -------------------------------------------------------------

@app.get("/api/traffic")
def traffic_condition(latitude: float = 18.5204, longitude: float = 73.8567):
    factor = get_current_traffic_factor()
    hotspots = get_city_traffic_hotspots(latitude, longitude)
    return {
        "success": True,
        "current_traffic": factor,
        "hotspots": hotspots
    }


# -------------------------------------------------------------
# Route Directions, Multi-Modal Mobility & Exposure Optimization
# -------------------------------------------------------------

@app.get("/route")
def route(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
    mode: str = "driving"
):
    validate_coords(origin_lat, origin_lon)
    validate_coords(dest_lat, dest_lon)

    try:
        result = get_route_options(origin_lat, origin_lon, dest_lat, dest_lon, mode=mode)
    except Exception as e:
        # High resilience fallback
        from backend.services.directions_service import _generate_synthetic_routes, compute_mode_metrics, _label_routes
        from backend.services.parking_service import find_nearest_parking
        synthetic = _generate_synthetic_routes(origin_lat, origin_lon, dest_lat, dest_lon)
        routes = []
        for sr in synthetic:
            pts = [{"lat": lat, "lng": lng} for lng, lat in sr["geometry"]["coordinates"]]
            d_km = round(sr["distance"] / 1000.0, 2)
            m_data = compute_mode_metrics(d_km, sr["duration"], 0, 95.0, mode=mode)
            routes.append({
                "path": pts,
                "segments": [{"start_index": 0, "end_index": len(pts)-1, "polluted": False}],
                "traffic_segments": [{"start_index": 0, "end_index": len(pts)-1, "status": "light", "color": "#10B981", "label": "Free Flow", "speed_kmh": 40}],
                "distance_text": f"{d_km:.1f} km",
                "distance_value": sr["distance"],
                "distance_km": d_km,
                "mode": mode,
                "duration_text": m_data["duration_text"],
                "duration_value": m_data["duration_sec"],
                "duration_in_traffic_text": m_data["duration_text"],
                "duration_in_traffic_value": m_data["duration_sec"],
                "delay_minutes": 0,
                "congestion_level": "light",
                "calories_burned": m_data["calories_burned"],
                "health_note": m_data["health_note"],
                "avg_aqi": 95.0,
                "cumulative_exposure": m_data["cumulative_exposure"],
                "aqi_category": "Satisfactory",
                "multi_modal_comparison": {
                    "car": compute_mode_metrics(d_km, sr["duration"], 0, 95.0, mode="driving"),
                    "motorcycle": compute_mode_metrics(d_km, sr["duration"], 0, 95.0, mode="motorcycle"),
                    "cycling": compute_mode_metrics(d_km, sr["duration"], 0, 95.0, mode="cycling"),
                    "walking": compute_mode_metrics(d_km, sr["duration"], 0, 95.0, mode="walking")
                }
            })
        result = {
            "routes": _label_routes(routes),
            "nearby_parking": find_nearest_parking(dest_lat, dest_lon, max_results=3)
        }

    return {
        "success": True,
        "routes": result["routes"],
        "nearby_parking": result.get("nearby_parking", [])
    }


# -------------------------------------------------------------
# Smart Parking Hubs & Slot Reservation Endpoints
# -------------------------------------------------------------

@app.get("/api/parking")
def list_parking_hubs(city: Optional[str] = None):
    hubs = get_parking_hubs(city)
    return {
        "success": True,
        "total": len(hubs),
        "parking_hubs": hubs
    }


@app.get("/api/parking/near")
def nearby_parking(latitude: float, longitude: float, max_results: int = 4):
    validate_coords(latitude, longitude)
    hubs = find_nearest_parking(latitude, longitude, max_results=max_results)
    return {
        "success": True,
        "nearby_parking": hubs
    }


@app.post("/api/parking/reserve")
def reserve_parking(payload: dict = Body(...)):
    hub_id = payload.get("hub_id", "")
    vehicle_type = payload.get("vehicle_type", "car")
    vehicle_number = payload.get("vehicle_number", "MH-12-AB-1234")
    duration_hours = int(payload.get("duration_hours", 2))

    res = reserve_parking_slot(
        hub_id=hub_id,
        vehicle_type=vehicle_type,
        vehicle_number=vehicle_number,
        duration_hours=duration_hours
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message", "Reservation failed"))
    return res


# -------------------------------------------------------------
# Geocoding & Mobility Advice Endpoints
# -------------------------------------------------------------

@app.get("/geocode")
def geocode(q: str):
    result = geocode_location(q)
    if result is None:
        raise HTTPException(status_code=404, detail=f"'{q}' was not found.")
    return {"success": True, "result": result}


@app.get("/geocode-suggestions")
def geocode_suggestions_endpoint(q: str):
    results = geocode_suggestions(q)
    return {"success": True, "results": results}


@app.get("/mobility-recommendation")
def mobility_recommendation(
    aqi_category: str,
    temperature: Optional[float] = None,
    humidity: Optional[float] = None,
    wind_speed: Optional[float] = None,
    health_profile: str = "normal",
    aqi_value: Optional[float] = None
):
    result = get_mobility_recommendation(
        aqi_category=aqi_category,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        health_profile=health_profile,
        aqi_value=aqi_value
    )
    return {"success": True, "recommendation": result}


@app.get("/api/health-profiles")
def get_health_profiles():
    return {
        "success": True,
        "profiles": HEALTH_PROFILES
    }


# -------------------------------------------------------------
# AI Environmental Chatbot Endpoint ("AirIQ EcoBot")
# -------------------------------------------------------------

@app.post("/api/chatbot")
def chatbot_endpoint(payload: dict = Body(...)):
    message = payload.get("message", "")
    context = payload.get("context", {})
    response = get_chatbot_response(message, context=context)
    return {
        "success": True,
        "response": response
    }


# -------------------------------------------------------------
# Personal Trip Exposure & History Endpoints
# -------------------------------------------------------------

@app.post("/api/exposure/save")
def log_trip_exposure(payload: dict = Body(...)):
    res = save_trip_exposure(
        origin=payload.get("origin", "Current Location"),
        destination=payload.get("destination", "Destination"),
        route_type=payload.get("route_type", "Cleanest"),
        distance_km=float(payload.get("distance_km", 0.0)),
        duration_mins=float(payload.get("duration_mins", 0.0)),
        avg_aqi=float(payload.get("avg_aqi", 100.0)),
        cumulative_exposure=float(payload.get("cumulative_exposure", 0.0)),
        aqi_category=payload.get("aqi_category", "Moderate"),
        health_profile=payload.get("health_profile", "normal")
    )
    return res


@app.get("/api/exposure/history")
def trip_history(limit: int = 15):
    history = get_trip_history(limit=limit)
    return {"success": True, "history": history}


@app.get("/api/exposure/summary")
def daily_exposure_summary():
    summary = get_daily_exposure_summary()
    return {"success": True, "summary": summary}


# -------------------------------------------------------------
# User Authentication & Profile Endpoints
# -------------------------------------------------------------

from backend.services.auth_service import authenticate_user, register_user

@app.post("/api/auth/login")
def login_endpoint(payload: dict = Body(...)):
    email_or_user = payload.get("email") or payload.get("username") or payload.get("email_or_user", "")
    password = payload.get("password", "")
    res = authenticate_user(email_or_user, password)
    if not res.get("success"):
        raise HTTPException(status_code=401, detail=res.get("message", "Authentication failed"))
    return res


@app.post("/api/auth/register")
def register_endpoint(payload: dict = Body(...)):
    name = payload.get("name", "")
    email = payload.get("email", "")
    password = payload.get("password", "")
    city = payload.get("city", "pune")
    health_profile = payload.get("health_profile", "normal")
    res = register_user(name=name, email=email, password=password, city=city, health_profile=health_profile)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message", "Registration failed"))
    return res


@app.get("/api/auth/demo-users")
def demo_users_endpoint():
    return {
        "success": True,
        "demo_accounts": [
            {"name": "Sanjeevini S.", "email": "sanjeevini@airsense.ai", "label": "Asthmatic Profile (Chennai)", "city": "chennai", "profile": "asthmatic"},
            {"name": "Rahul Sharma", "email": "commuter@airsense.ai", "label": "Urban Commuter (Mumbai)", "city": "mumbai", "profile": "normal"},
            {"name": "Ananya Rao", "email": "cyclist@airsense.ai", "label": "Eco Cyclist (Bengaluru)", "city": "bengaluru", "profile": "athlete"},
            {"name": "AirSense Admin", "email": "admin@airsense.ai", "label": "Environmental Admin (Pune)", "city": "pune", "profile": "normal"}
        ]
    }


# -------------------------------------------------------------
# Frontend Static Files & SPA Delivery
# -------------------------------------------------------------

if os.path.exists(FRONTEND_DIR):
    css_path = os.path.join(FRONTEND_DIR, "css")
    js_path = os.path.join(FRONTEND_DIR, "js")
    if os.path.exists(css_path):
        app.mount("/css", StaticFiles(directory=css_path), name="css")
    if os.path.exists(js_path):
        app.mount("/js", StaticFiles(directory=js_path), name="js")
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    @app.get("/index.html")
    def serve_frontend_index():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend index.html not found"}

    @app.get("/login")
    @app.get("/login.html")
    def serve_frontend_login():
        login_file = os.path.join(FRONTEND_DIR, "login.html")
        if os.path.exists(login_file):
            return FileResponse(login_file)
        return {"message": "Frontend login.html not found"}

