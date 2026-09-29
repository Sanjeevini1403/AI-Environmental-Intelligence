# AI-Powered Environmental Intelligence System
### Air Quality Prediction & Smart Mobility Recommendations — Pune

A full-stack system that fetches live weather and air-quality data for Pune,
predicts the Air Quality Index (AQI) using a trained Machine Learning model,
recommends the safest mode of mobility, and suggests routes that avoid
high-pollution areas — all using entirely free, keyless services
(OpenStreetMap + OSRM), no paid API or billing account required.

**This project currently supports the Pune region only** (per project
guidance) — both the frontend map and the backend API reject
locations/routes outside Pune's bounding box.

---

## 1. Features

- **Live Weather Data** — temperature, humidity, wind speed (Open-Meteo API)
- **Live Air Quality Data** — PM2.5, PM10, NO2, SO2, CO, O3 (Open-Meteo Air Quality API)
- **AI AQI Prediction** — Random Forest Regressor trained on historical Pune
  environmental data, served through a FastAPI backend
- **Smart Mobility Recommendations** — rule-based engine that combines the
  predicted AQI category with live weather to suggest a travel mode, the
  best travel time window, and whether a mask is required
- **Interactive Map (Leaflet + OpenStreetMap, free)** — click anywhere in
  Pune to check that location, with a marker colour-coded by the live AQI
  category, a "Use my location" button, and a popup showing weather + AQI
  details. No API key or billing account needed.
- **Pollution Zone View** — toggleable colour-coded grid of nearby points
  (green→purple by AQI category) around the selected location, built by
  reusing the existing air-quality service + ML model over a small grid
- **AQI Forecast Dashboard** — next 1h / 3h / 6h / 24h predicted AQI plus a
  24-hour line chart, built by running the existing ML model over
  Open-Meteo's free hourly air-quality forecast
- **Best Time to Travel** — automatically finds the 2-hour window in the
  next 24 hours with the lowest predicted AQI
- **Smart Route Recommendation** — enter a start and destination in Pune;
  fetches alternative driving routes (distance + estimated travel time)
  from OSRM's free public routing service, then estimates pollution
  exposure along each route by sampling points on its path through the
  existing air-quality service + ML model. Labels routes **Fastest**,
  **Cleanest**, and **Balanced**, and recommends the best overall pick
  (see section 7 for the algorithm). No API key needed.
- **Pollution Alerts** — a banner appears when the current AQI is Moderate
  or worse, or when the forecast shows AQI worsening sharply in the next
  few hours
- **Search by Place Name** — type a spot in Pune (e.g. "Kothrud") and it's
  geocoded via the free OpenStreetMap Nominatim API, biased to Pune
- **Recent Locations** — the last 5 places you checked are saved in the
  browser (`localStorage`) as quick-access chips
- **Downloadable Report** — export the current reading as a JSON file

**Nothing in this project needs a paid API key, a Google Cloud account, or
a billing card.** Every external service used — Open-Meteo (weather + air
quality + forecast), OpenStreetMap Nominatim (search), and OSRM (routing)
— is free and keyless.

---

## 2. A note on routing — no live traffic data

OSRM's free public routing server gives route alternatives, distance, and
an *estimated* travel time based on road speed limits — it does **not**
have live traffic data (that's a paid-provider feature, e.g. Google
Directions API with a billing account). For a student project demo this
is a reasonable trade-off: you still get multiple real routes and a
genuine pollution-exposure comparison between them, just without
real-time congestion. The route cards say "(estimated, no live traffic
data)" so this is clear to anyone reviewing the project.

If a future requirement needs real-time traffic, that's the one piece
that would need a paid key — everything else in this project stays free
either way.

---

## 3. Project Structure

