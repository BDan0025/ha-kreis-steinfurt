"""Persistent incident history for configurable entity retention."""

from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    RETENTION_30_DAYS,
    RETENTION_48_HOURS,
    RETENTION_7_DAYS,
    RETENTION_NEVER,
)
from .models import Einsatz

_STORAGE_VERSION = 1

_RETENTION_PERIODS = {
    RETENTION_48_HOURS: timedelta(hours=48),
    RETENTION_7_DAYS: timedelta(days=7),
    RETENTION_30_DAYS: timedelta(days=30),
}


class EinsatzHistory:
    """Keep incident data while a configured retention period is active."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        """Initialize history storage for one config entry."""
        self._store = Store[dict[str, Any]](
            hass,
            _STORAGE_VERSION,
            f"{DOMAIN}.{entry_id}.history",
        )
        self._einsaetze: dict[str, Einsatz] = {}

    async def async_load(self) -> None:
        """Load previously seen incidents."""
        data = await self._store.async_load() or {}
        for item in data.get("einsaetze", []):
            try:
                einsatz = Einsatz.from_dict(item)
            except (KeyError, TypeError, ValueError):
                continue
            self._einsaetze[einsatz.einsatznr] = einsatz

    async def async_update(self, einsaetze: list[Einsatz], retention: str) -> None:
        """Save new or changed incidents and remove expired records."""
        changed = False
        now = dt_util.utcnow()
        for einsatz in einsaetze:
            previous = self._einsaetze.get(einsatz.einsatznr)
            stored = self._with_history(previous, einsatz, now)
            if previous != stored:
                self._einsaetze[einsatz.einsatznr] = stored
                changed = True

        if self._prune(retention):
            changed = True

        if changed:
            await self._store.async_save(
                {"einsaetze": [einsatz.as_dict() for einsatz in self._einsaetze.values()]}
            )

    @staticmethod
    def _with_history(
        previous: Einsatz | None,
        current: Einsatz,
        now,
    ) -> Einsatz:
        """Return source data enriched with lifecycle timestamps."""
        if previous is None:
            return replace(
                current,
                erstmals_gesehen=now,
                letzte_aenderung=now,
            )

        source_changed = _source_fields_changed(previous, current)

        return replace(
            current,
            erstmals_gesehen=previous.erstmals_gesehen or now,
            letzte_aenderung=(
                now if source_changed or previous.letzte_aenderung is None else previous.letzte_aenderung
            ),
        )

    def retained_einsaetze(self, retention: str) -> list[Einsatz]:
        """Return incidents still covered by the configured retention period."""
        self._prune(retention)
        return list(self._einsaetze.values())

    def get(self, einsatznr: str, retention: str) -> Einsatz | None:
        """Return a retained incident by its published number."""
        self._prune(retention)
        return self._einsaetze.get(einsatznr)

    def _prune(self, retention: str) -> bool:
        """Drop incidents outside the configured period."""
        if retention == RETENTION_NEVER:
            return False

        period = _RETENTION_PERIODS.get(retention, _RETENTION_PERIODS[RETENTION_48_HOURS])
        cutoff = dt_util.now().replace(tzinfo=None) - period
        retained = {
            einsatznr: einsatz
            for einsatznr, einsatz in self._einsaetze.items()
            if einsatz.beginn >= cutoff
        }
        if len(retained) == len(self._einsaetze):
            return False

        self._einsaetze = retained
        return True
def _source_fields_changed(previous: Einsatz, current: Einsatz) -> bool:
    """Compare only values supplied by the public incident source."""
    return any(
        getattr(previous, field) != getattr(current, field)
        for field in (
            "einsatzart",
            "ort",
            "beginn",
            "zustand",
            "strasse",
            "sachverhalt",
        )
    )
