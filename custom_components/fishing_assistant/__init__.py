import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType
from .helpers.location import resolve_location_metadata


from .const import DOMAIN
from .helpers.location import resolve_location_metadata

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry):
    """Set up Fishing Assistant from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass, config_entry):
    return await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Fishing Assistant from YAML config."""
    conf = config.get(DOMAIN)

    if not conf:
        _LOGGER.warning("Fishing Assistant is not configured.")
        return True

    hass.data.setdefault(DOMAIN, {})

    locations = conf.get("locations", [])
    resolved_locations = []

    for location in locations:
        name = location.get("name")
        fish = location.get("fish", [])
        body_type = location.get("body_type", "lake")
        lat = location.get("latitude")
        lon = location.get("longitude")
        zone_id = location.get("zone")

        # If zone is given, try to resolve lat/lon from Home Assistant
        if zone_id:
            zone = hass.states.get(zone_id)
            if not zone:
                _LOGGER.error(f"Zone '{zone_id}' not found in HA.")
                continue
            lat = zone.attributes.get("latitude")
            lon = zone.attributes.get("longitude")

        if lat is None or lon is None:
            _LOGGER.error(f"Location '{name}' is missing valid coordinates.")
            continue

        # Enrich with metadata (timezone, elevation)
        metadata = await resolve_location_metadata(hass, lat, lon)

        resolved_locations.append({
            "name": name,
            "latitude": lat,
            "longitude": lon,
            "fish": fish,
            "body_type": body_type,
            "timezone": metadata.get("timezone"),
            "elevation": metadata.get("elevation")
        })

    hass.data[DOMAIN]["locations"] = resolved_locations

    _LOGGER.info(f"Fishing Assistant loaded {len(resolved_locations)} locations.")

    # Load sensor platform
    hass.async_create_task(
        async_load_platform(hass, "sensor", DOMAIN, {}, config)
    )

    return True
