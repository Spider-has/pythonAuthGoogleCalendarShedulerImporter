import json
from pathlib import Path
from typing import Optional, Tuple

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)

    def save_config(self, calendar_id: str, weeks_ahead: int):
        """Сохраняет конфигурацию в JSON."""
        config = {
            "calendar_id": calendar_id,
            "weeks_ahead": weeks_ahead
        }
        self.config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')

    def load_config(self) -> Optional[Tuple[str, int]]:
        """Загружает (calendar_id, weeks_ahead) или None."""
        if not self.config_path.exists():
            return None
        try:
            data = json.loads(self.config_path.read_text(encoding='utf-8'))
            return data["calendar_id"], data["weeks_ahead"]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise ValueError(f"Некорректный формат конфигурационного файла: {e}")