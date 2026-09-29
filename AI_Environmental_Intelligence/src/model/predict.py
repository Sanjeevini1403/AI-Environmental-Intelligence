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


    predicted_aqi = model.predict(
        input_data
    )[0]


    predicted_aqi = max(
        0,
        min(500, predicted_aqi)
    )


    category = get_aqi_category(
        predicted_aqi
    )


    return {
        "predicted_aqi": round(
            float(predicted_aqi),
            2
        ),
        "category": category
    }


if __name__ == "__main__":

    result = predict_aqi(
        pm25=20,
        pm10=30,
        no2=40,
        so2=10,
        co=70,
        o3=30
    )

    print("\nAQI Prediction")
    print("-------------------------")
    print("Predicted AQI:", result["predicted_aqi"])
    print("Category:", result["category"])