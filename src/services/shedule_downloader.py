# services/schedule_downloader.py
import requests
from datetime import datetime, timedelta
from typing import List

class ScheduleDownloader:
    BASE_URL = "https://ruz.spbstu.ru/faculty/125/groups/42681/ical"

    @staticmethod
    def get_monday_of_week(date: datetime) -> datetime:
        """Возвращает понедельник недели для заданной даты."""
        return date - timedelta(days=date.weekday())

    def download_ics_for_weeks(self, weeks_ahead: int) -> List[str]:
        """
        Скачивает .ics-контент для текущей недели и `weeks_ahead` недель вперёд.
        Возвращает список строк (контент каждого .ics).
        """
        if weeks_ahead < 1:
            raise ValueError("weeks_ahead должен быть >= 1")

        contents = []
        today = datetime.now()
        
        for i in range(weeks_ahead):
            monday = self.get_monday_of_week(today + timedelta(weeks=i))
            date_str = monday.strftime("%Y-%m-%d")
            url = f"{self.BASE_URL}?date={date_str}"
            
            print(f"📥 Скачивание расписания на неделю с {date_str}...")
            try:
                response = requests.get(url)
                response.raise_for_status()
                contents.append(response.text)
            except Exception as e:
                print(f"⚠️ Не удалось скачать расписание на {date_str}: {e}")

        return contents