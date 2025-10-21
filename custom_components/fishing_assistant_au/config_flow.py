from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN
from .helpers.location import resolve_location_metadata_sync
from .fish_profiles import get_fish_species

class FishingAssistantConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Fishing Assistant config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            name = user_input["name"]
            lat = user_input["latitude"]
            lon = user_input["longitude"]
            fish = user_input["fish"]
            body_type = user_input["body_type"]

            await self.async_set_unique_id(f"{lat:.5f}_{lon:.5f}")
            self._abort_if_unique_id_configured()

            metadata = await self.hass.async_add_executor_job(
                resolve_location_metadata_sync, lat, lon
            )

            return self.async_create_entry(
                title=name,
                data={
                    "name": name,
                    "latitude": lat,
                    "longitude": lon,
                    "fish": fish,
                    "body_type": body_type,
                    "elevation": metadata.get("elevation"),
                    "timezone": metadata.get("timezone"),
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("latitude"): vol.Coerce(float),
                vol.Required("longitude"): vol.Coerce(float),
                vol.Required("fish"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": f, "label": f.replace("_", " ").title()}
                            for f in sorted(get_fish_species())
                        ],
                        multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN
                    )
                ),
                vol.Required("body_type"): vol.In(["lake", "river", "pond", "reservoir"]),
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FishingAssistantOptionsFlow(config_entry)
    
    @staticmethod
    @callback
    def async_get_entry_title(entry: ConfigEntry) -> str:
        """Return the title of the config entry shown in the UI."""
        return entry.data.get("name", "Fishing Location")



class FishingAssistantOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Fishing Assistant."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("fish", default=self.config_entry.data.get("fish", [])): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"value": f, "label": f.replace("_", " ").title()}
                            for f in sorted(get_fish_species())
                        ],
                        multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN
                    )
                ),
                vol.Required("body_type", default=self.config_entry.data.get("body_type", "lake")):
                    vol.In(["lake", "river", "pond", "reservoir"]),
            })
        )
