"""Sensor platform for Kreis Steinfurt."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KreisSteinfurtCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kreis Steinfurt sensors."""

    coordinator: KreisSteinfurtCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            KreisSteinfurtStatusSensor(coordinator, entry.entry_id),
        ]
    )


class KreisSteinfurtStatusSensor(
    CoordinatorEntity[KreisSteinfurtCoordinator],
    SensorEntity,
):
    """Status sensor for Kreis Steinfurt."""

    _attr_has_entity_name = True
    _attr_name = "Einsätze (48 h)"
    _attr_icon = "mdi:fire-truck"

    def __init__(
        self,
        coordinator: KreisSteinfurtCoordinator,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"kreis_steinfurt_einsaetze_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the number of incidents."""
        if self.coordinator.data is None:
            return 0

        return len(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict:
        """Return sensor attributes."""

        einsaetze = self.coordinator.data or []

        laufende_einsaetze = [
            einsatz for einsatz in einsaetze
            if einsatz.zustand.casefold() != "abgeschlossen"
        ]

        return {
            "einsatzanzahl_letzte_48_stunden": len(einsaetze),
            "laufende_einsaetze": len(laufende_einsaetze),
            "einsatznummern": [
                e.einsatznr for e in einsaetze
            ],
            "orte": [
                e.ort for e in einsaetze
            ],
            "einsaetze": [
                {
                    "einsatznr": e.einsatznr,
                    "einsatzart": e.einsatzart,
                    "ort": e.ort,
                    "beginn": e.beginn.isoformat(),
                    "zustand": e.zustand,
                }
                for e in einsaetze
            ],
        }
