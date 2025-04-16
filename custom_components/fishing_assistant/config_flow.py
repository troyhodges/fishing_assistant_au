from __future__ import annotations

import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import DOMAIN, FISH_SPECIES
from .helpers.location import resolve_location_metadata

class FishingAssistantConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Fishing Assistant."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors = {}

        if user_input is not None:
            name = user_input["name"]
            lat = user_input["latitude"]
            lon = user_input["longitude"]
            fish = user_input["fish"]
            body_type = user_input["body_type"]

            # Get elevation and timezone once
            metadata = await resolve_location_metadata(self.hass, lat, lon)

            return self.async_create_entry(
                title=name,
                data={
                    "name": name,
                    "latitude": lat,
                    "longitude": lon,
                    "fish": fish,
                    "body_type": body_type,
                    "timezone": metadata.get("timezone"),
                    "elevation": metadata.get("elevation")
                }
            )

        # First step: let user define one location
        schema = vol.Schema({
            vol.Required("name"): str,
            vol.Required("latitude"): vol.Coerce(float),
            vol.Required("longitude"): vol.Coerce(float),
            vol.Required("fish"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[{"value": f, "label": f.replace("_", " ").title()} for f in FISH_SPECIES],
                    multiple=True,
                    mode=selector.SelectSelectorMode.DROPDOWN
                )
            ),
            vol.Required("body_type"): vol.In(["lake", "river", "pond", "canal", "reservoir"]),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
