"""Sensor platform for Kreis Steinfurt."""

from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util
from homeassistant.util import slugify

from .const import CITY_COORDINATES, DOMAIN, MAP_LOCATION_SOURCE
from .coordinator import KreisSteinfurtCoordinator
from .models import Einsatz

_MAX_LIST_ITEMS = 50
_MAX_CITY_HISTORY_ITEMS = 25
_LAST_INCIDENT_MAP_ITEMS = 10


def _laufende_einsaetze(einsaetze: list[Einsatz]) -> list[Einsatz]:
    """Return entries that the source does not mark as finished."""
    return [
        einsatz
        for einsatz in einsaetze
        if einsatz.zustand.casefold() != "abgeschlossen"
    ]


def _einsatz_attributes(einsatz: Einsatz, kartenposition: str) -> dict[str, object]:
    """Return the public attributes for an individual incident."""
    city_coordinates = CITY_COORDINATES.get(einsatz.ort)
    latitude = longitude = None
    location_source = "nicht verfügbar"
    if kartenposition != MAP_LOCATION_SOURCE and city_coordinates:
        latitude, longitude = city_coordinates
        location_source = "stadtmittelpunkt"
    return {
        "einsatznummer": einsatz.einsatznr,
        "einsatzart": einsatz.einsatzart,
        "ort": einsatz.ort,
        "beginn": einsatz.beginn.strftime("%d.%m.%Y %H:%M"),
        "beginn_iso": einsatz.beginn.isoformat(),
        "status": einsatz.zustand,
        "strasse": einsatz.strasse,
        "sachverhalt": einsatz.sachverhalt,
        "latitude": latitude,
        "longitude": longitude,
        "kartenposition": location_source,
        "erstmals_gesehen": _datetime_to_iso(einsatz.erstmals_gesehen),
        "letzte_aenderung": _datetime_to_iso(einsatz.letzte_aenderung),
    }


def _einsatz_list_attributes(einsatz: Einsatz) -> dict[str, object]:
    """Return compact incident data suitable for list sensor attributes."""
    return {
        "einsatznummer": einsatz.einsatznr,
        "einsatzart": einsatz.einsatzart,
        "ort": einsatz.ort,
        "beginn": einsatz.beginn.strftime("%d.%m.%Y %H:%M"),
        "beginn_iso": einsatz.beginn.isoformat(),
        "status": einsatz.zustand,
    }


def _compact_list(
    einsaetze: list[Einsatz],
    max_items: int = _MAX_LIST_ITEMS,
) -> list[dict[str, object]]:
    """Return at most the newest incidents without oversized attributes."""
    newest = sorted(einsaetze, key=lambda einsatz: einsatz.beginn, reverse=True)
    return [_einsatz_list_attributes(einsatz) for einsatz in newest[:max_items]]


def _datetime_to_iso(value: datetime | None) -> str | None:
    """Return an optional datetime as an ISO value."""
    return value.isoformat() if value is not None else None


