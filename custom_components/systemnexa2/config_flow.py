from __future__ import annotations
from homeassistant import config_entries
import voluptuous as vol
from .const import (
    DOMAIN, CONF_HOST, CONF_PORT, CONF_TOKEN, CONF_NAME, CONF_MODEL,
    DEFAULT_NAME, DEFAULT_PORT, DEFAULT_MODEL,
    MODEL_WPD01, MODEL_WBD01, MODEL_WPR01, MODEL_WPO01, MODEL_WBR01
)

MODEL_OPTIONS = [MODEL_WPD01, MODEL_WBD01, MODEL_WPR01, MODEL_WPO01, MODEL_WBR01]

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
    vol.Optional(CONF_TOKEN, default=""): str,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): vol.In(MODEL_OPTIONS),
})

class SystemNexa2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 6  # behåll samma entry-version som 0.4.0 (ingen ny migrationsdata krävs)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Stabil, deterministisk unique_id per config entry (host:port)
            unique = f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
            await self.async_set_unique_id(unique)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input
            )

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)