import pandas as pd
file_path = "data/pune_environmental_features.csv"
df = pd.read_csv(file_path)
print("Dataset loaded successfully!")
print("Shape:", df.shape)
def calculate_sub_index(concentration, breakpoints):
    """
    Calculate AQI sub-index using linear interpolation.
    """
    concentration = float(concentration)
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= concentration <= c_high:
            return (
                ((i_high - i_low) / (c_high - c_low))
                * (concentration - c_low)
                + i_low
            )
    if concentration < breakpoints[0][0]:
        return 0
    return 500
pm25_breakpoints = [
    (0, 30, 0, 50),
    (31, 60, 51, 100),
    (61, 90, 101, 200),
    (91, 120, 201, 300),
    (121, 250, 301, 400),
    (251, 500, 401, 500)
]
pm10_breakpoints = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 250, 101, 200),
    (251, 350, 201, 300),
    (351, 430, 301, 400),
    (431, 500, 401, 500)
]
no2_breakpoints = [
    (0, 40, 0, 50),
    (41, 80, 51, 100),
    (81, 180, 101, 200),
    (181, 280, 201, 300),
    (281, 400, 301, 400),
    (401, 500, 401, 500)
]

so2_breakpoints = [
    (0, 40, 0, 50),
    (41, 80, 51, 100),
    (81, 380, 101, 200),
    (381, 800, 201, 300),
    (801, 1600, 301, 400),
    (1601, 2000, 401, 500)
]


# O3 (µg/m³)
o3_breakpoints = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 168, 101, 200),
    (169, 208, 201, 300),
    (209, 748, 301, 400),
    (749, 1000, 401, 500)
]


# CO (mg/m³)
co_breakpoints = [
    (0, 1.0, 0, 50),
    (1.1, 2.0, 51, 100),
    (2.1, 10, 101, 200),
    (10.1, 17, 201, 300),
    (17.1, 34, 301, 400),
    (34.1, 50, 401, 500)
]


# =========================================
# ROUND CONCENTRATIONS
# =========================================

df["PM2_5_AQI_Value"] = df["PM2_5"].round()
df["PM10_AQI_Value"] = df["PM10"].round()
df["NO2_AQI_Value"] = df["NO2"].round()
df["SO2_AQI_Value"] = df["SO2"].round()
df["O3_AQI_Value"] = df["O3"].round()

# CO conversion:
# Dataset CO is treated as µg/m³
# CPCB CO breakpoint is mg/m³
df["CO_mg"] = df["CO"] / 1000


# =========================================
# CALCULATE INDIVIDUAL AQI SUB-INDICES
# =========================================

df["PM25_AQI"] = df["PM2_5_AQI_Value"].apply(
    lambda x: calculate_sub_index(x, pm25_breakpoints)
)

df["PM10_AQI"] = df["PM10_AQI_Value"].apply(
    lambda x: calculate_sub_index(x, pm10_breakpoints)
)

df["NO2_AQI"] = df["NO2_AQI_Value"].apply(
    lambda x: calculate_sub_index(x, no2_breakpoints)
)

df["SO2_AQI"] = df["SO2_AQI_Value"].apply(
    lambda x: calculate_sub_index(x, so2_breakpoints)
)

df["O3_AQI"] = df["O3_AQI_Value"].apply(
    lambda x: calculate_sub_index(x, o3_breakpoints)
)

df["CO_AQI"] = df["CO_mg"].apply(
    lambda x: calculate_sub_index(x, co_breakpoints)
)


# =========================================
# OVERALL AQI
# =========================================

aqi_columns = [
    "PM25_AQI",
    "PM10_AQI",
    "NO2_AQI",
    "SO2_AQI",
    "O3_AQI",
    "CO_AQI"
]

# Overall AQI = maximum pollutant sub-index
df["AQI"] = df[aqi_columns].max(axis=1)

# Round AQI to integer
df["AQI"] = df["AQI"].round().astype(int)


# =========================================
# AQI CATEGORY
# =========================================

def aqi_category(aqi):

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


df["AQI_Category"] = df["AQI"].apply(aqi_category)


# =========================================
# DISPLAY AQI RESULTS
# =========================================

print("\n========== AQI RESULTS ==========")

print(
    df[
        [
            "PM2_5",
            "PM10",
            "NO2",
            "SO2",
            "CO",
            "O3",
            "AQI",
            "AQI_Category"
        ]
    ].head(10)
)


# =========================================
# AQI STATISTICS
# =========================================

print("\n========== AQI STATISTICS ==========")

print(df["AQI"].describe())


# =========================================
# AQI CATEGORY COUNT
# =========================================

print("\n========== AQI CATEGORY COUNT ==========")

print(df["AQI_Category"].value_counts())


# =========================================
# SAVE FINAL DATASET
# =========================================

output_file = "data/pune_aqi_dataset.csv"

df.to_csv(output_file, index=False)

print("\nAQI target created successfully!")
print("Saved at:", output_file)