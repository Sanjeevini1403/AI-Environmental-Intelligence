import pandas as pd
# Load cleaned dataset
file_path = "data/pune_environmental_cleaned.csv"
df = pd.read_csv(file_path)
print("Dataset loaded successfully!")
print("Original shape:", df.shape)
# Create average pollutant features
df["PM2_5"] = (df["PM2_MAX"] + df["PM2_MIN"]) / 2
df["PM10"] = (df["PM10_MAX"] + df["PM10_MIN"]) / 2
df["NO2"] = (df["NO2_MAX"] + df["NO2_MIN"]) / 2
df["SO2"] = (df["SO2_MAX"] + df["SO2_MIN"]) / 2
df["CO"] = (df["CO_MAX"] + df["CO_MIN"]) / 2
df["O3"] = (df["OZONE_MAX"] + df["OZONE_MIN"]) / 2
# Display new features
print("\n========== NEW POLLUTANT FEATURES ==========")
print(df[
    ["PM2_5", "PM10", "NO2", "SO2", "CO", "O3"]
].head())
print("\n========== FEATURE STATISTICS ==========")
print(df[
    ["PM2_5", "PM10", "NO2", "SO2", "CO", "O3"]
].describe())

# Save feature-engineered dataset
output_file = "data/pune_environmental_features.csv"

df.to_csv(output_file, index=False)

print("\nFeature engineering completed!")
print("Saved at:", output_file)