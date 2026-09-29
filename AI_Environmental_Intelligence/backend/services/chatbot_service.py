"""
AI Environmental Intelligence Chatbot Service ("AirIQ / EcoBot").

Processes user inquiries regarding localized air quality, smart mobility advice,
health precautions for vulnerable profiles (asthma, elderly, children), mask guidelines,
traffic mitigation, and environmental science.
Supports English and Tanglish/Tamil queries seamlessly.
"""

import re
from typing import Dict, Any


def get_chatbot_response(
    query: str,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Generates intelligent contextual responses based on user query and live environmental status.
    """
    if not query or not query.strip():
        return {
            "reply": "Hello! I am **AirIQ EcoBot**, your AI Environmental Assistant. Ask me about air quality, safe routes, asthma/health precautions, or traffic conditions in English or Tamil/Tanglish!",
            "suggested_prompts": [
                "Is it safe to go outside right now?",
                "Do I need an N95 mask today?",
                "What is the cleanest route to my destination?",
                "Enaku asthma iruku, veliya pogalama?"
            ]
        }

    q = query.lower().strip()
    ctx = context or {}
    curr_aqi = ctx.get("aqi", 125)
    category = ctx.get("category", "Moderate")
    profile = ctx.get("profile", "normal").lower()
    location_name = ctx.get("location_name", "your area")

    # Detect Tanglish / Tamil keywords
    is_tanglish = any(w in q for w in [
        "veliya", "polama", "pogalama", "iruku", "epdi", "enna", "sollu", "mudiyuma",
        "kaatu", "koodathu", "thevaiya", "nallatha", "romba", "kaathu", "kulanthai"
    ])

    # 1. Asthma & Respiratory Sensitivity
    if any(w in q for w in ["asthma", "breath", "wheez", "respiratory", "inhaler", "lung"]):
        if is_tanglish:
            return {
                "reply": (
                    f"🌬️ **Asthma Health Alert for {location_name} (AQI: {curr_aqi} - {category})**:\n\n"
                    "• **Asthma irukavanga**: AQI 100 thaandinaal outdoor activities avoid pannuradhu nalladhu.\n"
                    "• Veliya poga vendiyirundha **N95 / FFP2 mask** kandippa podunga.\n"
                    "• Ungaloda **Rescue Inhaler** eppothum kaiyila vechikonga.\n"
                    "• Heavy traffic areas (NH4, Ring Road, Market) la particulate matter (PM2.5) romba athigama irukum, anga poga venaam.\n"
                    "• Home la window moodi AC-la recirculation mode use pannunga."
                ),
                "category": "health_asthma"
            }
        else:
            return {
                "reply": (
                    f"🌬️ **Asthma & Respiratory Guidance for {location_name} (Current AQI: {curr_aqi} — {category})**:\n\n"
                    f"• **Exposure Risk**: At an AQI of {curr_aqi}, fine particulates (PM2.5) and NO₂ can penetrate deep into bronchial airways, triggering spasms or wheezing.\n"
                    "• **Actionable Advice**:\n"
                    "  1. Keep an **albuterol/rescue inhaler** readily accessible.\n"
                    "  2. Limit brisk outdoor exertion, especially along heavy vehicle corridors.\n"
                    "  3. Use an **N95 or N99 respirator mask** if stepping outdoors.\n"
                    "  4. Keep windows sealed during morning and evening rush hours.\n"
                    "  5. In your car, switch air ventilation to **Cabin Air Recirculation** mode."
                ),
                "category": "health_asthma"
            }

    # 2. Mask Guidelines
    if any(w in q for w in ["mask", "n95", "cloth mask", "respirator", "face cover"]):
        if curr_aqi <= 50:
            msg = "Air quality is currently **Good**. Masks are generally not required unless you are clinically allergic to pollen or dust."
        elif curr_aqi <= 100:
            msg = "Air quality is **Satisfactory**. Sensitive individuals or those with asthma riding two-wheelers should wear a surgical or standard face mask."
        else:
            msg = (
                f"⚠️ Current AQI is **{curr_aqi} ({category})**. Regular cloth masks do NOT filter microscopic PM2.5 particles! "
                "An **N95 or FFP2 certified particulate mask** with a tight facial seal is strongly recommended for outdoor travel."
            )
        if is_tanglish:
            msg += "\n\n💡 *Tip: Cloth mask toxic gases and fine dust ah filter pannathu, N95 mask poduradhu best protection!*"
        return {"reply": msg, "category": "mask_advice"}

    # 3. Outdoor Jogging / Exercise / Walking Safety
    if any(w in q for w in ["jog", "run", "walk", "exercise", "cycle", "cycling", "outdoor", "veliya"]):
        if curr_aqi <= 100:
            rec = "✅ **Safe for outdoor activities!** The ambient air quality is within acceptable healthy limits."
            if "athlete" in profile:
                rec += " Perfect window for intensive running or cycling."
        elif curr_aqi <= 200:
            rec = (
                f"⚠️ **Caution for Outdoor Exertion (AQI: {curr_aqi})**:\n"
                "• Short walks are okay, but **avoid high-intensity cardio/jogging** outdoors.\n"
                "• Heavy breathing causes 4x more PM2.5 to enter your alveoli.\n"
                "• Shift your workout indoors or postpone to early morning (05:30 - 07:00 AM) when winds disperse pollutants."
            )
        else:
            rec = (
                f"⛔ **Severe Risk Alert (AQI: {curr_aqi})**:\n"
                "Outdoor exercise is strongly **not recommended**. Heavy particulate pollution can cause acute chest tightness and vascular stress. Please exercise indoors!"
            )
        return {"reply": rec, "category": "outdoor_activity"}

    # 4. Route & Traffic Advice
    if any(w in q for w in ["route", "traffic", "cleanest", "fastest", "drive", "travel", "vandi", "signal", "jam"]):
        return {
            "reply": (
                "🚗 **Smart Mobility & Route Selection**:\n\n"
                "• **Cleanest Route Feature**: Our system calculates cumulative pollution exposure along candidate OSRM paths. Choosing the 'Cleanest Route' avoids stop-and-go exhaust zones, cutting your toxic inhalation by up to 35%.\n"
                "• **Traffic Congestion**: Congestion spikes NO₂ and carbon monoxide levels due to idling engines. Check our map's **Traffic Layer** (Green = Free Flow, Orange = Moderate, Red = Heavy Congestion).\n"
                "• **Recommended Action**: For commute, use an enclosed four-wheeler with AC recirculate or metro/train instead of open two-wheelers during rush hours."
            ),
            "category": "routing_traffic"
        }

    # 5. Children & Elderly Care
    if any(w in q for w in ["child", "children", "baby", "kid", "elderly", "parents", "senior", "thatha", "paati"]):
        return {
            "reply": (
                f"👨‍👩‍👧‍👦 **Care for Children & Seniors (AQI: {curr_aqi} - {category})**:\n\n"
                "• **Children**: Their lung-to-body surface area is higher, and their lungs are still developing. Do not allow outdoor playground games when AQI > 150.\n"
                "• **Elderly**: Higher vulnerability to cardiac stress and airway inflammation caused by fine particulate exposure.\n"
                "• **Home Tips**: Keep indoor air clean using HEPA filtration or indoor plants like Spider Plant and Areca Palm. Hydrate frequently."
            ),
            "category": "vulnerable_groups"
        }

    # 6. Pollutant Breakdown (PM2.5, PM10, NO2, SO2, CO, O3)
    if any(w in q for w in ["pm2.5", "pm10", "no2", "so2", "ozone", "co", "pollutant"]):
        return {
            "reply": (
                "🧪 **Primary Urban Pollutants Explained**:\n\n"
                "• **PM2.5 (Fine Particles < 2.5 µm)**: Emitted by vehicle exhaust & combustion. Enters deep lungs and bloodstream; high health hazard.\n"
                "• **PM10 (Coarse Dust < 10 µm)**: Road dust and construction debris. Irritates eyes, throat, and nasal passages.\n"
                "• **NO₂ (Nitrogen Dioxide)**: Produced by diesel and petrol engine combustion; triggers airway inflammation.\n"
                "• **O₃ (Ground-level Ozone)**: Formed when sunlight reacts with vehicular emissions; strong respiratory irritant.\n"
                "• **CO (Carbon Monoxide)**: Colorless gas from incomplete combustion; reduces oxygen transport in blood."
            ),
            "category": "pollutants"
        }

    # 7. Best Travel Window
    if any(w in q for w in ["best time", "cleanest time", "when to travel", "time window", "eppa poga"]):
        return {
            "reply": (
                f"⏰ **Optimal Travel Window for {location_name}**:\n\n"
                "• **Cleanest Window**: **06:00 AM – 08:00 AM** and **01:30 PM – 03:30 PM** typically exhibit lower vehicular congestion and better thermal dispersion.\n"
                "• **Worst Window (Avoid)**: **08:30 AM – 11:30 AM** (morning office rush) and **05:30 PM – 09:00 PM** (evening gridlock).\n"
                "• Check the **Next 24 Hours Forecast Chart** on our dashboard to view the exact cleanest 2-hour window calculated by our ML model!"
            ),
            "category": "travel_window"
        }

    # Default general reply
    if is_tanglish:
        return {
            "reply": (
                f"🌿 **AirIQ Intelligence Update for {location_name}**:\n\n"
                f"Ipo current AQI **{curr_aqi}** ({category}) ah iruku.\n"
                "• Unkaluku asthma, elder care, cleanest route illa traffic pathi edhaavathu theriyanuma?\n"
                "• Keela irukura quick buttons click panni kelunga, naan udaney guide panren!"
            ),
            "category": "general"
        }
    else:
        return {
            "reply": (
                f"🌿 **AirIQ Environmental Intelligence Overview**:\n\n"
                f"Currently, {location_name} is recording an AQI of **{curr_aqi}** ({category}).\n\n"
                "You can ask me specific questions such as:\n"
                "• *'Should I wear a mask today?'*\n"
                "• *'What is the cleanest travel route?'*\n"
                "• *'Health precautions for asthma or elderly?'*\n"
                "• *'Where is traffic heavy right now?'*"
            ),
            "category": "general"
        }
