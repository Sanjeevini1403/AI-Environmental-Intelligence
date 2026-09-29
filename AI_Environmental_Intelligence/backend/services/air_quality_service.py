import requests


AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def get_air_quality(latitude, longitude):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
        "timezone": "auto"
    }

    response = requests.get(
        AIR_QUALITY_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "pm2_5": current.get("pm2_5"),
        "pm10": current.get("pm10"),
        "carbon_monoxide": current.get("carbon_monoxide"),
        "nitrogen_dioxide": current.get("nitrogen_dioxide"),
        "sulphur_dioxide": current.get("sulphur_dioxide"),
        "ozone": current.get("ozone")
    }