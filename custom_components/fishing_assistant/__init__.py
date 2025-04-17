import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Fishing Assistant from YAML configuration."""
    _LOGGER.info("Fishing Assistant component is setting up.")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Fishing Assistant from a config entry."""
    _LOGGER.info("Fishing Assistant config entry is setting up.")
    
    # Store config entry in hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data
    
    # Forward entry setup to sensor platform
    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Fishing Assistant config entry is unloading.")
    
    # Unload the sensor platform
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, ["sensor"])
    
    # Remove config entry from hass data
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)
        
    return unload_ok