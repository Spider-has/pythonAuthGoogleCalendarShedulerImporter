#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

cd "$SCRIPT_DIR" || exit 1

mkdir -p logs

VENV_DIR="venv"
LOG_FILE="logs/autostart.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "========== НАЧАЛО ВЫПОЛНЕНИЯ =========="

if [ ! -d "$VENV_DIR" ]; then
    log "Виртуальное окружение не найдено. Создаю..."
    python3 -m venv "$VENV_DIR" || { log "Ошибка: не удалось создать venv"; exit 1; }
    log "Устанавливаю зависимости..."
    "$VENV_DIR/bin/pip" install -r requirements.txt || { log "Ошибка установки зависимостей"; exit 1; }
    log "Виртуальное окружение готово!"
fi

log "Запуск main.py..."
"$VENV_DIR/bin/python" "src/main.py" --non-interactive  >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

log "========== ЗАВЕРШЕНИЕ (код: $EXIT_CODE) =========="
echo "" >> "$LOG_FILE"