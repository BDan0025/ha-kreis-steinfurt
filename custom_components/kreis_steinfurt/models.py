"""Data models for Kreis Steinfurt."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Einsatz:
    """Represents one incident."""

    einsatznr: str
    einsatzart: str
    ort: str
    beginn: datetime
    zustand: str

    strasse: str | None = None
    sachverhalt: str | None = None
    erstmals_gesehen: datetime | None = None
    letzte_aenderung: datetime | None = None
    abgeschlossen_am: datetime | None = None

    def as_dict(self) -> dict[str, str | None]:
        """Serialize the incident for Home Assistant storage."""
        return {
            "einsatznr": self.einsatznr,
            "einsatzart": self.einsatzart,
            "ort": self.ort,
            "beginn": self.beginn.isoformat(),
            "zustand": self.zustand,
            "strasse": self.strasse,
            "sachverhalt": self.sachverhalt,
            "erstmals_gesehen": _datetime_to_string(self.erstmals_gesehen),
            "letzte_aenderung": _datetime_to_string(self.letzte_aenderung),
            "abgeschlossen_am": _datetime_to_string(self.abgeschlossen_am),
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | None]) -> "Einsatz":
        """Restore a stored incident."""
        return cls(
            einsatznr=str(data["einsatznr"]),
            einsatzart=str(data["einsatzart"]),
            ort=str(data["ort"]),
            beginn=datetime.fromisoformat(str(data["beginn"])),
            zustand=str(data["zustand"]),
            strasse=data.get("strasse"),
            sachverhalt=data.get("sachverhalt"),
            erstmals_gesehen=_datetime_from_string(data.get("erstmals_gesehen")),
            letzte_aenderung=_datetime_from_string(data.get("letzte_aenderung")),
            abgeschlossen_am=_datetime_from_string(data.get("abgeschlossen_am")),
        )


def _datetime_to_string(value: datetime | None) -> str | None:
    """Serialize an optional datetime."""
    return value.isoformat() if value is not None else None


def _datetime_from_string(value: str | None) -> datetime | None:
    """Deserialize an optional datetime."""
    return datetime.fromisoformat(value) if value else None
