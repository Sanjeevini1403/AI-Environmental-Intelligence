"""
Smart Mobility Recommendation Service with Health Sensitivity Profiles.

Combines predicted AQI category and live weather conditions (temperature, humidity,
wind speed) with personalized user health sensitivity settings:
- Normal / General Public
- Asthmatic / Respiratory Vulnerability
- Elderly (Seniors 65+)
- Children (<12 years)
- Outdoor Athletes & Cyclists

Tailors alert thresholds, transport mode advice, window recommendations, and protective mask requirements.
"""


HEALTH_PROFILES = {
    "normal": {
        "label": "General Public / Normal",
        "alert_threshold_aqi": 150,
        "description": "Standard population with typical environmental tolerance."
    },
    "asthmatic": {
        "label": "Asthmatic / Respiratory Condition",
        "alert_threshold_aqi": 75,
        "description": "High respiratory sensitivity; bronchial hyper-responsiveness."
    },
    "elderly": {
        "label": "Elderly (Seniors 65+)",
        "alert_threshold_aqi": 90,
        "description": "Elevated vulnerability to cardiovascular and particulate stress."
    },
    "children": {
        "label": "Children (< 12 Years)",
        "alert_threshold_aqi": 80,
        "description": "Rapid breathing rate and developing lung tissues."
    },
    "athlete": {
        "label": "Outdoor Athlete / Marathoner",
        "alert_threshold_aqi": 100,
        "description": "Deep volumetric inhalation during sustained aerobic training."
    }
}


def _heat_note(temperature):
    if temperature is None:
        return None
    if temperature >= 38:
        return "Severe heat condition - carry electrolytes and avoid midday travel."
    if temperature >= 33:
        return "Warm conditions - prefer shaded routes and stay hydrated."
    return None


def _wind_note(wind_speed):
    if wind_speed is None:
        return None
    if wind_speed >= 30:
        return "High wind velocity - two-wheeler riders should be cautious of dust gusts."
    return None


def get_mobility_recommendation(
    aqi_category: str,
    temperature: float = None,
    humidity: float = None,
    wind_speed: float = None,
    health_profile: str = "normal",
    aqi_value: float = None
):
    category = (aqi_category or "").strip()
    profile = (health_profile or "normal").lower().strip()
    if profile not in HEALTH_PROFILES:
        profile = "normal"

    profile_info = HEALTH_PROFILES[profile]
    threshold = profile_info["alert_threshold_aqi"]
    is_breached = (aqi_value is not None and aqi_value >= threshold) or category in ["Poor", "Very Poor", "Severe"]

    # Base recommendation rules
    if category in ("Good", "Satisfactory"):
        if profile == "asthmatic" and aqi_value and aqi_value > 75:
            recommended_mode = "Walking with Inhaler / Public Transit"
            mask_required = False
            best_travel_window = "Late morning or early afternoon"
            message = "Air is acceptable, but sensitive asthmatic individuals should carry medication."
        elif profile == "athlete":
            recommended_mode = "Outdoor Cycling / Running"
            mask_required = False
            best_travel_window = "Morning (06:00 - 08:30 AM)"
            message = "Optimal air conditions for sustained outdoor endurance training."
        else:
            recommended_mode = "Walking / Cycling"
            mask_required = False
            best_travel_window = "Anytime today"
            message = "Air quality is healthy for all outdoor mobility."

    elif category == "Moderate":
        if profile in ("asthmatic", "elderly", "children"):
            recommended_mode = "Enclosed Vehicle / Metro / Bus"
            mask_required = True
            best_travel_window = "Midday (12:00 - 03:30 PM)"
            message = (
                f"Personalized Alert for {profile_info['label']}: Current AQI exceeds your sensitivity "
                f"threshold ({threshold}). Avoid prolonged outdoor exposure and use a protective mask."
            )
        elif profile == "athlete":
            recommended_mode = "Indoor Cardio Training"
            mask_required = False
            best_travel_window = "Early morning before traffic builds"
            message = "Moderate particulate levels. Shift heavy aerobic running indoors to protect lung capacity."
        else:
            recommended_mode = "Cycling / Public Transport"
            mask_required = False
            best_travel_window = "Morning (06:00 - 09:30 AM) or Evening"
            message = "Moderate air quality. Safe for normal commute, but minimize idling in traffic jams."

    elif category == "Poor":
        recommended_mode = "Enclosed Four-Wheeler (AC Recirculate) / Metro"
        mask_required = True
        best_travel_window = "Early morning (before 08:00 AM) or postpone"
        if profile == "asthmatic":
            message = "HIGH RISK FOR ASTHMA: Avoid all outdoor walking and open two-wheelers. Carry rescue inhaler."
        else:
            message = "Poor air quality. Avoid open-air transit. Wear N95 respirator mask outdoors."

    elif category == "Very Poor":
        recommended_mode = "Enclosed AC Car / Postpone Non-Essential Travel"
        mask_required = True
        best_travel_window = "Postpone if possible"
        message = "Very poor air quality. Toxic particulates elevated. N95 mask required outdoors."

    else:  # Severe
        recommended_mode = "Strictly Avoid Outdoor Travel"
        mask_required = True
        best_travel_window = "Stay Indoors"
        message = "HAZARDOUS AIR QUALITY: Severe respiratory emergency conditions. Keep air purifiers running."

    notes = [n for n in (_heat_note(temperature), _wind_note(wind_speed)) if n]

    return {
        "health_profile": profile,
        "profile_label": profile_info["label"],
        "alert_threshold": threshold,
        "threshold_breached": is_breached,
        "recommended_mode": recommended_mode,
        "mask_required": mask_required,
        "best_travel_window": best_travel_window,
        "message": message,
        "additional_notes": notes
    }
