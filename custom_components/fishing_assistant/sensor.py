from homeassistant.helpers.entity import Entity
from .const import DOMAIN, FISH_TYPES
from .score import get_fish_scores

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensors = [FishScoreSensor(fish) for fish in FISH_TYPES]
    async_add_entities(sensors, True)

class FishScoreSensor(Entity):
    def __init__(self, fish):
        self._fish = fish
        self._state = None

    @property
    def name(self):
        return f"{self._fish.capitalize()} Score"

    @property
    def state(self):
        return self._state

    def update(self):
        scores = get_fish_scores()
        self._state = scores.get(self._fish, 0)
