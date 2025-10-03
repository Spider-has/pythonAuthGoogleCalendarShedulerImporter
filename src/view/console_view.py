import sys
from services.google_calendar import GoogleCalendarService

class ConsoleUserInteraction:
    def __init__(self, calendar_service: GoogleCalendarService):
        self.calendar_service = calendar_service

    def prompt_weeks_ahead(self) -> int:
        """Запрашивает у пользователя количество недель для импорта."""
        try:
            weeks_input = input("На сколько недель вперёд импортировать расписание? ").strip()
            weeks = int(weeks_input)
            if weeks < 1:
                self._exit_with_error("Количество недель должно быть >= 1")
            if weeks > 10:
                confirm = input(f"Вы уверены, что хотите скачать {weeks} недель? (y/N): ").strip().lower()
                if confirm != 'y':
                    self._exit_with_error("Отменено пользователем")
            return weeks
        except ValueError:
            self._exit_with_error("Введите целое число")

    def prompt_calendar_selection(self) -> str:
        """Запрашивает у пользователя выбор календаря. Возвращает calendar_id.
        Завершает программу при ошибке.
        """
        try:
            writable_calendars = self.calendar_service.get_writable_calendars()
        except Exception as e:
            self._exit_with_error(f"Не удалось получить список календарей: {e}")

        print("\nВаши календари (можно выбрать для импорта). Рекомендуется создать отдельный календарь, чтобы ваше основное расписание точно никак не повредилось:")
        for i, cal in enumerate(writable_calendars, 1):
            summary = cal.get('summary', 'Без названия')
            print(f"{i}. {summary} (ID: {cal['id']})")
        
        print(f"\n{len(writable_calendars) + 1}. Создать новый календарь")

        try:
            choice = input(f"\nВыберите номер (1–{len(writable_calendars) + 1}): ").strip()
            choice_num = int(choice)

            if 1 <= choice_num <= len(writable_calendars):
                selected = writable_calendars[choice_num - 1]
                print(f"✅ Выбран календарь: {selected['summary']}")
                return selected['id']
            
            elif choice_num == len(writable_calendars) + 1:
                new_name = input("Введите название нового календаря: ").strip()
                if not new_name:
                    self._exit_with_error("Название календаря не может быть пустым.")
                try:
                    new_id = self.calendar_service.create_calendar(new_name)
                    print(f"✅ Создан новый календарь: {new_name}")
                    return new_id
                except Exception as e:
                    self._exit_with_error(f"Не удалось создать календарь: {e}")
            else:
                self._exit_with_error(
                    f"Неверный номер. Допустимые значения: 1–{len(writable_calendars) + 1}"
                )

        except ValueError:
            self._exit_with_error("Введено не число.")
        except KeyboardInterrupt:
            print("\n\n⚠️ Программа прервана пользователем.", file=sys.stderr)
            sys.exit(1)

    def _exit_with_error(self, message: str):
        print(f"❌ {message}", file=sys.stderr)
        sys.exit(1)