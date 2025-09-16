DOMAIN = "systemnexa2"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_TOKEN = "token"
CONF_NAME = "name"
CONF_MODEL = "model"

DEFAULT_NAME = "System Nexa 2"
DEFAULT_PORT = 3000
DEFAULT_MODEL = "WPD-01"

PLATFORMS = ["light", "switch"]

# Supported models
MODEL_WPD01 = "WPD-01"  # Dimmer (plug)
MODEL_WBD01 = "WBD-01"  # Dimmer (in-wall)
MODEL_WPR01 = "WPR-01"  # Relay plug (on/off)
MODEL_WPO01 = "WPO-01"  # Outdoor on/off
MODEL_WBR01 = "WBR-01"  # In-wall on/off

DIMMER_MODELS = {MODEL_WPD01, MODEL_WBD01}
SWITCH_MODELS = {MODEL_WPR01, MODEL_WPO01, MODEL_WBR01}
