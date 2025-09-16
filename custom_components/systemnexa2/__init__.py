from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS, DEFAULT_MODEL
from .coordinator import NexaCoordinator

CURRENT_ENTRY_VERSION = 6  # matchar config_flow.VERSION för 0.4.0

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if entry.version < CURRENT_ENTRY_VERSION:
        ok = await async_migrate_entry(hass, entry)
        if not ok:
            return False

    coord = NexaCoordinator(hass, entry)
    await coord.async_start()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coord
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        coordinator: NexaCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_stop()
    return unloaded

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrera äldre config entries till nyare datamodell."""
    version = entry.version
    data = dict(entry.data)

    if version < 6:
        if "model" not in data:
            data["model"] = DEFAULT_MODEL  # "WPD-01"
        hass.config_entries.async_update_entry(entry, data=data, version=6)
        version = 6

    return True
