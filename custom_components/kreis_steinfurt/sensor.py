"""Sensor platform for Kreis Steinfurt."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import KreisSteinfurtCoordinator
from .models import Einsatz


def _laufende_einsaetze(einsaetze: list[Einsatz]) -> list[Einsatz]:
    """Return entries that the source does not mark as finished."""
    return [
        einsatz
        for einsatz in einsaetze
        if einsatz.zustand.casefold() != "abgeschlossen"
    ]


def _einsatz_attributes(einsatz: Einsatz) -> dict[str, str | None]:
    """Return the public attributes for an individual incident."""
    return {
        "einsatznummer": einsatz.einsatznr,
        "einsatzart": einsatz.einsatzart,
        "ort": einsatz.ort,
        "beginn": einsatz.beginn.strftime("%d.%m.%Y %H:%M"),
        "status": einsatz.zustand,
        "strasse": einsatz.strasse,
        "sachverhalt": einsatz.sachverhalt,
        "latitude": None,
        "longitude": None,
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up summary, city and individual-incident sensors."""
    coordinator: KreisSteinfurtCoordinator = hass.data[DOMAIN][entry.entry_id]
    known_incidents: set[str] = set()
    known_cities: set[str] = set()
    incident_entities: dict[str, KreisSteinfurtEinsatzSensor] = {}

    def _new_dynamic_entities() -> list[SensorEntity]:
        einsaetze = [
            einsatz
            for einsatz in coordinator.retained_einsaetze
            if einsatz.ort in coordinator.monitored_areas
        ]
        new_entities: list[SensorEntity] = []

        for einsatz in einsaetze:
            if einsatz.einsatznr not in known_incidents:
                known_incidents.add(einsatz.einsatznr)
                incident_entity = KreisSteinfurtEinsatzSensor(
                    coordinator,
                    entry.entry_id,
                    einsatz.einsatznr,
                )
                incident_entities[einsatz.einsatznr] = incident_entity
                new_entities.append(incident_entity)

            city_id = slugify(einsatz.ort)
            if city_id not in known_cities:
                known_cities.add(city_id)
                new_entities.append(KreisSteinfurtCitySensor(coordinator, entry.entry_id, einsatz.ort))

        return new_entities

    def _remove_expired_entities() -> None:
        """Remove entities once their configured retention has ended."""
        entity_registry = er.async_get(hass)
        for einsatznr, entity in tuple(incident_entities.items()):
            if coordinator.get_retained_einsatz(einsatznr) is not None:
                continue
            if entity.entity_id is not None:
                entity_registry.async_remove(entity.entity_id)
            incident_entities.pop(einsatznr)
            known_incidents.discard(einsatznr)

    def _cleanup_registry() -> None:
        """Remove retained incident entities no longer eligible after a restart."""
        entity_registry = er.async_get(hass)
        retained = [
            einsatz
            for einsatz in coordinator.retained_einsaetze
            if einsatz.ort in coordinator.monitored_areas
        ]
        incident_unique_ids = {
            f"{DOMAIN}_einsatz_{slugify(einsatz.einsatznr)}_{entry.entry_id}"
            for einsatz in retained
        }
        city_unique_ids = {
            f"{DOMAIN}_einsatzort_{slugify(einsatz.ort)}_{entry.entry_id}"
            for einsatz in retained
        }

        for registry_entry in er.async_entries_for_config_entry(
            entity_registry,
            entry.entry_id,
        ):
            if registry_entry.unique_id.startswith(f"{DOMAIN}_einsatz_"):
                if registry_entry.unique_id not in incident_unique_ids:
                    entity_registry.async_remove(registry_entry.entity_id)
            elif registry_entry.unique_id.startswith(f"{DOMAIN}_einsatzort_"):
                if registry_entry.unique_id not in city_unique_ids:
                    entity_registry.async_remove(registry_entry.entity_id)

    _cleanup_registry()

    async_add_entities(
        [
            KreisSteinfurtEinsaetzeSensor(coordinator, entry.entry_id),
            KreisSteinfurtLaufendeEinsaetzeSensor(coordinator, entry.entry_id),
            KreisSteinfurtLetzte24StundenSensor(coordinator, entry.entry_id),
            *_new_dynamic_entities(),
        ]
    )

    def _async_add_new_entities() -> None:
        _remove_expired_entities()
        if new_entities := _new_dynamic_entities():
            async_add_entities(new_entities)

    entry.async_on_unload(coordinator.async_add_listener(_async_add_new_entities))


class _KreisSteinfurtCoordinatorSensor(
    CoordinatorEntity[KreisSteinfurtCoordinator],
    SensorEntity,
):
    """Base class for all Kreis Steinfurt coordinator sensors."""

    _attr_icon = "mdi:fire-truck"

    @property
    def _einsaetze(self) -> list[Einsatz]:
        """Return current incidents in the configured monitoring area."""
        return [
            einsatz
            for einsatz in self.coordinator.data or []
            if einsatz.ort in self.coordinator.monitored_areas
        ]


