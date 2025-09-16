DOMAIN = "systemnexa2"

CONF_HOST = "host"
CONF_TOKEN = "token"
CONF_NAME = "name"
CONF_POLL_INTERVAL = "poll_interval"
CONF_PORT = "port"

DEFAULT_NAME = "WPD-01"
DEFAULT_POLL_INTERVAL = 10  # seconds
DEFAULT_PORT = 80  # Many devices use 3000; if host already includes :port, that wins.

PLATFORMS = ["light"]