import httpx
from timezonefinder import TimezoneFinder
from homeassistant.core import HomeAssistant

async def resolve_location_metadata(hass: HomeAssistant, lat: float, lon: float) -> dict:
    """Calculate timezone and elevation for a given lat/lon."""
    # Get timezone
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=lat, lng=lon) or hass.config.time_zone

    # Default elevation if we can't get it
    elevation = 500

    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            if response.status_code == 200:
                result = response.json().get("results", [{}])[0]
                elevation = result.get("elevation", elevation)
    except Exception as e:
        # You might want to log this
        hass.logger.warning(f"Could not fetch elevation for ({lat},{lon}): {e}")

    return {
        "timezone": timezone,
        "elevation": elevation
    }
