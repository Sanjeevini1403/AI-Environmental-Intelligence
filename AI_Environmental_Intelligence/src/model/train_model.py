import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "pune_aqi_dataset.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "aqi_prediction_model.pkl"
)


os.makedirs(MODEL_DIR, exist_ok=True)


print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())


features = [
    "PM2_5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3"
]

target = "AQI"


missing_features = [
    column for column in features
    if column not in df.columns
]

if missing_features:
    raise ValueError(
        f"Missing feature columns: {missing_features}"
    )


if target not in df.columns:
    raise ValueError(
        f"Target column '{target}' not found in dataset"
    )


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


print("\nTraining Random Forest model...")


model = RandomForestRegressor(
    n_estimators=150,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)


model.fit(X_train, y_train)


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


print("\nModel Evaluation")
print("-------------------------")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


joblib.dump(
    model,
    MODEL_PATH
)


print("\nModel saved successfully!")
print("Model path:", MODEL_PATH)

print("\nFeatures used:")
for feature in features:
    print("-", feature)

print("\nTarget:")
print("-", target)