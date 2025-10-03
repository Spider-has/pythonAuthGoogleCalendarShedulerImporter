#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Создаём venv, если нужно
if [ ! -d "venv" ]; then
    echo "🔧 Создаю виртуальное окружение..."
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi

echo "🚀 Запуск интерактивной настройки..."
venv/bin/python src/main.py
echo "✅ Настройка завершена! Теперь можно добавлять run_scheduler.sh в автозагрузку."