from __future__ import annotations
import asyncio, aiohttp, json, logging
from typing import Optional
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_TOKEN, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

def normalize_state(raw: dict | None) -> dict:
    if not raw:
        return {}
    if raw.get("type") == "state":
        try:
            v = float(raw.get("value", 0))
        except Exception:
            v = 0.0
        return {"on": 1 if v > 0 else 0, "v": v}
    v = raw.get("v", 0)
    try:
        v = float(v)
    except Exception:
        v = 0.0
    on = raw.get("on", 1 if v > 0 else 0)
    return {"on": 1 if on else 0, "v": v}

class NexaCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass, entry: ConfigEntry):
        super().__init__(hass, _LOGGER, name=f"{DOMAIN}_{entry.entry_id}", update_interval=None)
        self.hass = hass
        self.entry = entry
        self.host = entry.data.get(CONF_HOST)
        self.port = entry.data.get(CONF_PORT, DEFAULT_PORT)
        self.token = entry.data.get(CONF_TOKEN, "")
        self.session = aiohttp.ClientSession()
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.ws_task: Optional[asyncio.Task] = None
        self.cmd_queue: asyncio.Queue = asyncio.Queue()
        self._ws_connected = asyncio.Event()
        self.data = {}

    async def _async_update_data(self) -> dict:
        return await self.http_fetch_state()

    async def http_fetch_state(self) -> dict:
        url = f"http://{self.host}:{self.port}/state"
        try:
            async with self.session.get(url, timeout=8) as resp:
                resp.raise_for_status()
                self.data = normalize_state(await resp.json(content_type=None))
                return self.data
        except Exception as e:
            raise UpdateFailed(f"HTTP state error: {e}")

    async def ws_loop(self):
        url = f"ws://{self.host}:{self.port}/live"
        while True:
            try:
                async with self.session.ws_connect(url, heartbeat=30) as ws:
                    self.ws = ws
                    await ws.send_json({"type": "login", "value": self.token or ""})
                    self._ws_connected.set()
                    try:
                        await self.http_fetch_state()
                        self.async_set_updated_data(self.data)
                    except Exception:
                        pass
                    reader = asyncio.create_task(self.ws_reader())
                    writer = asyncio.create_task(self.ws_writer())
                    done, pending = await asyncio.wait({reader, writer}, return_when=asyncio.FIRST_EXCEPTION)
                    for t in pending:
                        t.cancel()
            except Exception as e:
                _LOGGER.warning("WS reconnect in 5s: %s", e)
                self._ws_connected.clear()
                await asyncio.sleep(5)

    async def ws_reader(self):
        assert self.ws
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    if data.get("type") == "state":
                        self.data = normalize_state(data)
                        self.async_set_updated_data(self.data)
                except Exception as e:
                    _LOGGER.debug("WS parse issue: %s", e)
            elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                break

    async def ws_writer(self):
        assert self.ws
        while True:
            value = await self.cmd_queue.get()
            try:
                await self.ws.send_json({"type": "state", "value": str(value)})
            except Exception as e:
                _LOGGER.warning("WS send failed (%s); falling back to HTTP", e)
                await self._http_send_value(value)

    async def _http_send_value(self, value):
        try:
            if value in ("0", "1"):
                url = f"http://{self.host}:{self.port}/state?on={value}"
            else:
                url = f"http://{self.host}:{self.port}/state?v={value}"
            async with self.session.get(url, timeout=8) as resp:
                resp.raise_for_status()
        except Exception as e:
            _LOGGER.error("HTTP command failed: %s", e)

    async def async_send_value(self, value_0_1):
        # Round to 2 decimals for dimming values
        if isinstance(value_0_1, (int, float)):
            if value_0_1 in (0, 1):
                val = "1" if value_0_1 == 1 else "0"
            else:
                val = f"{round(float(value_0_1), 2):.2f}"
        else:
            val = str(value_0_1)

        if not self._ws_connected.is_set():
            await self._http_send_value(val)
            return
        await self.cmd_queue.put(val)
        # optimistic update
        if val in ("0", "1"):
            self.data["on"] = 1 if val == "1" else 0
            self.data["v"] = 1.0 if val == "1" else 0.0
        else:
            try:
                v = float(val)
            except Exception:
                v = 0.0
            self.data["on"] = 1 if v > 0 else 0
            self.data["v"] = v
        self.async_set_updated_data(self.data)

    async def async_start(self):
        if not self.ws_task:
            self.ws_task = asyncio.create_task(self.ws_loop())

    async def async_stop(self):
        if self.ws_task:
            self.ws_task.cancel()
            self.ws_task = None
        if self.ws and not self.ws.closed:
            await self.ws.close()
        await self.session.close()