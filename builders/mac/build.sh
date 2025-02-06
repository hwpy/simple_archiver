#!/bin/bash

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
sys.path.append("../packages")
import packages.build_tools
from config import SwissKnifeConfig
print(packages.build_tools.build_pybuilder(SwissKnifeConfig))
')

# Выводим команду для отладки (опционально)
echo "Команда для сборки приложения: $command"

# Выполняем команду в Bash
eval "$command"

# Деактивируем виртуальное окружение (опционально)
deactivate

echo "Билд сохранен в директорию ./dist"