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
        default_path = None
        if Platform.OS == Platform.Windows:
            default_path = rf"C:\Program Files\WinRAR\{rar_unrar}.exe"
        else:
            default_path = rar_unrar

        """
        elif Platform.OS == Platform.macOS:
            paths_to_check = [
                f"/usr/local/bin/{rar_unrar}",
                f"/opt/local/bin/{rar_unrar}"
            ]
            for path in paths_to_check:
                if os.path.exists(path):
                    default_path = path
        """

        if os.path.exists(default_path):
            return default_path

        for path in os.environ["PATH"].split(os.pathsep):
            rar_unrar_path = os.path.join(path, rar_unrar)
            if os.path.exists(rar_unrar_path):
                return rar_unrar_path

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
                    raise Exception(
                        "Для работы с .rar архивами необходимо установить unrar."
                    )
                with rarfile.RarFile(file_path, "r") as rar_ref:
                    if password:
                        rar_ref.setpassword(password)
                    rar_ref.extractall(extract_path)
            elif file_path.endswith(".7z"):
                with py7zr.SevenZipFile(
                    file_path, mode="r", password=password
                ) as seven_zip_ref:
                    seven_zip_ref.extractall(extract_path)
            return True
        except Exception as e:
            raise Exception(f"Ошибка при разархивировании: {str(e)}")

    def archive(
        self, files: list, archive_path: str, archive_type: str, password: str = None
    ):
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
                with py7zr.SevenZipFile(
                    archive_path, "w", password=password
                ) as seven_zip_ref:
                    for file in files:
                        seven_zip_ref.write(file, os.path.basename(file))
            return True
        except Exception as e:
            raise Exception(f"Ошибка при архивации: {str(e)}")
