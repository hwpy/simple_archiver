# simple_archiver
Простой архиватор

![Alt text](media/screenshot.png?raw=true "Optional Title")

## На данный момент поддерживается
1. Разархивировать .7z, .zip, .rar (требуется установка brew install rar)
2. Архивировать .7z, .zip, .rar (требуется установка brew install unrar) с паролем и без пароля

## Сборка с помощью pyinstaller:
* pyinstaller --windowed --name="Simple archiver" --icon="media/appicon.png" simple_archiver.py