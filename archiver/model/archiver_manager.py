# model.py
import os
from pathlib import Path
import subprocess
import sys
from typing import Literal

import py7zr
import pyzipper
import rarfile

from utils.platform_settings import Platform


class ArchiveManager:
    def __init__(self):
        self.rar_path = self.find_rar_unrar("rar")
        self.unrar_path = self.find_rar_unrar("unrar")

    def find_rar_unrar(self, rar_unrar: Literal["rar", "unrar"]):
        # Определяем возможные пути для разных ОС
        search_paths = []

        if Platform.OS == Platform.Windows:
            # Стандартные пути для Windows
            search_paths = [
                r"C:\Program Files\WinRAR\{0}.exe",
                r"C:\Program Files (x86)\WinRAR\{0}.exe",
                r"{0}.exe",  # Проверка PATH
            ]
        elif Platform.OS == Platform.macOS:
            # Пути для macOS
            search_paths = [
                "/usr/local/bin/{0}",
                "/opt/local/bin/{0}",
                "/usr/bin/{0}",
                "/opt/homebrew/bin/{0}",  # Для Homebrew на Apple Silicon
                "{0}",  # Проверка PATH
            ]
        else:
            # Для Linux и других ОС
            search_paths = ["{0}"]

        # Ищем существующий файл
        for path_template in search_paths:
            full_path = path_template.format(rar_unrar)

            # Для Windows: проверяем rar/unrar в разных регистрах
            if Platform.OS == Platform.Windows:
                if os.path.exists(full_path):
                    return full_path
                # Проверяем версию в верхнем регистре
                upper_path = os.path.join(os.path.dirname(full_path), rar_unrar.upper() + ".exe")
                if os.path.exists(upper_path):
                    return upper_path
            else:
                if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                    return full_path

        # Дополнительная проверка PATH для всех ОС
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            candidate = os.path.join(path_dir, rar_unrar)
            if Platform.OS == Platform.Windows:
                candidate += ".exe"

            if os.path.exists(candidate):
                if Platform.OS != Platform.Windows or os.access(candidate, os.X_OK):
                    return candidate

        # Последняя попытка найти через which/where
        try:
            cmd = "where" if Platform.OS == Platform.Windows else "which"
            result = (
                subprocess.check_output([cmd, rar_unrar], stderr=subprocess.DEVNULL, shell=True)
                .decode()
                .strip()
            )

            if os.path.exists(result):
                return result
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return None

    def check_unrar_installed(self):
        return self.unrar_path is not None

    def check_rar_installed(self):
        return self.rar_path is not None

    def unarchive(self, file_path: str, extract_path: str, password: str = None):
        try:
            if file_path.endswith(".zip"):
                with pyzipper.AESZipFile(file_path, "r") as zip_ref:
                    if password:
                        zip_ref.setpassword(password.encode())
                    zip_ref.extractall(extract_path)
            elif file_path.endswith(".rar"):
                if not self.check_unrar_installed():
                    raise Exception("Для работы с .rar архивами необходимо установить unrar.")
                with rarfile.RarFile(file_path, "r") as rar_ref:
                    if password:
                        rar_ref.setpassword(password)
                    rar_ref.extractall(extract_path)
            elif file_path.endswith(".7z"):
                with py7zr.SevenZipFile(file_path, mode="r", password=password) as seven_zip_ref:
                    seven_zip_ref.extractall(extract_path)
            return True
        except Exception as e:
            raise Exception(f"Ошибка при разархивировании: {str(e)}")

    def archive(self, files: list, archive_path: str, archive_type: str, password: str = None):
        try:
            if archive_type == ".zip":
                with pyzipper.AESZipFile(
                    archive_path,
                    "w",
                    compression=pyzipper.ZIP_DEFLATED,
                    encryption=pyzipper.WZ_AES if password else None,
                ) as zip_ref:
                    if password:
                        zip_ref.setpassword(password.encode())
                    for file in files:
                        zip_ref.write(file, os.path.basename(file))
            elif archive_type == ".rar":
                raise Exception("Работа с .rar архивами пока что не поддерживается.")
                # if not self.check_rar_installed():
                #     return
                # rar_cmd = [self.rar_path, "a", archive_path] + files
                # if password:
                #     rar_cmd.insert(2, f"-p{password}")
                # subprocess.run(rar_cmd, check=True)
            elif archive_type == ".7z":
                with py7zr.SevenZipFile(archive_path, "w", password=password) as seven_zip_ref:
                    for file in files:
                        seven_zip_ref.write(file, os.path.basename(file))
            return True
        except Exception as e:
            raise Exception(f"Ошибка при архивации: {str(e)}")
