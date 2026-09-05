"""HTTP client for the Kreis Steinfurt incident list."""

from __future__ import annotations

from aiohttp import ClientSession

from .const import SOURCE_URL
from .models import Einsatz
from .parser import parse_einsaetze


class KreisSteinfurtClient:
    """Retrieve and parse the public incident list."""

    def __init__(self, session: ClientSession, url: str = SOURCE_URL) -> None:
        """Initialize the client."""
        self._session = session
        self._url = url

    async def async_get_einsaetze(self) -> list[Einsatz]:
        """Return the incidents currently published by Kreis Steinfurt."""
        async with self._session.get(
            self._url,
            headers={"User-Agent": "Home Assistant Kreis Steinfurt integration"},
        ) as response:
            response.raise_for_status()
            html = await response.text()

        return parse_einsaetze(html)
