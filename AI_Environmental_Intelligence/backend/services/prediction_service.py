import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "aqi_prediction_model.pkl"
)


model = joblib.load(MODEL_PATH)


FEATURES = [
    "PM2_5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3"
]


def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


def predict_aqi(
    pm25,
    pm10,
    no2,
    so2,
    co,
    o3
):

    input_data = pd.DataFrame(
        [[
            pm25,
            pm10,
            no2,
            so2,
            co,
            o3
        ]],
        columns=FEATURES
    )

    prediction = model.predict(input_data)[0]

    prediction = max(
        0,
        min(500, prediction)
    )

    return {
        "predicted_aqi": round(float(prediction), 2),
        "category": get_aqi_category(prediction)
    }