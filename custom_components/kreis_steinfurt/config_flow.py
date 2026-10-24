"""Config flow for Kreis Steinfurt integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

from .const import (
    CONF_AREAS,
    CONF_RETENTION,
    DOMAIN,
    KREIS_STEINFURT_AREAS,
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
        return KreisSteinfurtOptionsFlow(config_entry)

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

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None):
        """Manage retention and monitored areas."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data_schema = vol.Schema(
            {
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
