"""Sensor platform for Kreis Steinfurt."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import KreisSteinfurtCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kreis Steinfurt sensors."""

    coordinator: KreisSteinfurtCoordinator = entry.runtime_data

    async_add_entities(
        [
            KreisSteinfurtStatusSensor(coordinator),
        ]
    )


class KreisSteinfurtStatusSensor(
    CoordinatorEntity[KreisSteinfurtCoordinator],
    SensorEntity,
):
    """Status sensor for Kreis Steinfurt."""

    _attr_has_entity_name = True
    _attr_name = "Status"
    _attr_unique_id = "kreis_steinfurt_status"
    _attr_icon = "mdi:fire-truck"

    def __init__(
        self,
        coordinator: KreisSteinfurtCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

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

        return {
            "aktive_einsaetze": len(einsaetze),
            "einsatznummern": [
                e.einsatznr for e in einsaetze
            ],
            "orte": [
                e.ort for e in einsaetze
            ],
        }