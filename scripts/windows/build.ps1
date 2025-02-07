# Установка режима остановки при любой ошибке
$ErrorActionPreference = "Stop"

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

# Получаем путь к Python из виртуального окружения
$pythonPath = Join-Path -Path $venv_path -ChildPath "Scripts\python.exe"

# Проверяем, существует ли Python в виртуальном окружении
if (-Not (Test-Path $pythonPath)) {
    Write-Output "Ошибка: Python не найден в виртуальном окружении! Убедитесь, что виртуальное окружение настроено правильно."
    exit 1
}

# Активируем виртуальное окружение
& "$venv_path\Scripts\Activate.ps1"

# Указываем абсолютный путь к папке "scripts"
$scriptsPath = Resolve-Path -Path "."
$configPath = Resolve-Path -Path "config"

Write-Output "Путь к utils: $scriptsPath"

# Вызываем Python с многострочной командой
$command = @"
import sys
sys.path.append(r"$scriptsPath")
sys.path.append(r"$configPath")
from scripts import build_tools
from config.swiss_knife_config import SwissKnifeConfig
build_tools.build_with_pyinstaller(SwissKnifeConfig)
"@

# Выводим команду для отладки (опционально)
Write-Output "Команда для сборки приложения: $command"

# Сохраняем код во временный файл
$tempFile = [System.IO.Path]::GetTempFileName()
$command | Out-File -FilePath $tempFile -Encoding utf8

Write-Output $pythonPath $tempFile

# Запускаем Python из виртуального окружения
Start-Process -FilePath $pythonPath -ArgumentList $tempFile -NoNewWindow -Wait

# Удаляем временный файл
Remove-Item -Path $tempFile

# Деактивируем виртуальное окружение (опционально)
deactivate

Write-Output "Билд сохранен в директорию .\dist"