from __future__ import annotations
from typing import Any, Optional
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import NexaCoordinator

BRIGHTNESS_MAX = 255

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator: NexaCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NexaWpd01Light(coordinator, entry)])

class NexaWpd01Light(CoordinatorEntity[NexaCoordinator], LightEntity):
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_should_poll = False

    def __init__(self, coordinator: NexaCoordinator, entry: ConfigEntry):
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}-wpd01"
        self._attr_name = entry.title or "WPD-01"

    @property
    def is_on(self) -> bool:
        state = self.coordinator.data or {}
        if "on" in state:
            return bool(state.get("on"))
        v = state.get("v")
        try:
            return float(v) > 0 if v is not None else False
        except Exception:
            return False

    @property
    def brightness(self) -> Optional[int]:
        state = self.coordinator.data or {}
        v = state.get("v")
        if v is None:
            return None
        try:
            v = float(v)
        except Exception:
            return None
        v = min(1.0, max(0.0, v))
        return int(round(v * BRIGHTNESS_MAX))

    async def async_turn_on(self, **kwargs: Any) -> None:
        if ATTR_BRIGHTNESS in kwargs:
            v = max(0, min(BRIGHTNESS_MAX, int(kwargs[ATTR_BRIGHTNESS]))) / BRIGHTNESS_MAX
            data = await self.coordinator.api.set_brightness(v)
        else:
            data = await self.coordinator.api.set_on(True)
        self.coordinator.async_set_updated_data(data)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        data = await self.coordinator.api.set_on(False)
        self.coordinator.async_set_updated_data(data)
        self.async_write_ha_state()

    async def async_update(self) -> None:
        await self.coordinator.async_request_refresh()