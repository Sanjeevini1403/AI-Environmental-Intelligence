import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_endpoints():
    print("Testing backend endpoints...")

    # 1. Status
    res = client.get("/api/status")
    assert res.status_code == 200, f"Status failed: {res.text}"
    print("[OK] /api/status OK:", res.json()["system"])

    # 2. Cities
    res = client.get("/api/cities")
    assert res.status_code == 200
    cities = res.json()["cities"]
    assert "pune" in cities and "delhi" in cities
    print(f"[OK] /api/cities OK ({len(cities)} cities supported)")

    # 3. KPI Summary
    res = client.get("/api/kpi-summary?city=pune")
    assert res.status_code == 200
    kpis = res.json()["kpis"]
    assert "stations_active" in kpis and "forecast_accuracy" in kpis
    print(f"[OK] /api/kpi-summary OK (Active: {kpis['stations_active']}, Accuracy: {kpis['forecast_accuracy']})")

    # 4. Stations List
    res = client.get("/api/stations?city=pune")
    assert res.status_code == 200
    stations = res.json()["stations"]
    assert len(stations) > 0
    print(f"[OK] /api/stations OK ({len(stations)} stations loaded)")

    # 5. Spatial Interpolation (IDW)
    res = client.get("/api/interpolation?latitude=18.5204&longitude=73.8567&generate_grid=true")
    assert res.status_code == 200
    interp = res.json()
    assert "point_estimate" in interp and "grid" in interp
    print("[OK] /api/interpolation (IDW) OK: Estimated AQI =", interp["point_estimate"]["estimated_aqi"])

    # 6. Traffic Hotspots
    res = client.get("/api/traffic?latitude=18.5204&longitude=73.8567")
    assert res.status_code == 200
    traffic = res.json()
    assert "current_traffic" in traffic and "hotspots" in traffic
    print("[OK] /api/traffic OK: Period =", traffic["current_traffic"]["period"])

    # 7. Environment (Fused sensor + ML prediction + mobility)
    res = client.get("/environment?latitude=18.5204&longitude=73.8567&health_profile=asthmatic")
    assert res.status_code == 200
    env = res.json()
    assert env["success"] is True
    print(f"[OK] /environment OK: Predicted AQI = {env['aqi_prediction']['predicted_aqi']} ({env['aqi_prediction']['category']})")

    # 8. Forecast (24 Hours)
    res = client.get("/forecast?latitude=18.5204&longitude=73.8567&hours=24")
    assert res.status_code == 200
    fc = res.json()
    assert len(fc["hourly_forecast"]) > 0
    print(f"[OK] /forecast OK ({len(fc['hourly_forecast'])} hourly predictions)")

    # 9. AI Chatbot
    res = client.post("/api/chatbot", json={
        "message": "Enaku asthma iruku, ipo veliya polama?",
        "context": {"aqi": 140, "category": "Moderate", "profile": "asthmatic"}
    })
    assert res.status_code == 200
    bot_res = res.json()
    assert "reply" in bot_res["response"]
    print("[OK] /api/chatbot (Tanglish / Asthma) OK. Sample reply:\n", bot_res["response"]["reply"][:120], "...")

    # 10. Exposure History
    res = client.get("/api/exposure/summary")
    assert res.status_code == 200
    print("[OK] /api/exposure/summary OK:", res.json()["summary"])

    # 11. Geocode Suggestions (Typeahead for any city)
    res = client.get("/geocode-suggestions?q=chennai")
    assert res.status_code == 200
    places = res.json()["results"]
    assert len(places) > 0
    print(f"[OK] /geocode-suggestions OK ({len(places)} results for 'chennai')")

    # 12. Smart Route Advisory (Fast & Resilient)
    res = client.get("/route?origin_lat=18.5074&origin_lon=73.8077&dest_lat=18.5913&dest_lon=73.7389&mode=driving")
    assert res.status_code == 200
    routes = res.json()["routes"]
    assert len(routes) > 0
    print(f"[OK] /route OK ({len(routes)} routes generated, Cleanest/Fastest/Balanced)")

    print("\n[SUCCESS] ALL BACKEND TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_endpoints()
