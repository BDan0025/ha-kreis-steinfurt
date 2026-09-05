"""Config flow for Kreis Steinfurt integration."""

from homeassistant import config_entries

from .const import DOMAIN, NAME


class KreisSteinfurtConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow."""

    VERSION = 2

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
