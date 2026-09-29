"""
Direct Unit & Services Verification Script (Windows compatible encoding).
"""

import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.services.stations_service import get_all_stations, get_network_kpi_summary
from backend.services.interpolation_service import estimate_aqi_idw, generate_spatial_aqi_grid
from backend.services.traffic_service import get_current_traffic_factor, evaluate_route_traffic, get_city_traffic_hotspots
from backend.services.chatbot_service import get_chatbot_response
from backend.services.prediction_service import predict_aqi
from backend.services.mobility_service import get_mobility_recommendation
from backend.services.exposure_service import save_trip_exposure, get_trip_history, get_daily_exposure_summary
from backend.pune_bounds import SUPPORTED_CITIES, is_valid_location

def test_services():
    print("=" * 60)
    print("Testing Environmental Intelligence Core Services...")
    print("=" * 60)

    # 1. Prediction Service
    pred = predict_aqi(pm25=55, pm10=110, no2=45, so2=18, co=500, o3=60)
    assert "predicted_aqi" in pred and "category" in pred
    print(f"[OK] Prediction Service: AQI = {pred['predicted_aqi']} ({pred['category']})")

    # 2. Regional Bounds & Cities
    assert len(SUPPORTED_CITIES) >= 7
    assert is_valid_location(18.5204, 73.8567) is True
    print(f"[OK] Regional Support: {len(SUPPORTED_CITIES)} metropolitan regions configured.")

    # 3. Monitoring Stations & KPI Summary
    stations = get_all_stations("pune")
    assert len(stations) >= 5
    kpis = get_network_kpi_summary("pune")
    assert kpis["stations_active"] > 0
    print(f"[OK] Stations & KPIs: Active = {kpis['stations_active']}, Accuracy = {kpis['forecast_accuracy']}")

    # 4. Spatial Interpolation (IDW)
    idw_res = estimate_aqi_idw(18.5204, 73.8567)
    assert "estimated_aqi" in idw_res
    print(f"[OK] Spatial Interpolation (IDW): Estimated AQI = {idw_res['estimated_aqi']} (Confidence: {idw_res['confidence_percent']})")

    grid = generate_spatial_aqi_grid(18.5204, 73.8567, radius_km=10, steps=3)
    assert len(grid) == 9
    print(f"[OK] Spatial Interpolation Grid: Generated {len(grid)} continuous interpolation coordinates.")

    # 5. Traffic Congestion Modeling
    traffic = get_current_traffic_factor()
    assert "congestion_level" in traffic
    hotspots = get_city_traffic_hotspots(18.5204, 73.8567)
    assert len(hotspots) > 0
    sample_path = [{"lat": 18.52, "lng": 73.85}, {"lat": 18.53, "lng": 73.86}, {"lat": 18.54, "lng": 73.87}]
    route_traffic = evaluate_route_traffic(sample_path, base_duration_sec=900)
    assert len(route_traffic["traffic_segments"]) > 0
    print(f"[OK] Traffic Service: Status = {traffic['congestion_level']}, Segments = {len(route_traffic['traffic_segments'])}, Hotspots = {len(hotspots)}")

    # 6. Personalized Mobility & Health Profiles
    mob_asthma = get_mobility_recommendation("Moderate", temperature=31, aqi_value=120, health_profile="asthmatic")
    assert mob_asthma["threshold_breached"] is True
    assert mob_asthma["mask_required"] is True
    print(f"[OK] Health Profile Service (Asthma): Mask Required = {mob_asthma['mask_required']}, Breached = {mob_asthma['threshold_breached']}")

    # 7. AI Environmental Chatbot (English & Tanglish)
    bot_eng = get_chatbot_response("Should I wear an N95 mask today?", context={"aqi": 160, "category": "Moderate"})
    assert "mask" in bot_eng["reply"].lower()

    bot_tanglish = get_chatbot_response("Enaku asthma iruku, ipo veliya polama?", context={"aqi": 130, "category": "Moderate"})
    assert "asthma" in bot_tanglish["reply"].lower()
    print("[OK] AI Chatbot Service: Responded correctly in English & Tanglish.")

    # 8. Exposure SQLite Database & Tracking
    save_trip_exposure(
        origin="Kothrud", destination="Hinjewadi", route_type="Cleanest",
        distance_km=14.2, duration_mins=28, avg_aqi=95, cumulative_exposure=44.3,
        aqi_category="Moderate", health_profile="normal"
    )
    hist = get_trip_history(limit=5)
    assert len(hist) > 0
    summary = get_daily_exposure_summary()
    assert "cumulative_aqi_exposure" in summary
    print(f"[OK] Personal Exposure Store: {len(hist)} trips logged, Today's Dosage = {summary['cumulative_aqi_exposure']} AQI·hr")

    print("\n" + "=" * 60)
    print("ALL 8 CORE SERVICES VALIDATED AND FULLY OPERATIONAL!")
    print("=" * 60)

if __name__ == "__main__":
    test_services()
