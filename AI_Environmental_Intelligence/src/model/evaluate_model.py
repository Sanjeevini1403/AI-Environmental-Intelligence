import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "pune_aqi_dataset.csv"
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "aqi_prediction_model.pkl"
)


print("Loading dataset...")

df = pd.read_csv(DATA_PATH)


features = [
    "PM2_5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3"
]

target = "AQI"


X = df[features]
y = df[target]


X = X.fillna(X.median())
y = y.fillna(y.median())


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Loading trained model...")

model = joblib.load(MODEL_PATH)


predictions = model.predict(X_test)


mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n================================")
print("AQI MODEL EVALUATION")
print("================================")

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

print("\nSample Predictions")
print("--------------------------------")

results = pd.DataFrame({
    "Actual_AQI": y_test.values[:10],
    "Predicted_AQI": predictions[:10]
})

print(results.to_string(index=False))