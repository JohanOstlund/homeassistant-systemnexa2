from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Optional("port", default=3000): int,
        vol.Optional("token", default=""): str,
        vol.Optional("name", default="WPD-01"): str,
    }
)

class SystemNexa2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"], data=user_input
            )
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
