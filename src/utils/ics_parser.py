import pytz
from datetime import datetime, timezone
from icalendar import Calendar
from config.config import TAG, TIME_ZONE

def parse_ics_content(ics_content: str):
    events = []
    cal = Calendar.from_ical(ics_content)
    tz = pytz.timezone(TIME_ZONE)

    for component in cal.walk():
        if component.name == "VEVENT":
            dtstart = component.get('dtstart').dt
            dtend = component.get('dtend').dt
            summary = str(component.get('summary', 'Без названия'))
            location = str(component.get('location', ''))

            # Приведение к UTC, если naive
            if isinstance(dtstart, datetime):
                if dtstart.tzinfo is None:
                    dtstart = dtstart.replace(tzinfo=timezone.utc)
                    dtend = dtend.replace(tzinfo=timezone.utc)
                
                start_local = dtstart.astimezone(tz)
                end_local = dtend.astimezone(tz)

                event = {
                    'summary': summary,
                    'location': location,
                    'description': TAG,
                    'start': {'dateTime': start_local.isoformat(), 'timeZone': TIME_ZONE},
                    'end': {'dateTime': end_local.isoformat(), 'timeZone': TIME_ZONE}
                }
                events.append(event)
            else:
                # События на весь день (редко в расписании, но на всякий случай)
                event = {
                    'summary': summary,
                    'location': location,
                    'description': TAG,
                    'start': {'date': dtstart.isoformat()},
                    'end': {'date': dtend.isoformat()}
                }
                events.append(event)

    return events