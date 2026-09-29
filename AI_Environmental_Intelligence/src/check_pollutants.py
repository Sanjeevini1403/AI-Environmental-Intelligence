import pandas as pd

# Load cleaned dataset
file_path = "data/pune_environmental_cleaned.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Shape:", df.shape)

# Pollutant columns
pollutants = [
    "PM2_MAX",
    "PM10_MAX",
    "NO2_MAX",
    "SO2_MAX",
    "CO_MAX",
    "OZONE_MAX"
]

print("\n========== POLLUTANT STATISTICS ==========")

print(df[pollutants].describe())

print("\n========== SAMPLE POLLUTANT VALUES ==========")

print(df[pollutants].head(10))

print("\n========== MINIMUM VALUES ==========")

print(df[pollutants].min())

print("\n========== MAXIMUM VALUES ==========")

print(df[pollutants].max())