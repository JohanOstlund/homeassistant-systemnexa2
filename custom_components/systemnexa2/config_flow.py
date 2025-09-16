from __future__ import annotations
from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_TOKEN, CONF_NAME, DEFAULT_NAME, DEFAULT_PORT

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
    vol.Optional(CONF_TOKEN, default=""): str,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
})

class SystemNexa2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(f"{DOMAIN}-{user_input[CONF_HOST]}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input.get(CONF_NAME, DEFAULT_NAME), data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)