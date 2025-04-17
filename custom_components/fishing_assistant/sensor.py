from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from .const import DOMAIN

from .score import get_fish_score

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities
):
    """Set up fishing assistant sensors from a config entry."""
    data = config_entry.data
    sensors = []

    name = data["name"]
    lat = data["latitude"]
    lon = data["longitude"]
    fish_list = data["fish"]
    body_type = data["body_type"]
    timezone = data["timezone"]
    elevation = data["elevation"]

    for fish in fish_list:
        sensors.append(
            FishScoreSensor(
                name=name,
                fish=fish,
                lat=lat,
                lon=lon,
                body_type=body_type,
                timezone=timezone,
                elevation=elevation,
            )
        )

    async_add_entities(sensors)


class FishScoreSensor(Entity):
    def __init__(self, name, fish, lat, lon, body_type, timezone, elevation):
        self._name = f"{name.lower().replace(' ', '_')}_{fish}_score"
        self._friendly_name = f"{name} ({fish.title()}) Fishing Score"
        self._state = None
        self._attrs = {
            "fish": fish,
            "location": name,
            "lat": lat,
            "lon": lon,
            "body_type": body_type,
            "timezone": timezone,
            "elevation": elevation,
        }

    @property
    def name(self):
        return self._friendly_name

    @property
    def unique_id(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

    async def async_update(self):
        # Placeholder: fake score for now
        self._state = 0.75
        
        
async def async_update(self):
    self._state = await get_fish_score(
        fish=self._attrs["fish"],
        lat=self._attrs["lat"],
        lon=self._attrs["lon"],
        timezone=self._attrs["timezone"],
        elevation=self._attrs["elevation"],
        body_type=self._attrs["body_type"],
    )
