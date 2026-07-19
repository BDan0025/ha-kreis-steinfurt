"""HTTP client for Kreis Steinfurt."""

from __future__ import annotations

import logging

from aiohttp import ClientSession

from .const import SOURCE_URL
from .parser import parse_einsaetze

_LOGGER = logging.getLogger(__name__)


client = KreisSteinfurtClient(
    session,
    SOURCE_URL,
)