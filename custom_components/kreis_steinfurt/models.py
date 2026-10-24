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
        )
