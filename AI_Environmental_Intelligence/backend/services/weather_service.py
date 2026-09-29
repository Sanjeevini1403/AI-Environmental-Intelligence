import requests


WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude, longitude):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    response = requests.get(
        WEATHER_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "temperature_unit": "°C",
        "humidity_unit": "%",
        "wind_speed_unit": "km/h"
    }