def _einsaetze_in_zeitraum(einsaetze: list[Einsatz], days: int) -> list[Einsatz]:
    """Return incidents today or within the previous number of days."""
    now = dt_util.now().replace(tzinfo=None)
    since = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if days > 1:
        since = now - timedelta(days=days)
    return [einsatz for einsatz in einsaetze if einsatz.beginn >= since]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up summary, city and individual-incident sensors."""
    coordinator: KreisSteinfurtCoordinator = hass.data[DOMAIN][entry.entry_id]
    known_incidents: set[str] = set()
    incident_entities: dict[str, KreisSteinfurtEinsatzSensor] = {}
    letzter_einsatz_sensor = KreisSteinfurtLetzterEinsatzSensor(
        coordinator,
        entry.entry_id,
    )
    city_last_incident_entities = [
        KreisSteinfurtCityLastIncidentSensor(coordinator, entry.entry_id, city)
        for city in sorted(coordinator.monitored_areas)
    ]
    last_incident_map_entities = [
        KreisSteinfurtLastIncidentMapSensor(coordinator, entry.entry_id, position)
        for position in range(1, _LAST_INCIDENT_MAP_ITEMS + 1)
    ]

    def _is_monitored(einsatz: Einsatz) -> bool:
        """Return whether an incident matches the configured options."""
        types = coordinator.monitored_incident_types
        return (
            einsatz.ort in coordinator.monitored_areas
            and (types is None or einsatz.einsatzart in types)
        )

    def _new_dynamic_entities() -> list[SensorEntity]:
        einsaetze = [
            einsatz
            for einsatz in coordinator.retained_einsaetze
            if _is_monitored(einsatz)
        ]
        new_entities: list[SensorEntity] = []

        for einsatz in einsaetze:
            if (
                coordinator.incident_entities_enabled
                and einsatz.einsatznr not in known_incidents
            ):
                known_incidents.add(einsatz.einsatznr)
                incident_entity = KreisSteinfurtEinsatzSensor(
                    coordinator,
                    entry.entry_id,
                    einsatz.einsatznr,
                )
                incident_entities[einsatz.einsatznr] = incident_entity
                new_entities.append(incident_entity)

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
        incident_unique_ids = {
            f"{DOMAIN}_einsatz_{slugify(einsatz.einsatznr)}_{entry.entry_id}"
            for einsatz in coordinator.retained_einsaetze
            if _is_monitored(einsatz)
        }
        city_unique_ids = {
            f"{DOMAIN}_einsatzort_{slugify(city)}_{entry.entry_id}"
            for city in coordinator.monitored_areas
        }
        city_last_incident_unique_ids = {
            f"{DOMAIN}_letzter_einsatzort_{slugify(city)}_{entry.entry_id}"
            for city in coordinator.monitored_areas
        }

        for registry_entry in er.async_entries_for_config_entry(
            entity_registry,
            entry.entry_id,
        ):
            if registry_entry.unique_id.startswith(f"{DOMAIN}_einsatz_"):
                if (
                    not coordinator.incident_entities_enabled
                    or registry_entry.unique_id not in incident_unique_ids
                ):
                    entity_registry.async_remove(registry_entry.entity_id)
            elif registry_entry.unique_id.startswith(f"{DOMAIN}_einsatzort_"):
                if (
                    not coordinator.city_summaries_enabled
                    or registry_entry.unique_id not in city_unique_ids
                ):
                    entity_registry.async_remove(registry_entry.entity_id)
            elif registry_entry.unique_id.startswith(f"{DOMAIN}_letzter_einsatzort_"):
                if (
                    not coordinator.city_last_incident_enabled
                    or registry_entry.unique_id not in city_last_incident_unique_ids
                ):
                    entity_registry.async_remove(registry_entry.entity_id)

    _cleanup_registry()

    async_add_entities(
        [
            KreisSteinfurtEinsaetzeSensor(coordinator, entry.entry_id),
            letzter_einsatz_sensor,
            KreisSteinfurtLaufendeEinsaetzeSensor(coordinator, entry.entry_id),
            KreisSteinfurtLetzte24StundenSensor(coordinator, entry.entry_id),
            KreisSteinfurtHistorieSensor(coordinator, entry.entry_id),
            KreisSteinfurtEinsaetzeHeuteSensor(coordinator, entry.entry_id),
            KreisSteinfurtEinsaetzeLetzte7TageSensor(coordinator, entry.entry_id),
            KreisSteinfurtEinsatzartenSensor(coordinator, entry.entry_id),
            KreisSteinfurtAbrufintervallSensor(coordinator, entry.entry_id),
            KreisSteinfurtQuellseitenSensor(coordinator, entry.entry_id),
            KreisSteinfurtQuellEinsatzanzahlSensor(coordinator, entry.entry_id),
            KreisSteinfurtLetzteAktualisierungSensor(coordinator, entry.entry_id),
            *last_incident_map_entities,
            *(
                [
                    KreisSteinfurtCitySensor(coordinator, entry.entry_id, city)
                    for city in sorted(coordinator.monitored_areas)
                ]
                if coordinator.city_summaries_enabled
                else []
            ),
            *(
                city_last_incident_entities
                if coordinator.city_last_incident_enabled
                else []
            ),
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
            self.coordinator.get_retained_einsatz(einsatz.einsatznr) or einsatz
            for einsatz in self.coordinator.data or []
            if self._is_monitored(einsatz)
        ]

    @property
    def _historie(self) -> list[Einsatz]:
        """Return retained incidents in the configured monitoring scope."""
        return [
            einsatz
            for einsatz in self.coordinator.retained_einsaetze
            if self._is_monitored(einsatz)
        ]

    def _is_monitored(self, einsatz: Einsatz) -> bool:
        """Return whether an incident matches the selected area and type."""
        types = self.coordinator.monitored_incident_types
        return (
            einsatz.ort in self.coordinator.monitored_areas
            and (types is None or einsatz.einsatzart in types)
        )


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
        attributes: dict[str, object] = {
            "einsatzanzahl_letzte_48_stunden": len(self._einsaetze),
            "laufende_einsaetze": len(_laufende_einsaetze(self._einsaetze)),
            "einsatznummern": [einsatz.einsatznr for einsatz in self._einsaetze],
            "orte": sorted({einsatz.ort for einsatz in self._einsaetze}),
        }
        if self.coordinator.list_attributes_enabled:
            attributes["einsaetze"] = _compact_list(self._einsaetze)
        return attributes


class KreisSteinfurtLetzterEinsatzSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose the newest incident through one stable entity ID."""

    _attr_name = "Kreis Steinfurt letzter Einsatz"
    _attr_suggested_object_id = "kreis_steinfurt_letzter_einsatz"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the latest-incident detail sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_letzter_einsatz_{entry_id}"

    @property
    def _letzter_einsatz(self) -> Einsatz | None:
        """Return the latest incident from the current source data."""
        return max(self._einsaetze, key=lambda einsatz: einsatz.beginn, default=None)

    @property
    def available(self) -> bool:
        """Make the entity unavailable when no incident is currently published."""
        return super().available and self._letzter_einsatz is not None

    @property
    def native_value(self) -> str | None:
        """Return the status of the latest incident."""
        if (einsatz := self._letzter_einsatz) is None:
            return None
        return einsatz.zustand

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return complete details of the latest incident."""
        if (einsatz := self._letzter_einsatz) is None:
            return {}
        return _einsatz_attributes(einsatz, self.coordinator.kartenposition)


class KreisSteinfurtLaufendeEinsaetzeSensor(_KreisSteinfurtCoordinatorSensor):
    """Count incidents that are not marked as completed."""

    _attr_name = "Kreis Steinfurt laufende Einsätze"
    _attr_suggested_object_id = "kreis_steinfurt_laufende_einsatze"

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
        if self.coordinator.list_attributes_enabled:
            return {"einsaetze": _compact_list(laufende)}
        return {}


class KreisSteinfurtLetzte24StundenSensor(_KreisSteinfurtCoordinatorSensor):
    """Count incidents whose start time is within the last 24 hours."""

    _attr_name = "Kreis Steinfurt Einsätze letzte 24 Stunden"
    _attr_suggested_object_id = "kreis_steinfurt_einsatze_letzte_24_stunden"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the 24-hour sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsaetze_letzte_24_stunden_{entry_id}"

    @property
    def _letzte_24_stunden(self) -> list[Einsatz]:
        """Return incidents started in the last 24 hours."""
        since = dt_util.now().replace(tzinfo=None) - timedelta(hours=24)
        return [einsatz for einsatz in self._einsaetze if einsatz.beginn >= since]

    @property
    def native_value(self) -> int:
        """Return the number of incidents in the last 24 hours."""
        return len(self._letzte_24_stunden)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the incidents in the selected time period."""
        if self.coordinator.list_attributes_enabled:
            return {"einsaetze": _compact_list(self._letzte_24_stunden)}
        return {}


class KreisSteinfurtHistorieSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose retained incidents for dashboard lists and automations."""

    _attr_name = "Kreis Steinfurt Einsatzhistorie"
    _attr_suggested_object_id = "kreis_steinfurt_einsatzhistorie"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the history sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsatzhistorie_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return number of incidents retained in the selected scope."""
        return len(self._historie)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return retained incidents with their lifecycle details."""
        attributes: dict[str, object] = {
            "aufbewahrung": self.coordinator.retention,
            "einsatzarten": self.coordinator.known_incident_types,
            "einsatzanzahl": len(self._historie),
        }
        if self.coordinator.list_attributes_enabled:
            attributes["einsaetze"] = _compact_list(self._historie)
        return attributes


class _KreisSteinfurtZeitraumSensor(_KreisSteinfurtCoordinatorSensor):
    """Base sensor for retained-incident statistics."""

    _days: int

    @property
    def _zeitraum_einsaetze(self) -> list[Einsatz]:
        """Return retained incidents in the sensor period."""
        return _einsaetze_in_zeitraum(self._historie, self._days)

    @property
    def native_value(self) -> int:
        """Return the number of incidents in the sensor period."""
        return len(self._zeitraum_einsaetze)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return totals per municipality and incident type."""
        einsaetze = self._zeitraum_einsaetze
        by_city = {
            city: len([einsatz for einsatz in einsaetze if einsatz.ort == city])
            for city in sorted({einsatz.ort for einsatz in einsaetze})
        }
        by_type = {
            incident_type: len(
                [einsatz for einsatz in einsaetze if einsatz.einsatzart == incident_type]
            )
            for incident_type in sorted({einsatz.einsatzart for einsatz in einsaetze})
        }
        return {
            "gesamt": len(einsaetze),
            "nach_ort": by_city,
            "nach_einsatzart": by_type,
        }


