# Swiss knife
Версия: 0.2.0

<p align="center">
    <img src="media/screenshots/screenshot_mac.png">
</p>
<p align="center">
    <img src="media/screenshots/screenshot_win.png">
</p>

## Требования
1. python 3.10
2. unrar (опционально, нужен для работы с *.rar)

## На данный момент поддерживается
1. Разархивировать .7z, .zip, .rar (требуется установка модуля rar: brew / macports / website) - с паролем / без пароля
2. Архивировать .7z, .zip - с паролем / без пароля

## Сборка с помощью pyinstaller:
### macOS:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
scripts/mac/build.sh
```

### Windows:
```bash
python -m venv venv
venv\Scripts\activate - Windows
pip install -r requirements.txt
scripts\windows\build.ps1
```