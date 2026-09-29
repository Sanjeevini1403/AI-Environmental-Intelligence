import requests
import csv
from datetime import datetime

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Pune coordinates
latitude = 18.5204
longitude = 73.8567


# ---------------- WEATHER DATA ----------------

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

weather_response = requests.get(
    WEATHER_URL,
    params=weather_params
)

if weather_response.status_code != 200:
    print("Weather API Error:", weather_response.status_code)
    exit()

weather_data = weather_response.json()

temperature = weather_data["current"]["temperature_2m"]
humidity = weather_data["current"]["relative_humidity_2m"]
wind_speed = weather_data["current"]["wind_speed_10m"]


# ---------------- AIR QUALITY DATA ----------------

air_quality_params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
}

air_response = requests.get(
    AIR_QUALITY_URL,
    params=air_quality_params
)

if air_response.status_code != 200:
    print("Air Quality API Error:", air_response.status_code)
    exit()

air_data = air_response.json()

pm25 = air_data["hourly"]["pm2_5"][0]
pm10 = air_data["hourly"]["pm10"][0]
co = air_data["hourly"]["carbon_monoxide"][0]
no2 = air_data["hourly"]["nitrogen_dioxide"][0]
so2 = air_data["hourly"]["sulphur_dioxide"][0]
o3 = air_data["hourly"]["ozone"][0]

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------- SAVE TO CSV ----------------

file_path = "data/pune_environmental_data.csv"

headers = [
    "timestamp",
    "latitude",
    "longitude",
    "temperature",
    "humidity",
    "wind_speed",
    "pm2_5",
    "pm10",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone"
]

row = [
    timestamp,
    latitude,
    longitude,
    temperature,
    humidity,
    wind_speed,
    pm25,
    pm10,
    co,
    no2,
    so2,
    o3
]

with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerow(row)

print("\n========== DATA COLLECTED ==========")
print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Wind Speed:", wind_speed, "km/h")
print("PM2.5:", pm25, "µg/m³")
print("PM10:", pm10, "µg/m³")
print("CO:", co, "µg/m³")
print("NO2:", no2, "µg/m³")
print("SO2:", so2, "µg/m³")
print("O3:", o3, "µg/m³")

print("\nCSV file created successfully!")
print("Saved at:", file_path)