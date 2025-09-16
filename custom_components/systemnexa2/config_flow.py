from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import aiohttp_client
from .const import DOMAIN, CONF_HOST, CONF_TOKEN, CONF_NAME, CONF_POLL_INTERVAL, DEFAULT_NAME, DEFAULT_POLL_INTERVAL

class SystemNexa2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            try:
                session = aiohttp_client.async_get_clientsession(self.hass)
                url = f"http://{user_input[CONF_HOST]}/state"
                headers = {"token": user_input.get(CONF_TOKEN, "")} if user_input.get(CONF_TOKEN) else {}
                async with session.get(url, headers=headers, timeout=8) as resp:
                    if resp.status != 200:
                        errors["base"] = "cannot_connect"
                    else:
                        info = await resp.json(content_type=None)
                        title = user_input.get(CONF_NAME) or info.get("name") or DEFAULT_NAME
                        await self.async_set_unique_id(f"{DOMAIN}-{user_input[CONF_HOST]}")
                        self._abort_if_unique_id_configured()
                        return self.async_create_entry(
                            title=title,
                            data={
                                CONF_HOST: user_input[CONF_HOST],
                                CONF_TOKEN: user_input.get(CONF_TOKEN, ""),
                                CONF_POLL_INTERVAL: user_input.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL),
                                CONF_NAME: title,
                            },
                        )
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_TOKEN, default=""): str,
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Optional(CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)