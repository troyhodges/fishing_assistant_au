import httpx
from timezonefinder import TimezoneFinder
from homeassistant.core import HomeAssistant

async def resolve_location_metadata(hass: HomeAssistant, lat: float, lon: float) -> dict:
    """Calculate timezone and elevation for a given lat/lon."""
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=lat, lng=lon) or hass.config.time_zone
    elevation = 500  # Default

    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            if response.status_code == 200:
                results = response.json().get("results", [])
                if results:
                    elevation = results[0].get("elevation", elevation)
    except Exception as e:
        _LOGGER = getattr(hass, "logger", None)
        if _LOGGER:
            _LOGGER.warning(f"Elevation API failed: {e}")

    return {"timezone": timezone, "elevation": elevation}
