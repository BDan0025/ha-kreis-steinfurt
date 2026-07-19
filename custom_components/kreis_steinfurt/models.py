"""Data models for Kreis Steinfurt."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Einsatz:
    """Represents one incident from the dispatch page."""

    einsatznr: str
    einsatzart: str
    ort: str
    beginn: datetime
    zustand: str