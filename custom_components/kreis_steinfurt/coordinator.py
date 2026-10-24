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
from .const import (
    CONF_AREAS,
    CONF_RETENTION,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    KREIS_STEINFURT_AREAS,
    RETENTION_48_HOURS,
)
from .history import EinsatzHistory
from .models import Einsatz

_LOGGER = logging.getLogger(__name__)


class KreisSteinfurtCoordinator(DataUpdateCoordinator):
    """Coordinator for Kreis Steinfurt data."""

    def __init__(self, hass, entry) -> None:
        """Initialize the coordinator."""

        self._entry = entry
        self._history = EinsatzHistory(hass, entry.entry_id)

        self._client = KreisSteinfurtClient(
            async_get_clientsession(hass)
        )

    async def async_initialize(self) -> None:
        """Load retained incidents before the first source refresh."""
        await self._history.async_load()

    @property
    def monitored_areas(self) -> set[str]:
        """Return the currently selected Kreis Steinfurt municipalities."""
        return set(self._entry.options.get(CONF_AREAS, KREIS_STEINFURT_AREAS))

    @property
    def retention(self) -> str:
        """Return the configured incident entity retention."""
        return self._entry.options.get(CONF_RETENTION, RETENTION_48_HOURS)

    @property
    def retained_einsaetze(self) -> list[Einsatz]:
        """Return stored incidents still within their retention period."""
        return self._history.retained_einsaetze(self.retention)

    def get_retained_einsatz(self, einsatznr: str) -> Einsatz | None:
        """Return one retained incident for a dynamic entity."""
        return self._history.get(einsatznr, self.retention)

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

            await self._history.async_update(einsaetze, self.retention)

            _LOGGER.debug(
                "%s Einsätze gefunden",
                len(einsaetze),
            )

            return einsaetze

        except Exception as err:
            raise UpdateFailed(
                f"Fehler beim Abrufen der Einsatzdaten: {err}"
            ) from err