class KreisSteinfurtEinsaetzeHeuteSensor(_KreisSteinfurtZeitraumSensor):
    """Count retained incidents that started today (last 24 hours)."""

    _attr_name = "Kreis Steinfurt Einsätze heute"
    _attr_suggested_object_id = "kreis_steinfurt_einsatze_heute"
    _days = 1

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the daily statistics sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsaetze_heute_{entry_id}"


class KreisSteinfurtEinsaetzeLetzte7TageSensor(_KreisSteinfurtZeitraumSensor):
    """Count retained incidents from the last seven days."""

    _attr_name = "Kreis Steinfurt Einsätze letzte 7 Tage"
    _attr_suggested_object_id = "kreis_steinfurt_einsatze_letzte_7_tage"
    _days = 7

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the weekly statistics sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsaetze_letzte_7_tage_{entry_id}"


class KreisSteinfurtEinsatzartenSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose observed incident types and counts for filters and dashboards."""

    _attr_name = "Kreis Steinfurt Einsatzarten"
    _attr_suggested_object_id = "kreis_steinfurt_einsatzarten"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the incident-type overview sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsatzarten_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the number of incident types currently known."""
        return len(self.coordinator.known_incident_types)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return per-type totals for current and retained incidents."""
        return {
            "einsatzarten": {
                incident_type: {
                    "aktuell": len(
                        [einsatz for einsatz in self._einsaetze if einsatz.einsatzart == incident_type]
                    ),
                    "historie": len(
                        [einsatz for einsatz in self._historie if einsatz.einsatzart == incident_type]
                    ),
                }
                for incident_type in self.coordinator.known_incident_types
            }
        }


class KreisSteinfurtAbrufintervallSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose the configured source polling interval."""

    _attr_name = "Kreis Steinfurt Abrufintervall"
    _attr_suggested_object_id = "kreis_steinfurt_abrufintervall"
    _attr_native_unit_of_measurement = "s"
    _attr_icon = "mdi:timer-outline"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the polling interval sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_abrufintervall_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the configured polling interval in seconds."""
        return self.coordinator.scan_interval


class KreisSteinfurtQuellseitenSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose the number of pages currently returned by the source."""

    _attr_name = "Kreis Steinfurt Quellseiten"
    _attr_suggested_object_id = "kreis_steinfurt_quellseiten"
    _attr_icon = "mdi:book-open-page-variant-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the source-page diagnostic sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_quellseiten_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the current number of source pages."""
        return self.coordinator.source_page_count

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return details about the complete source list."""
        return {
            "einsaetze_auf_der_quelle": self.coordinator.source_incident_count,
            "abgerufene_einsaetze": len(self.coordinator.data or []),
        }


class KreisSteinfurtQuellEinsatzanzahlSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose the total number of incidents published by the source."""

    _attr_name = "Kreis Steinfurt Einsätze auf der Quelle"
    _attr_suggested_object_id = "kreis_steinfurt_einsaetze_auf_der_quelle"
    _attr_icon = "mdi:database-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the source-count diagnostic sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_einsaetze_auf_der_quelle_{entry_id}"

    @property
    def native_value(self) -> int:
        """Return the total count the source reports."""
        return self.coordinator.source_incident_count

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the source-page count and successfully read entries."""
        return {
            "quellseiten": self.coordinator.source_page_count,
            "abgerufene_einsaetze": len(self.coordinator.data or []),
        }


class KreisSteinfurtLetzteAktualisierungSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose when the integration last completed a source refresh."""

    _attr_name = "Kreis Steinfurt letzte Aktualisierung"
    _attr_suggested_object_id = "kreis_steinfurt_letzte_aktualisierung"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:clock-check-outline"

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str) -> None:
        """Initialize the refresh-time diagnostic sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_letzte_aktualisierung_{entry_id}"

    @property
    def native_value(self) -> datetime | None:
        """Return the last successful full refresh time."""
        return self.coordinator.last_update_success_time


class KreisSteinfurtCitySensor(_KreisSteinfurtCoordinatorSensor):
    """Count incidents for one city."""

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str, city: str) -> None:
        """Initialize a city sensor."""
        super().__init__(coordinator)
        self._city = city
        city_id = slugify(city)
        self._attr_name = f"Kreis Steinfurt Einsätze {city}"
        self._attr_suggested_object_id = f"kreis_steinfurt_einsatze_{city_id}"
        self._attr_unique_id = f"{DOMAIN}_einsatzort_{city_id}_{entry_id}"

    @property
    def _city_einsaetze(self) -> list[Einsatz]:
        """Return the incidents belonging to this city."""
        return [einsatz for einsatz in self._einsaetze if einsatz.ort == self._city]

    @property
    def _city_historie(self) -> list[Einsatz]:
        """Return retained incidents belonging to this city."""
        return [einsatz for einsatz in self._historie if einsatz.ort == self._city]

    @property
    def native_value(self) -> int:
        """Return the number of incidents in this city."""
        return len(self._city_einsaetze)

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return the city's incidents and running count."""
        einsaetze = self._city_einsaetze
        historie = self._city_historie
        attributes: dict[str, object] = {
            "ort": self._city,
            "laufende_einsaetze": len(_laufende_einsaetze(einsaetze)),
            "einsatzanzahl_heute": len(_einsaetze_in_zeitraum(historie, 1)),
            "einsatzanzahl_letzte_7_tage": len(_einsaetze_in_zeitraum(historie, 7)),
        }
        if self.coordinator.list_attributes_enabled:
            attributes["einsaetze"] = _compact_list(einsaetze)
            attributes["historie"] = _compact_list(historie, _MAX_CITY_HISTORY_ITEMS)
        return attributes


class KreisSteinfurtCityLastIncidentSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose the latest retained incident for one selected city."""

    def __init__(self, coordinator: KreisSteinfurtCoordinator, entry_id: str, city: str) -> None:
        """Initialize a stable latest-incident sensor for one city."""
        super().__init__(coordinator)
        self._city = city
        city_id = slugify(city)
        self._attr_name = f"Kreis Steinfurt letzter Einsatz {city}"
        self._attr_suggested_object_id = f"kreis_steinfurt_letzter_einsatz_{city_id}"
        self._attr_unique_id = f"{DOMAIN}_letzter_einsatzort_{city_id}_{entry_id}"

    @property
    def _letzter_einsatz(self) -> Einsatz | None:
        """Return the newest retained incident for this city."""
        return max(
            (einsatz for einsatz in self._historie if einsatz.ort == self._city),
            key=lambda einsatz: einsatz.beginn,
            default=None,
        )

    @property
    def native_value(self) -> str | None:
        """Return the source status of the city's latest retained incident."""
        if (einsatz := self._letzter_einsatz) is None:
            return None
        return einsatz.zustand

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return details for the city's latest retained incident."""
        if (einsatz := self._letzter_einsatz) is None:
            return {"ort": self._city, "status": "kein Einsatz gespeichert"}
        attributes = _einsatz_attributes(einsatz, self.coordinator.kartenposition)
        return attributes