class KreisSteinfurtEinsaetzeSensor(_KreisSteinfurtCoordinatorSensor):
    """Count all incidents published for the last 48 hours."""

    _attr_name = "Kreis Steinfurt Einsätze"
    _attr_suggested_object_id = "kreis_steinfurt_einsaetze"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the summary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsaetze_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the number of published incidents."""
        return len(self._einsaetze)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return incident details for cards and automations."""
        return {
            "einsatzanzahl_letzte_48_stunden": len(self._einsaetze),
            "laufende_einsaetze": len(_laufende_einsaetze(self._einsaetze)),
            "einsatznummern": [einsatz.einsatznr for einsatz in self._einsaetze],
            "orte": sorted({einsatz.ort for einsatz in self._einsaetze}),
            "einsaetze": [_einsatz_attributes(einsatz) for einsatz in self._einsaetze],
        }


class KreisSteinfurtLaufendeEinsaetzeSensor(_KreisSteinfurtCoordinatorSensor):
    """Count incidents that are not marked as completed."""

    _attr_name = "Kreis Steinfurt laufende Einsätze"
    _attr_suggested_object_id = "kreis_steinfurt_laufende_einsaetze"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the running-incident sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_laufende_einsaetze_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the number of incidents that are not completed."""
        return len(_laufende_einsaetze(self._einsaetze))

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the currently running incidents."""
        laufende = _laufende_einsaetze(self._einsaetze)
        return {"einsaetze": [_einsatz_attributes(einsatz) for einsatz in laufende]}


class KreisSteinfurtLetzte24StundenSensor(_KreisSteinfurtCoordinatorSensor):
    """Count incidents whose start time is within the last 24 hours."""

    _attr_name = "Kreis Steinfurt Einsätze letzte 24 Stunden"
    _attr_suggested_object_id = "kreis_steinfurt_einsaetze_letzte_24_stunden"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the 24-hour sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsaetze_letzte_24_stunden_{entry_id}"

    @property
    def _letzte_24_stunden(self) -> list[Einsatz]:
        """Return incidents started in the last 24 hours."""
        since = datetime.now() - timedelta(hours=24)
        return [einsatz for einsatz in self._einsaetze if einsatz.beginn >= since]

    @property
    def native_value(self) -> int:
        """Return the number of incidents in the last 24 hours."""
        return len(self._letzte_24_stunden)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the incidents in the selected time period."""
        return {"einsaetze": [_einsatz_attributes(einsatz) for einsatz in self._letzte_24_stunden]}


class KreisSteinfurtCitySensor(_KreisSteinfurtCoordinatorSensor):
    """Count incidents for one city."""

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str, city: str) -> None:
        """Initialize a city sensor."""
        super().__init__(coordinator)
        self._city = city
        city_id = slugify(city)
        self._attr_name = f"Kreis Steinfurt Einsätze {city}"
        self._attr_suggested_object_id = f"kreis_steinfurt_einsaetze_{city_id}"
        self._attr_unique_id = f"{DOMAIN}_einsatzort_{city_id}_{entry_id}"

    @property
    def _city_einsaetze(self) -> list[Einsatz]:
        """Return the incidents belonging to this city."""
        return [einsatz for einsatz in self._einsaetze if einsatz.ort == self._city]

    @property
    def native_value(self) -> int:
        """Return the number of incidents in this city."""
        return len(self._city_einsaetze)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the city's incidents and running count."""
        einsaetze = self._city_einsaetze
        return {
            "ort": self._city,
            "laufende_einsaetze": len(_laufende_einsaetze(einsaetze)),
            "einsaetze": [_einsatz_attributes(einsatz) for einsatz in einsaetze],
        }


class KreisSteinfurtEinsatzSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose one published incident as its own sensor."""

    def __init__(
        self,
        coordinator: KreisSteinfurtCoordinator,
        entry_id: str,
        einsatznr: str,
    ) -> None:
        """Initialize an incident sensor."""
        super().__init__(coordinator)
        self._einsatznr = einsatznr
        incident_id = slugify(einsatznr)
        self._attr_name = f"Kreis Steinfurt Einsatz {einsatznr}"
        self._attr_suggested_object_id = f"kreis_steinfurt_einsatz_{incident_id}"
        self._attr_unique_id = f"{DOMAIN}_einsatz_{incident_id}_{entry_id}"

    @property
    def _einsatz(self) -> Einsatz | None:
        """Return this sensor's incident while its retention is active."""
        return self.coordinator.get_retained_einsatz(self._einsatznr)

    @property
    def available(self) -> bool:
        """Mark the entity unavailable after its incident leaves the 48-hour list."""
        return super().available and self._einsatz is not None

    @property
    def native_value(self) -> str | None:
        """Return the published status."""
        if (einsatz := self._einsatz) is None:
            return None
        return einsatz.zustand

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return all data published for this incident."""
        if (einsatz := self._einsatz) is None:
            return {"einsatznummer": self._einsatznr}
        return _einsatz_attributes(einsatz)
