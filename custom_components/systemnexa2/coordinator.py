from __future__ import annotations
import asyncio
import aiohttp
import logging
import json
from typing import Any, Optional
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from .const import (
    DOMAIN, CONF_HOST, CONF_PORT, CONF_TOKEN, CONF_POLL_INTERVAL,
    DEFAULT_PORT, DEFAULT_POLL_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

def _normalize_state(raw: dict | str | None) -> dict:
    if raw is None:
        return {}
    if isinstance(raw, dict) and raw.get("type") == "state" and "value" in raw:
        try:
            v = float(raw.get("value", 0))
        except Exception:
            v = 0.0
        return {"on": 1 if v > 0 else 0, "v": v}
    if isinstance(raw, dict):
        out = {}
        v = raw.get("v", 0)
        try:
            v = float(v)
        except Exception:
            v = 0.0
        on = raw.get("on")
        if on is None:
            on = 1 if v > 0 else 0
        out["on"] = 1 if bool(on) else 0
        out["v"] = v
        return out
    return {}

class NexaCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass, entry: ConfigEntry):
        super().__init__(hass, _LOGGER, name=f"{DOMAIN}_{entry.entry_id}", update_interval=None)
        self.hass = hass
        self.entry = entry
        self.host: str = entry.data.get(CONF_HOST)
        self.port: int = entry.data.get(CONF_PORT, DEFAULT_PORT)
        self.token: str = entry.data.get(CONF_TOKEN, "")
        self.session = aiohttp.ClientSession()
        self._ws_task: Optional[asyncio.Task] = None
        self._ws_ok = False
        self.data = {}

    async def _async_update_data(self) -> dict:
        return await self.async_fetch_state()

    async def async_fetch_state(self) -> dict:
        try:
            async with self.session.get(f"http://{self.host}:{self.port}/state", timeout=8) as resp:
                resp.raise_for_status()
                raw = await resp.json(content_type=None)
                self.data = _normalize_state(raw)
                return self.data
        except Exception as err:
            raise UpdateFailed(f"HTTP state error: {err}")

    async def _ws_loop(self):
        url = f"ws://{self.host}:{self.port}/live"
        headers = {}
        while True:
            try:
                async with self.session.ws_connect(url, headers=headers, heartbeat=30) as ws:
                    _LOGGER.info("WS connected: %s", url)
                    await ws.send_json({"type": "login", "value": self.token or ""})
                    self._ws_ok = True
                    try:
                        await self.async_fetch_state()
                        self.async_set_updated_data(self.data)
                    except Exception:
                        pass
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                payload = json.loads(msg.data)
                                if payload.get("type") == "state":
                                    self.data = _normalize_state(payload)
                                    self.async_set_updated_data(self.data)
                            except Exception as e:
                                _LOGGER.warning("WS parse error: %s", e)
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break
            except Exception as e:
                self._ws_ok = False
                _LOGGER.warning("WS error: %s (retry in 10s)", e)
                await asyncio.sleep(10)

    async def async_send_value(self, value_0_1: float | int):
        if self._ws_ok:
            try:
                async with self.session.ws_connect(f"ws://{self.host}:{self.port}/live") as ws:
                    await ws.send_json({"type": "login", "value": self.token or ""})
                    await ws.send_json({"type": "state", "value": str(value_0_1)})
                    return
            except Exception as e:
                _LOGGER.warning("WS command failed, fallback HTTP: %s", e)
        try:
            if isinstance(value_0_1, int):
                url = f"http://{self.host}:{self.port}/state?on={1 if value_0_1 else 0}"
            else:
                url = f"http://{self.host}:{self.port}/state?v={value_0_1}"
            async with self.session.get(url, timeout=8) as resp:
                resp.raise_for_status()
        except Exception as e:
            _LOGGER.error("HTTP command failed: %s", e)

    async def async_start(self):
        if not self._ws_task:
            self._ws_task = asyncio.create_task(self._ws_loop())

    async def async_stop(self):
        if self._ws_task:
            self._ws_task.cancel()
            self._ws_task = None
        await self.session.close()