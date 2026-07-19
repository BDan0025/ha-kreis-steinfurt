"""Config flow for Kreis Steinfurt integration."""

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, NAME


class KreisSteinfurtConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup."""

        if user_input is not None:
            return self.async_create_entry(
                title=NAME,
                data={},
            )

        return self.async_show_form(
            step_id="user"
        )