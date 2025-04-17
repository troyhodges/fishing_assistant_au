from __future__ import annotations

import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import DOMAIN, DEFAULT_NAME
from .helpers.location import resolve_location_metadata_sync
from .fish_profiles import get_fish_species


class FishingAssistantConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Fishing Assistant."""

    VERSION = 1
    # This makes it show up in the UI
    DOMAIN = DOMAIN

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            name = user_input["name"]
            lat = user_input["latitude"]
            lon = user_input["longitude"]
            fish = user_input["fish"]
            body_type = user_input["body_type"]

            # Get elevation and timezone once
            metadata = await self.hass.async_add_executor_job(resolve_location_metadata_sync, lat, lon)

            # Create an entry title that's unique
            entry_title = f"{name}"

            return self.async_create_entry(
                title=entry_title,
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
                    options=[
                        {"value": f, "label": f.replace("_", " ").title()}
                        for f in sorted(get_fish_species())
                    ],
                    multiple=True,
                    mode=selector.SelectSelectorMode.DROPDOWN
                )
            ),
            vol.Required("body_type"): vol.In(["lake", "river", "pond", "reservoir"]),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    # Add a method to allow users to add more locations
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """No options for now."""
        return None