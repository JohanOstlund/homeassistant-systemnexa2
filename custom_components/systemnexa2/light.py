from __future__ import annotations
from typing import Any, Optional
from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, DIMMER_MODELS, CONF_MODEL
from .coordinator import NexaCoordinator

BRIGHTNESS_MAX = 255

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    model = entry.data.get(CONF_MODEL, "WPD-01")
    if model in DIMMER_MODELS:
        coord: NexaCoordinator = hass.data[DOMAIN][entry.entry_id]
        async_add_entities([NexaDimmerLight(coord, entry, model)])

class NexaDimmerLight(CoordinatorEntity[NexaCoordinator], LightEntity):
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_should_poll = False

    def __init__(self, coordinator: NexaCoordinator, entry: ConfigEntry, model: str):
        super().__init__(coordinator)
        self._entry = entry
        self._model = model
        # Stabilt unique_id för entiteten:
        self._attr_unique_id = f"{coordinator.host}:{coordinator.port}-{model}-light"
        self._attr_name = entry.title or model

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            # Stabil device-identifierare per fysisk enhet (host:port)
            identifiers={(DOMAIN, f"{self.coordinator.host}:{self.coordinator.port}")},
            name=self._entry.title or self._model,
            manufacturer="System Nexa",
            model=self._model,
            configuration_url=f"http://{self.coordinator.host}:{self.coordinator.port}",
        )

    @property
    def is_on(self) -> bool:
        return bool((self.coordinator.data or {}).get("on", 0))

    @property
    def brightness(self) -> Optional[int]:
        v = (self.coordinator.data or {}).get("v")
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
            v = round(max(0, min(BRIGHTNESS_MAX, int(kwargs[ATTR_BRIGHTNESS]))) / BRIGHTNESS_MAX, 2)
            await self.coordinator.async_send_value(v)
        else:
            await self.coordinator.async_send_value(1)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_value(0)