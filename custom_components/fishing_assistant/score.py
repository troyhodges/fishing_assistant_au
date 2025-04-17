import datetime
import httpx
from typing import Optional
from .fish_profiles import FISH_PROFILES

OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

async def get_fish_score(
    fish: str,
    lat: float,
    lon: float,
    timezone: str,
    elevation: float,
    body_type: str
) -> float:
    """Calculate a score from 0 to 1 for the given species at this location."""

    fish_profile = FISH_PROFILES.get(fish)

    if not fish_profile:
        return 0.0

    try:
        now = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        forecast_url = (
            f"{OPEN_METEO_BASE}?latitude={lat}&longitude={lon}&hourly=temperature_2m,"
            f"cloudcover,pressure_msl&timezone={timezone}&elevation={elevation}&start_date={now.date()}&end_date={now.date()}"
        )

        async with httpx.AsyncClient() as client:
            resp = await client.get(forecast_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()

        temps = data["hourly"]["temperature_2m"]
        clouds = data["hourly"]["cloudcover"]
        pressure = data["hourly"]["pressure_msl"]
        times = data["hourly"]["time"]

        # Index of current hour
        hour_index = [i for i, t in enumerate(times) if t.startswith(now.strftime('%Y-%m-%dT%H'))]
        if not hour_index:
            return 0.0
        i = hour_index[0]

        # Extract values
        temp = temps[i]
        cloud = clouds[i]
        press = pressure[i]

        # --- Calculate Scores ---
        temp_score = _score_temp(temp, fish_profile["temp_range"])
        cloud_score = 1 - abs(cloud - fish_profile["ideal_cloud"]) / 100
        press_score = 1 if fish_profile["prefers_low_pressure"] and press < 1015 else 0.7

        # Weighted average
        score = (
            temp_score * 0.4 +
            cloud_score * 0.3 +
            press_score * 0.3
        )
        return round(score, 2)

    except Exception as e:
        print(f"Error fetching score for {fish}: {e}")
        return 0.0


def _score_temp(temp: float, ideal_range: tuple[float, float]) -> float:
    low, high = ideal_range
    if temp < low:
        return max(0, (temp - (low - 10)) / 10)
    elif temp > high:
        return max(0, (high + 10 - temp) / 10)
    return 1.0
