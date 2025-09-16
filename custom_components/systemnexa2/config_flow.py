from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client
from .const import (
    DOMAIN, CONF_HOST, CONF_TOKEN, CONF_NAME, CONF_POLL_INTERVAL, CONF_PORT,
    DEFAULT_NAME, DEFAULT_POLL_INTERVAL, DEFAULT_PORT
)
from .coordinator import build_base_url

class SystemNexa2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            try:
                host = user_input[CONF_HOST].strip()
                port = user_input.get(CONF_PORT, 3000)
                base = build_base_url(host, port)
                session = aiohttp_client.async_get_clientsession(self.hass)
                headers = {"token": user_input.get(CONF_TOKEN, "")} if user_input.get(CONF_TOKEN) else {}
                async with session.get(base + "state", headers=headers, timeout=8) as resp:
                    if resp.status != 200:
                        errors["base"] = "cannot_connect"
                    else:
                        info = await resp.json(content_type=None)
                        title = user_input.get(CONF_NAME) or info.get("name") or DEFAULT_NAME
                        await self.async_set_unique_id(f"{DOMAIN}-{host}")
                        self._abort_if_unique_id_configured()
                        return self.async_create_entry(
                            title=title,
                            data={
                                CONF_HOST: host,
                                CONF_PORT: port,
                                CONF_TOKEN: user_input.get(CONF_TOKEN, ""),
                                CONF_POLL_INTERVAL: user_input.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL),
                                CONF_NAME: title,
                            },
                        )
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required(CONF_HOST, description={"suggested_value": "192.168.1.67"}): str,
            vol.Optional(CONF_PORT, default=3000): int,
            vol.Optional(CONF_TOKEN, default=""): str,
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Optional(CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)