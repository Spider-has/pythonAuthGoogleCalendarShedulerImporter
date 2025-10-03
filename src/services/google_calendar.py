from datetime import date, datetime
from googleapiclient.discovery import build
from config.config import  TAG

class GoogleCalendarService:
    def __init__(self, credentials):
        self.service = build("calendar", "v3", credentials=credentials)
        self._calendar_id = None  # приватное поле
        self.tag = TAG


    def set_calendar_id(self, calendar_id: str):
        """Устанавливает ID календаря для последующих операций."""
        if not calendar_id or not isinstance(calendar_id, str):
            raise ValueError("ID календаря должен быть непустой строкой")
        self._calendar_id = calendar_id.strip()

    @property
    def calendar_id(self) -> str:
        """Возвращает текущий ID календаря. Вызывает ошибку, если не установлен."""
        if self._calendar_id is None:
            raise RuntimeError("calendar_id не установлен. Вызовите set_calendar_id().")
        return self._calendar_id


    def get_writable_calendars(self):
        """Возвращает список календарей, в которые можно писать (owner/writer)."""
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            return [
                cal for cal in calendars
                if cal.get('accessRole') in ('owner', 'writer')
            ]
        except Exception as e:
            raise RuntimeError(f"Не удалось получить список календарей: {e}") from e

    def delete_events_in_week(self, week_start: date, week_end: date):
        time_min = datetime.combine(week_start, datetime.min.time()).isoformat() + 'Z'
        time_max = datetime.combine(week_end, datetime.max.time()).isoformat() + 'Z'

        print(f"🔍 Поиск событий для удаления с {week_start} по {week_end}...")

        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        deleted = 0
        for event in events_result.get('items', []):
            if self.tag in str(event.get('description', '')):
                try:
                    self.service.events().delete(
                        calendarId=self.calendar_id,
                        eventId=event['id']
                    ).execute()
                    print(f"🗑️ Удалено: {event.get('summary', 'Без названия')}")
                    deleted += 1
                except Exception as e:
                    print(f"❌ Ошибка удаления: {e}")
        print(f"✅ Удалено {deleted} событий.")


    def create_calendar(self, summary: str, time_zone: str = "Europe/Moscow"):
        if not summary or not summary.strip():
            raise ValueError("Название календаря не может быть пустым")
        
        calendar_body = {
            'summary': summary.strip(),
            'timeZone': time_zone
        }
        try:
            created = self.service.calendars().insert(body=calendar_body).execute()
            return created['id']
        except Exception as e:
            raise RuntimeError(f"Не удалось создать календарь: {e}") from e

    def import_events(self, events):
        for event in events:
            try:
                self.service.events().insert(
                    calendarId=self.calendar_id,
                    body=event
                ).execute()
                print(f"✅ Добавлено: {event['summary']}")
            except Exception as e:
                print(f"❌ Ошибка при добавлении {event['summary']}: {e}")