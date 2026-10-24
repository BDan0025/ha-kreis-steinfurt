"""Config flow for Kreis Steinfurt integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

from .const import (
    CONF_AREAS,
    CONF_KARTENPOSITION,
    CONF_RETENTION,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    KREIS_STEINFURT_AREAS,
    MAP_LOCATION_AUTOMATIC,
    MAP_LOCATION_OPTIONS,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    NAME,
    RETENTION_48_HOURS,
    RETENTION_OPTIONS,
)


class KreisSteinfurtConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow."""

    VERSION = 2

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> KreisSteinfurtOptionsFlow:
        """Return the options flow for this integration."""
        return KreisSteinfurtOptionsFlow()

    async def async_step_user(self, user_input=None):
        """Handle the initial setup."""

        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=NAME,
                data={},
            )

        return self.async_show_form(
            step_id="user",
        )


class KreisSteinfurtOptionsFlow(config_entries.OptionsFlow):
    """Handle user-configurable monitoring settings."""

    async def async_step_init(self, user_input: dict | None = None):
        """Manage polling, retention and monitored areas."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                ): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL),
                ),
                vol.Required(
                    CONF_RETENTION,
                    default=options.get(CONF_RETENTION, RETENTION_48_HOURS),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=list(RETENTION_OPTIONS),
                        translation_key="retention",
                    )
                ),
                vol.Required(
                    CONF_KARTENPOSITION,
                    default=options.get(CONF_KARTENPOSITION, MAP_LOCATION_AUTOMATIC),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=list(MAP_LOCATION_OPTIONS),
                        translation_key="kartenposition",
                    )
                ),
                vol.Required(
                    CONF_AREAS,
                    default=options.get(CONF_AREAS, list(KREIS_STEINFURT_AREAS)),
                ): SelectSelector(
                    SelectSelectorConfig(
                        options=list(KREIS_STEINFURT_AREAS),
                        multiple=True,
                        translation_key="areas",
                    )
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=data_schema)
