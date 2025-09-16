from __future__ import annotations
import aiohttp
import logging
from typing import Any
from urllib.parse import urljoin
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from .const import CONF_HOST, CONF_TOKEN, CONF_POLL_INTERVAL, CONF_PORT, DEFAULT_POLL_INTERVAL, DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

def build_base_url(host: str, port: int | None) -> str:
    if ":" in host:
        return f"http://{host.strip('/')}/"
    p = port or DEFAULT_PORT
    return f"http://{host.strip('/')}:{p}/"

class NexaApiClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str, token: str):
        self._session = session
        self._base = base_url
        self._headers = {"token": token} if token else {}

    async def get_state(self) -> dict[str, Any]:
        url = urljoin(self._base, "state")
        async with self._session.get(url, headers=self._headers, timeout=8) as resp:
            resp.raise_for_status()
            return await resp.json(content_type=None)

    async def set_on(self, on: bool) -> dict[str, Any]:
        url = urljoin(self._base, f"state?on={1 if on else 0}")
        async with self._session.get(url, headers=self._headers, timeout=8) as resp:
            resp.raise_for_status()
            return await resp.json(content_type=None)

    async def set_brightness(self, value_0_1: float) -> dict[str, Any]:
        url = urljoin(self._base, f"state?v={value_0_1}")
        async with self._session.get(url, headers=self._headers, timeout=8) as resp:
            resp.raise_for_status()
            return await resp.json(content_type=None)

class NexaCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry

        poll = entry.data.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)
        host = entry.data[CONF_HOST]
        port = entry.data.get(CONF_PORT, DEFAULT_PORT)
        base_url = build_base_url(host, port)

        self.api = NexaApiClient(
            session=aiohttp.ClientSession(),
            base_url=base_url,
            token=entry.data.get(CONF_TOKEN, "")
        )

        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=timedelta(seconds=poll),
        )

    async def _async_update_data(self) -> dict:
        try:
            return await self.api.get_state()
        except Exception as err:
            raise UpdateFailed(str(err)) from err

    async def async_close(self):
        try:
            await self.api._session.close()
        except Exception:
            pass