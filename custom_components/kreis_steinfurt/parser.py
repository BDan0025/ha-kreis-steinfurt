"""Parser for the public Kreis Steinfurt incident list."""

from __future__ import annotations

from datetime import datetime
from html.parser import HTMLParser

from .models import Einsatz


class _IncidentHTMLParser(HTMLParser):
    """Extract incident-row fields without third-party dependencies."""

    _FIELDS = {"type", "city", "beginn", "status", "operation"}

    def __init__(self) -> None:
        """Initialize the parser state."""
        super().__init__()
        self.rows: list[dict[str, str]] = []
        self._row: dict[str, str] | None = None
        self._field: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Start tracking a published incident row."""
        classes = set(dict(attrs).get("class", "").split())
        if tag == "li" and "kreisleitsystem-rows" in classes:
            self._row = {}
            self._field = None
        elif self._row is not None:
            field = next(iter(classes & self._FIELDS), None)
            if field is not None:
                self._field = field

    def handle_data(self, data: str) -> None:
        """Collect text belonging to the current field."""
        if self._row is not None and self._field is not None:
            self._row[self._field] = self._row.get(self._field, "") + data

    def handle_endtag(self, tag: str) -> None:
        """Finish an incident row."""
        if tag == "li" and self._row is not None:
            self.rows.append(self._row)
            self._row = None
            self._field = None


def _value(row: dict[str, str], field: str, label: str = "") -> str:
    """Normalize a required incident field."""
    try:
        value = row[field].strip().removeprefix(label).strip().lstrip("\ufeff")
    except KeyError as err:
        raise ValueError(f"Missing {field} in incident row") from err
    return value


def parse_einsaetze(html: str) -> list[Einsatz]:
    """Parse all incident rows from the HTML response."""
    parser = _IncidentHTMLParser()
    parser.feed(html)
    parser.close()

    einsaetze: list[Einsatz] = []
    for row in parser.rows:
        beginn = _value(row, "beginn", "Beginn:")
        einsaetze.append(
            Einsatz(
                einsatznr=_value(row, "operation", "Einsatznr.:"),
                einsatzart=_value(row, "type"),
                ort=_value(row, "city", "Ort:"),
                beginn=datetime.strptime(beginn, "%Y-%m-%d %H:%M:%S"),
                zustand=_value(row, "status", "Zustand:"),
            )
        )

    return einsaetze
