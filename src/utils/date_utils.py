from datetime import date, timedelta, datetime
from typing import List

def get_week_range_from_events(events: List[dict]) -> tuple[date, date]:
    if not events:
        raise ValueError("Список событий пуст")

    all_dates = []
    for ev in events:
        start = ev['start']
        if 'dateTime' in start:
            dt_str = start['dateTime']
            if dt_str.endswith('Z'):
                dt_str = dt_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(dt_str)
            all_dates.append(dt.date())
        else:
            all_dates.append(date.fromisoformat(start['date']))

    min_date = min(all_dates)
    max_date = max(all_dates)

    first_monday = min_date - timedelta(days=min_date.weekday())
    last_sunday = max_date + timedelta(days=(6 - max_date.weekday()))

    return first_monday, last_sunday