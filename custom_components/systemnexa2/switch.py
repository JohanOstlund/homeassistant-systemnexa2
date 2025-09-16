from __future__ import annotations
from typing import Any
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, SWITCH_MODELS, CONF_MODEL
from .coordinator import NexaCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    model = entry.data.get(CONF_MODEL, "WPR-01")
    if model in SWITCH_MODELS:
        coord: NexaCoordinator = hass.data[DOMAIN][entry.entry_id]
        async_add_entities([NexaRelaySwitch(coord, entry, model)])

class NexaRelaySwitch(CoordinatorEntity[NexaCoordinator], SwitchEntity):
    _attr_should_poll = False

    def __init__(self, coordinator: NexaCoordinator, entry: ConfigEntry, model: str):
        super().__init__(coordinator)
        self._entry = entry
        self._model = model
        # Stabilt unique_id för entiteten:
        self._attr_unique_id = f"{coordinator.host}:{coordinator.port}-{model}-switch"
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

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_value(1)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_value(0)