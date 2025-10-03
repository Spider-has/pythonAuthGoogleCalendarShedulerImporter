from datetime import datetime, timedelta
from pathlib import Path

class RunTracker:
    def __init__(self, file_path: str = "last_run.txt", interval_hours: int = 24):
        self.file_path = Path(file_path)
        self.interval = timedelta(hours=interval_hours)

    def should_run(self) -> bool:
        """Возвращает True, если пора запускать обновление."""
        if not self.file_path.exists():
            return True

        try:
            last_run = datetime.fromisoformat(self.file_path.read_text().strip())
            return datetime.now() - last_run > self.interval
        except (ValueError, OSError):
            # Если файл повреждён — считаем, что нужно запустить
            return True

    def mark_as_run(self):
        """Сохраняет текущее время как время последнего запуска."""
        self.file_path.write_text(datetime.now().isoformat())