# Проверяем, существует ли виртуальное окружение в текущей директории
if (Test-Path "venv") {
    $venv_path = "venv"
} else {
    # Запрашиваем путь к виртуальному окружению
    $venv_path = Read-Host "Введите путь к виртуальному окружению (venv)"
}

# Проверяем, существует ли указанный путь
if (-Not (Test-Path $venv_path)) {
    Write-Output "Ошибка: Директория виртуального окружения не найдена! Создайте виртуальное окружение и установите requirements_dev."
    exit 1
}

# Активируем виртуальное окружение
& "$venv_path\Scripts\Activate.ps1"

# Вызываем Python и получаем вывод
$command = python -c @"
import sys
sys.path.append("../packages")
import packages.build_tools
from config import SwissKnifeConfig
print(packages.build_tools.build_pybuilder(SwissKnifeConfig))
"@

# Выводим команду для отладки (опционально)
Write-Output "Команда для сборки приложения: $command"

# Выполняем команду в PowerShell
Invoke-Expression $command

# Деактивируем виртуальное окружение (опционально)
deactivate

Write-Output "Билд сохранен в директорию .\dist"