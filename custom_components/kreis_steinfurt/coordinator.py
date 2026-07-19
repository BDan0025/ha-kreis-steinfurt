"""Data coordinator for Kreis Steinfurt."""

from datetime import timedelta
import logging

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import DOMAIN, SOURCE_URL, DEFAULT_SCAN_INTERVAL
from .parser import parse_einsaetze


_LOGGER = logging.getLogger(__name__)


class KreisSteinfurtCoordinator(DataUpdateCoordinator):
    """Coordinator for Kreis Steinfurt data."""

    def __init__(self, hass):

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=DEFAULT_SCAN_INTERVAL
            ),
        )

        self.url = SOURCE_URL


    async def _async_update_data(self):

        try:
            async with aiohttp.ClientSession() as session:

                async with session.get(
                    self.url,
                    timeout=10,
                ) as response:

                    html = await response.text()

        except Exception as err:

            _LOGGER.error(
                "Fehler beim Abrufen der Einsatzdaten: %s",
                err,
            )

            raise


        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        text = soup.get_text(
            "\n",
            strip=True,
        )

        einsaetze = parse_einsaetze(text)


        _LOGGER.debug(
            "%s Einsätze gefunden",
            len(einsaetze),
        )


        return einsaetze