"""Data coordinator for Kreis Steinfurt."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .client import KreisSteinfurtClient
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class KreisSteinfurtCoordinator(DataUpdateCoordinator):
    """Coordinator for Kreis Steinfurt data."""

    def __init__(self, hass) -> None:
        """Initialize the coordinator."""

        self._client = KreisSteinfurtClient(
            async_get_clientsession(hass)
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL,
            ),
        )

    async def _async_update_data(self):
        """Fetch data from the website."""

        try:
            einsaetze = await self._client.async_get_einsaetze()

            _LOGGER.debug(
                "%s Einsätze gefunden",
                len(einsaetze),
            )

            return einsaetze

        except Exception as err:
            raise UpdateFailed(
                f"Fehler beim Abrufen der Einsatzdaten: {err}"
            ) from err