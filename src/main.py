
import argparse
from services.config_service import ConfigManager
from services.google_auth import GoogleAuth
from services.google_calendar import GoogleCalendarService
from services.last_run_service import RunTracker
from services.shedule_downloader import ScheduleDownloader
from utils.ics_parser import parse_ics_content
from utils.date_utils import get_week_range_from_events
from config.config import AUTH_MODE, LAST_RUN_FILE, UPDATE_INTERVAL_HOURS
from view.console_view import ConsoleUserInteraction

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--non-interactive', action='store_true',
                        help='Запуск в фоновом режиме (без запросов пользователю)')
    args = parser.parse_args()

    config_manager = ConfigManager()
    config = config_manager.load_config()
    
    tracker = RunTracker(file_path=LAST_RUN_FILE, interval_hours=UPDATE_INTERVAL_HOURS)
    if not tracker.should_run():
        print("🕒 Обновление не требуется. Выход.")
        return
    
    credentials = GoogleAuth.get_credentials(AUTH_MODE)
    calendar_service = GoogleCalendarService(credentials)

    # 2. Загрузка конфигурации

    if not config:
        if args.non_interactive:
            print("❌ Конфигурация отсутствует. Запустите init.sh для настройки.")
            return
        else:
            print("📋 Это первый запуск. Настроим календарь для расписания.")

            ui = ConsoleUserInteraction(calendar_service)

            # 1. Выбор календаря
            calendar_id = ui.prompt_calendar_selection()
            
            # 2. Количество недель
            weeks_ahead = ui.prompt_weeks_ahead()
            
            # 3. Сохранение
            config_manager.save_config(calendar_id, weeks_ahead)
            print(f"\n💾 ID календаря сохранён\n")
    else:
        calendar_id, weeks_ahead = config
        print(f"✅ Используется календарь (ID: {calendar_id[:30]}...)")
        print(f"📅 Будет загружено {weeks_ahead} недель расписания")

    # Теперь устанавливаем выбранный calendar_id
    calendar_service.set_calendar_id(calendar_id)


    downloader = ScheduleDownloader()
    ics_contents = downloader.download_ics_for_weeks(weeks_ahead)

    if not ics_contents:
        print("❌ Не удалось скачать ни одного расписания")
        return

    # Парсинг всех событий
    all_events = []
    for content in ics_contents:
        events = parse_ics_content(content)
        all_events.extend(events)

    if not all_events:
        print("⚠️ Нет событий для импорта")
        return
    

    monday, sunday = get_week_range_from_events(all_events)
    print(f"📅 Общий период расписания: {monday} — {sunday}")

    # 4. Обновление календаря
    calendar_service.delete_events_in_week(monday, sunday)
    calendar_service.import_events(all_events)

    print("✅ Расписание успешно обновлено!")

    tracker.mark_as_run()
    print("\n✅ Расписание успешно обновлено и сохранено в last_run.txt!")

if __name__ == "__main__":
    main()