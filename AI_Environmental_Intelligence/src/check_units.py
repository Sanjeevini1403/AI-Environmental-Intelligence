import pandas as pd

df = pd.read_csv("data/pune_environmental_features.csv")

columns = ["PM2_5", "PM10", "NO2", "SO2", "CO", "O3"]

print("========== POLLUTANT RANGES ==========\n")

for column in columns:
    print(
        f"{column:8} | "
        f"Min: {df[column].min():8.2f} | "
        f"Mean: {df[column].mean():8.2f} | "
        f"Max: {df[column].max():8.2f}"
    )

print("\n========== SAMPLE ==========\n")
print(df[columns].head(10))