```
AI_Environmental_Intelligence/
├── backend/
│   ├── app.py                       # FastAPI app & routes (+ Pune bounds check)
│   ├── pune_bounds.py                # Pune bounding-box constants + check
│   ├── services/
│   │   ├── weather_service.py       # Open-Meteo weather fetch
│   │   ├── air_quality_service.py   # Open-Meteo air-quality fetch
│   │   ├── prediction_service.py    # Loads model, predicts AQI
│   │   ├── mobility_service.py      # Smart mobility recommendation logic
│   │   ├── geocoding_service.py     # Place name → lat/lon (OpenStreetMap, biased to Pune)
│   │   ├── forecast_service.py      # Hourly AQI forecast + best travel window (reuses the ML model)
│   │   ├── heatmap_service.py       # Pollution zone grid (reuses air-quality service + ML model)
│   │   ├── directions_service.py    # Free OSRM routing + route labelling (fastest/cleanest/balanced)
│   │   └── route_service.py         # Samples points along a route, reuses air-quality + ML model
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/script.js
├── models/
│   └── aqi_prediction_model.pkl     # Trained Random Forest model (Pune data)
├── data/                            # Raw → cleaned → feature-engineered datasets
├── src/                             # Data pipeline & model training scripts
├── requirements.txt
└── README.md
```

---

## 4. Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt
```

No API keys, `.env` file, or config file to set up — every external
service this project uses is free and keyless.

---

## 5. Running the Backend

Run this from the **project root** (the folder containing `backend/`),
so the `backend.*` imports resolve correctly:

```bash
uvicorn backend.app:app --reload
```

The API will start at `http://127.0.0.1:8000`.
Interactive API docs (Swagger UI) are auto-generated at
`http://127.0.0.1:8000/docs`.

---

## 6. Running the Frontend

Just open `frontend/index.html` directly in a browser (double-click it, or
use the VS Code "Live Server" extension). It calls the backend at
`http://127.0.0.1:8000`, so make sure the backend is running first.

The map loads centred on Pune (via free OpenStreetMap tiles) and can't be
panned or zoomed outside it. Click anywhere within Pune, search a place
name, or use "Use my location" to check conditions there.

If the backend isn't reachable, a banner appears immediately on load
saying so (rather than a confusing error only when you click something).

### Troubleshooting: "Can't reach the backend" / "Failed to fetch"

This means the browser couldn't reach `http://127.0.0.1:8000` at all —
it's almost always one of these, roughly in order of likelihood:

1. **The backend isn't running.** Check the terminal you ran
   `uvicorn backend.app:app --reload` in — it should still be open and
   show `Uvicorn running on http://127.0.0.1:8000` with no error text
   after it. If that terminal was closed, or shows a traceback, restart
   it (see section 5).
2. **It's running on a different port.** If you started it with
   `--port 8001` or similar, either drop that flag (the frontend expects
   the default port 8000) or edit `API_URL` at the top of
   `frontend/js/script.js` to match.
3. **A firewall or antivirus is blocking local connections.** Some
   security software blocks a Python process from accepting connections
   the first time it runs — check for a permission prompt, or briefly
   allow `python`/`uvicorn` through it.
4. **The page was opened over a different origin than expected** (e.g.
   through a proxy or tunnel) — this project assumes both the frontend
   and backend run locally on the same machine.

If none of these are it, open the browser's DevTools (F12) → Console tab
and look for the actual error there — it's more specific than the
banner's summary.

---

## 7. How the Smart Route Recommendation works

