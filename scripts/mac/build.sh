#!/bin/bash

set -e

if [ -d "venv" ]; then
    venv_path="venv";
else
    # Запрашиваем путь к виртуальному окружению
    read -p "Введите путь к виртуальному окружению (venv): " venv_path;
fi

# Проверяем, существует ли указанный путь
if [ ! -d "$venv_path" ]; then
  echo "Ошибка: Директория виртуального окружения не найдена! Создайте виртуально окружение и установите requirements_dev"
  exit 1
fi

# Активируем виртуальное окружение
source "$venv_path/bin/activate"

# Вызываем Python и получаем вывод
command=$(python -c '
import sys
sys.path.append("../scripts")
import scripts.build_tools
from config.swiss_knife_config import SwissKnifeConfig
scripts.build_tools.build_with_pyinstaller(SwissKnifeConfig)
')

# Выполняем команду в Bash
eval "$command"

# Деактивируем виртуальное окружение (опционально)
deactivate

echo "Билд сохранен в директорию ./dist"