import asyncio
import aiohttp
import logging
import json
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class NexaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, port, token):
        super().__init__(hass, _LOGGER, name="systemnexa2", update_interval=None)
        self.hass = hass
        self.host = host
        self.port = port
        self.token = token
        self.session = aiohttp.ClientSession()
        self.state = {}
        self._ws_task = None
        self._use_ws = False

    async def _async_update_data(self):
        return await self.async_fetch_state()

    async def async_fetch_state(self):
        try:
            async with self.session.get(f"http://{self.host}:{self.port}/state") as resp:
                data = await resp.json()
                self.state = data
                return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching state: {err}")

    async def async_listen_ws(self):
        url = f"ws://{self.host}:{self.port}/live"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        while True:
            try:
                async with self.session.ws_connect(url, headers=headers) as ws:
                    _LOGGER.info("WebSocket connected to %s", url)
                    await ws.send_json({"type": "login", "value": self.token or ""})
                    self._use_ws = True
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                data = json.loads(msg.data)
                                if data.get("type") == "state":
                                    self.state = data
                                    self.async_set_updated_data(data)
                            except Exception as e:
                                _LOGGER.warning("WS parse error: %s", e)
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break
            except Exception as e:
                self._use_ws = False
                _LOGGER.warning("WS connection error: %s, retrying in 10s", e)
                await asyncio.sleep(10)

    async def async_send_command(self, value: str):
        if self._use_ws:
            try:
                async with self.session.ws_connect(f"ws://{self.host}:{self.port}/live") as ws:
                    await ws.send_json({"type": "login", "value": self.token or ""})
                    await ws.send_json({"type": "state", "value": value})
                    return True
            except Exception as e:
                _LOGGER.warning("WS command failed, fallback to HTTP: %s", e)
        try:
            async with self.session.get(f"http://{self.host}:{self.port}/state?on={1 if value == '1' else 0}") as resp:
                return resp.status == 200
        except Exception as e:
            _LOGGER.error("HTTP command failed: %s", e)
            return False

    async def async_start(self):
        if not self._ws_task:
            self._ws_task = asyncio.create_task(self.async_listen_ws())

    async def async_stop(self):
        if self._ws_task:
            self._ws_task.cancel()
            self._ws_task = None
        await self.session.close()
