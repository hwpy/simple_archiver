# Файл setup.ps1

# 1. Запрос пути для установки
$installPath = Read-Host "Введите путь для установки (по умолчанию C:\Program Files)"
if (-not $installPath) {
    $installPath = "C:\Program Files"
}

# 2. Импорт конфигурации из SwissKnifeConfig
# Абсолютный путь к config.py (на два уровня выше)
$configPath = Join-Path -Path $PSScriptRoot -ChildPath "..\..\config.py" | Resolve-Path -ErrorAction Stop
if (-not (Test-Path $configPath)) {
    Write-Host "Ошибка: Файл config.py не найден по пути: $configPath"
    exit 1
}

# Загружаем конфигурацию
try {
    $config = & {
        $pythonCode = @"
import sys
import os
sys.path.append(os.path.abspath(r'$($configPath.Directory.Parent.FullName)'))
from config import SwissKnifeConfig
from packages.builder_tools import build_pybuilder

# Выводим только ожидаемые 7 значений + команду
print(SwissKnifeConfig.app_name)
print(SwissKnifeConfig.app_version)
print(SwissKnifeConfig.screenshot_mac_path)
print(SwissKnifeConfig.screenshot_win_path)
print(SwissKnifeConfig.mac_icon_path)
print(SwissKnifeConfig.win_icon_path)
print(SwissKnifeConfig.app_source)
print(build_pybuilder())  # Должна возвращать ТОЛЬКО команду
"@
        $pythonCode | python -
    }
} catch {
    Write-Host "Ошибка при выполнении Python-кода: $_"
    exit 1
}

# Разбираем вывод Python
$configLines = $config -split "`n" | Where-Object { $_ -ne '' }

# Проверка количества полученных строк
if ($configLines.Count -lt 8) {
    Write-Host "Ошибка: Недостаточно данных в выводе конфигурации. Получено $($configLines.Count) строк."
    exit 1
}

# Извлекаем значения
$app_name = $configLines[0].Trim()
$app_version = $configLines[1].Trim()
$screenshot_mac_path = $configLines[2].Trim()
$screenshot_win_path = $configLines[3].Trim()
$mac_icon_path = $configLines[4].Trim()
$win_icon_path = $configLines[5].Trim()
$app_source = $configLines[6].Trim()
$pyinstallerCommand = $configLines[7].Trim()

Write-Host "`n[Конфигурация]"
Write-Host "Имя приложения: $app_name"
Write-Host "Версия: $app_version"
Write-Host "Команда сборки: $pyinstallerCommand`n"

# 3. Выполнение команды PyInstaller
try {
    Write-Host "Собираем приложение с помощью PyInstaller..."
    Invoke-Expression $pyinstallerCommand -ErrorAction Stop
} catch {
    Write-Host "Ошибка при сборке: $_"
    exit 1
}

# 4. Копирование собранного приложения
$distPath = Join-Path -Path $PSScriptRoot -ChildPath "dist\$app_name"
$destinationPath = Join-Path -Path $installPath -ChildPath $app_name

# Проверка существования собранного приложения
if (-not (Test-Path $distPath)) {
    Write-Host "Ошибка: Собранное приложение не найдено по пути: $distPath"
    exit 1
}

try {
    # Очистка целевой директории
    if (Test-Path $destinationPath) {
        Write-Host "Удаляем существующую директорию: $destinationPath..."
        Remove-Item -Path $destinationPath -Recurse -Force -ErrorAction Stop
    }

    # Копирование
    Write-Host "Копируем в: $destinationPath..."
    Copy-Item -Path $distPath -Destination $destinationPath -Recurse -Force -ErrorAction Stop
} catch {
    Write-Host "Ошибка при копировании: $_"
    exit 1
}

Write-Host "`nУстановка успешно завершена!"
Write-Host "Приложение доступно в: $destinationPath"