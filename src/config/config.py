from typing import Final

# Auth
AUTH_MODE: Final[str] = 'by-auth'  # or 'by-service'
CLIENT_SECRET_FILE: Final[str] = 'client_secret.json'
SERVICE_ACCOUNT_FILE: Final[str] = 'service-credentials.json'
TOKEN_FILE: Final[str] = 'token.json'

# Calendar
TIME_ZONE: Final[str] = 'Europe/Moscow'
TAG: Final[str] = '[AUTO_IMPORTED]'
CALENDAR_CONFIG_FILE: Final[str] = "calendar_config.txt"


# AUTO RUN
LAST_RUN_FILE = "last_run.txt"
UPDATE_INTERVAL_HOURS = 24  # обновлять раз в 24 часа