class KreisSteinfurtLastIncidentMapSensor(_KreisSteinfurtCoordinatorSensor):
    """Expose one of the ten newest retained incidents as a map marker."""

    _attr_icon = "mdi:map-marker"

    def __init__(
        self,
        coordinator: KreisSteinfurtCoordinator,
        entry_id: str,
        position: int,
    ) -> None:
        """Initialize a stable marker slot for the latest-incidents map."""
        super().__init__(coordinator)
        self._position = position
        self._attr_name = str(position)
        self._attr_suggested_object_id = f"kreis_steinfurt_kartenpunkt_{position}"
        self._attr_unique_id = (
            f"{DOMAIN}_kartenpunkt_letzter_einsatz_{position}_{entry_id}"
        )

    @property
    def _einsatz(self) -> Einsatz | None:
        """Return the incident assigned to this marker slot."""
        einsaetze = sorted(
            self._historie,
            key=lambda einsatz: einsatz.beginn,
            reverse=True,
        )
        if len(einsaetze) < self._position:
            return None
        return einsaetze[self._position - 1]

    @property
    def available(self) -> bool:
        """Only expose markers for slots that contain an incident."""
        return super().available and self._einsatz is not None

    @property
    def native_value(self) -> str | None:
        """Return a concise map marker state."""
        if (einsatz := self._einsatz) is None:
            return None
        return einsatz.einsatzart

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return complete incident details including the map position."""
        if (einsatz := self._einsatz) is None:
            return {}
        attributes = _einsatz_attributes(einsatz, self.coordinator.kartenposition)
        attributes["position"] = self._position
        return attributes


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
        self._last_einsatz: Einsatz | None = coordinator.get_retained_einsatz(einsatznr)
        incident_id = slugify(einsatznr)
        self._attr_name = f"Kreis Steinfurt Einsatz {einsatznr}"
        self._attr_suggested_object_id = f"kreis_steinfurt_einsatz_{incident_id}"
        self._attr_unique_id = f"{DOMAIN}_einsatz_{incident_id}_{entry_id}"

    @property
    def _einsatz(self) -> Einsatz | None:
        """Return the retained incident or the last stable source snapshot."""
        if einsatz := self.coordinator.get_retained_einsatz(self._einsatznr):
            self._last_einsatz = einsatz
        return self._last_einsatz

    @property
    def available(self) -> bool:
        """Keep a retained entity available until it is removed by retention cleanup."""
        return super().available and self._einsatz is not None

    @property
    def native_value(self) -> str | None:
        """Return the published status."""
        if (einsatz := self._einsatz) is None:
            return None
        return einsatz.zustand

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Return all data published for this incident."""
        if (einsatz := self._einsatz) is None:
            return {"einsatznummer": self._einsatznr}
        return _einsatz_attributes(einsatz, self.coordinator.kartenposition)