1. The **From**/**To** place names are geocoded (Pune-scoped Nominatim).
2. The backend calls **OSRM's free public routing server**
   (`router.project-osrm.org`) asking for alternative driving routes with
   distance and an estimated travel time (based on road speeds, not live
   traffic — see section 2).
3. **If OSRM only returns one route** (it often does — this is a
   documented limitation of OSRM's own alternative-finding, not a bug
   here: see `backend/services/directions_service.py`'s docstring for
   the GitHub issues), the backend forces up to two more genuinely
   different paths by asking OSRM to route *through* a waypoint nudged
   perpendicular to the direct line between the two points. This means
   you'll (almost) always see real route choices, not one route wearing
   three tags.
4. Each route's path is sampled at **8 evenly-spaced points**. The
   existing air-quality service + ML model are reused to get a predicted
   AQI at each sample point, then averaged into a route-level "AQI
   exposure" score.
5. Routes are labelled:
   - **Fastest** — lowest estimated travel time
   - **Cleanest** — lowest average AQI exposure
   - **Balanced** *(recommended)* — best combined score, weighting travel
     time and AQI exposure equally (each normalised 0–1 across the
     returned routes, then averaged)
6. Each route is drawn on the map as a **series of coloured segments**
   rather than one flat line: stretches where the sampled AQI is Poor or
   worse are drawn in yellow, everything else in dark charcoal — similar
   to how a traffic layer colours a route by congestion, but for air
   quality. The recommended route is drawn thicker and bolder; clicking
   any route card highlights that route's segments and dims the others.

This reuses 100% of the existing air-quality + ML pipeline — no separate
pollution model was built for routing, and no paid routing API is used.

---

## 8. API Endpoints

| Method | Endpoint                 | Description                                                        |
|--------|---------------------------|--------------------------------------------------------------------|
| GET    | `/`                       | Health/welcome message                                             |
| GET    | `/health`                 | Health check                                                       |
| GET    | `/weather`                | `?latitude=&longitude=` → live weather                             |
| GET    | `/air-quality`            | `?latitude=&longitude=` → live pollutant concentrations            |
| GET    | `/geocode`                | `?q=<place name>` → lat/lon for a place in Pune (OpenStreetMap)    |
| POST   | `/predict-aqi`            | `?pm25=&pm10=&no2=&so2=&co=&o3=` → predicted AQI + category         |
| GET    | `/forecast`               | `?latitude=&longitude=&hours=24` → hourly AQI forecast, key snapshots, best travel window |
| GET    | `/heatmap`                | `?latitude=&longitude=&radius_km=10&grid_size=4` → grid of nearby points with predicted AQI |
| GET    | `/mobility-recommendation`| `?aqi_category=&temperature=&humidity=&wind_speed=` → travel advice |
| GET    | `/route`                  | `?origin_lat=&origin_lon=&dest_lat=&dest_lon=` → route options with distance, traffic ETA, AQI exposure, recommendation |
| GET    | `/environment`            | `?latitude=&longitude=` → weather + air quality + AQI prediction + mobility recommendation (all-in-one, used by the frontend) |

`/environment`, `/forecast`, `/heatmap`, `/geocode`, and `/route` all
reject coordinates/places outside Pune's bounding box with a `400`/`404`
and a clear message.

---

## 9. Re-training the Model (optional)

The trained model is already included in `models/aqi_prediction_model.pkl`.
To retrain it on `data/pune_aqi_dataset.csv` (or a new Pune dataset you
provide):

```bash
python src/model/train_model.py
python src/model/evaluate_model.py   # prints MAE, RMSE, R² on a test split
```

---

## 10. Notes for Submission

- CSE (AI & ML), Final Year Project — Pune region only, per mentor guidance
- Tech stack: Python, FastAPI, scikit-learn (Random Forest), Pandas,
  HTML/CSS/JavaScript, Leaflet + OpenStreetMap (map), OSRM (routing),
  OpenStreetMap Nominatim (geocoding). The 24-hour forecast chart is
  hand-drawn as inline SVG (no charting library), so it can't fail to
  load from a blocked or slow CDN.
- No API keys or secrets anywhere in this project — every external
  service used is free and keyless, so there's nothing to configure or
  keep out of source control on that front.

## 11. Known Limitation — Model Training Range

The bundled model (`models/aqi_prediction_model.pkl`) was trained on
`data/pune_aqi_dataset.csv`, where PM2.5 tops out around **37.5 µg/m³** and
PM10 around **48.5 µg/m³**. Random Forest models don't extrapolate well
beyond the ranges they were trained on — for pollutant values well above
those (which do happen on real high-pollution days), the model can return
similar/flat predictions instead of scaling further up. This affects the
Forecast Dashboard, Pollution Zone view, and Route AQI exposure scores on
unusually bad air days. It works correctly for typical/moderate
conditions. Retraining on a dataset with a wider pollutant range — e.g.
the Pune dataset your mentor asked you to use — would fix this.
