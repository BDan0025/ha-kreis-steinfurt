"""HTTP client for the Kreis Steinfurt incident list."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from aiohttp import ClientSession

from .const import SOURCE_URL
from .models import Einsatz
from .parser import parse_einsaetze, parse_pagination


@dataclass(frozen=True, slots=True)
class EinsatzAbruf:
    """All source entries and pagination metadata from one refresh."""

    einsaetze: list[Einsatz]
    seitenanzahl: int
    einsatzanzahl_auf_der_quelle: int


class KreisSteinfurtClient:
    """Retrieve and parse the public incident list."""

    def __init__(self, session: ClientSession, url: str = SOURCE_URL) -> None:
        """Initialize the client."""
        self._session = session
        self._url = url

    async def async_get_einsaetze(self) -> EinsatzAbruf:
        """Return every incident currently published by Kreis Steinfurt."""
        html = await self._async_get_page()
        einsaetze = parse_einsaetze(html)
        pagination = parse_pagination(html)

        if pagination is None:
            return EinsatzAbruf(einsaetze, 1, len(einsaetze))

        total, page_size = pagination
        page_count = max(1, ceil(total / page_size))
        for offset in range(1, page_count):
            einsaetze.extend(parse_einsaetze(await self._async_get_page(offset)))

        # The public list can change between page requests. Keep each incident once.
        unique_einsaetze = {einsatz.einsatznr: einsatz for einsatz in einsaetze}
        return EinsatzAbruf(
            list(unique_einsaetze.values()),
            page_count,
            total,
        )

    async def _async_get_page(self, offset: int | None = None) -> str:
        """Retrieve one source page, optionally using its zero-based offset."""
        url = self._url if offset is None else _url_with_offset(self._url, offset)
        async with self._session.get(
            url,
            headers={"User-Agent": "Home Assistant Kreis Steinfurt integration"},
        ) as response:
            response.raise_for_status()
            return await response.text()



def _url_with_offset(url: str, offset: int) -> str:
    """Return a source URL with its pagination offset replaced."""
    parsed = urlsplit(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["ttk0_offset"] = str(offset)
    return urlunsplit(parsed._replace(query=urlencode(query)))
