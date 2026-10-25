"""Kreis Steinfurt Einsätze integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .coordinator import KreisSteinfurtCoordinator


PLATFORMS = [
    "sensor",
]

# The integration is set up exclusively through its config flow, not YAML.
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up from YAML."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up from config entry."""

    coordinator = KreisSteinfurtCoordinator(hass, entry)

    await coordinator.async_initialize()

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def _async_update_listener(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload the integration after options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Migrate the original summary sensor to its stable entity ID."""
    if entry.version >= 2:
        return True

    entity_registry = er.async_get(hass)
    unique_id = f"{DOMAIN}_einsaetze_{entry.entry_id}"
    entity_id = entity_registry.async_get_entity_id("sensor", DOMAIN, unique_id)

    if entity_id is not None and entity_id != "sensor.kreis_steinfurt_einsaetze":
        entity_registry.async_update_entity(
            entity_id,
            new_entity_id="sensor.kreis_steinfurt_einsaetze",
        )

    hass.config_entries.async_update_entry(entry, version=2)
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload integration."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
