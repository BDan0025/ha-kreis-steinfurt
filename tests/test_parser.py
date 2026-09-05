"""Tests for the incident-list parser."""

from datetime import datetime
from pathlib import Path
import sys
import types

package = types.ModuleType("custom_components.kreis_steinfurt")
package.__path__ = [str(Path(__file__).parents[1] / "custom_components" / "kreis_steinfurt")]
sys.modules.setdefault("custom_components.kreis_steinfurt", package)
from custom_components.kreis_steinfurt.parser import parse_einsaetze


def test_parse_einsaetze() -> None:
    """All fields are read from the public list markup."""
    html = (Path(__file__).parent / "sample_page.html").read_text(encoding="utf-8")

    einsaetze = parse_einsaetze(html)

    assert len(einsaetze) == 2
    assert einsaetze[0].einsatznr == "26058928"
    assert einsaetze[0].einsatzart == "Drehleiter"
    assert einsaetze[0].ort == "Westerkappeln"
    assert einsaetze[0].beginn == datetime(2026, 9, 5, 15, 5)
    assert einsaetze[0].zustand == "laufend"


def test_parse_einsaetze_returns_empty_list_without_rows() -> None:
    """A valid response without entries is not an error."""
    assert parse_einsaetze("<html><body></body></html>") == []
