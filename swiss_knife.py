import os
import subprocess
import sys
from typing import Literal

import py7zr
import pyzipper
import qdarktheme
import rarfile
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config import SwissKnifeConfig


class ArchiveManager:
    def __init__(self):
        self.rar_path = self.find_rar_unrar("rar")
        self.unrar_path = self.find_rar_unrar("unrar")

    def find_rar_unrar(self, rar_unrar: Literal["rar", "unrar"]):
        # Проверка наличия rar / unrar по умолчанию
        if sys.platform == "win32":
            default_path = rf"C:\Program Files\WinRAR\{rar_unrar}.exe"
        elif sys.platform == "darwin":
            default_path = f"/usr/local/bin/{rar_unrar}"
        else:
            default_path = rar_unrar

        if os.path.exists(default_path):
            return default_path

        # Проверка переменных окружения
        for path in os.environ["PATH"].split(os.pathsep):
            rar_unrar_path = os.path.join(path, rar_unrar)
            if os.path.exists(rar_unrar_path):
                return rar_unrar_path

        return None

    def check_unrar_installed(self):
        if self.unrar_path is None:
            QMessageBox.warning(
                self, "Ошибка", "Для работы с .rar архивами необходимо установить unrar / winrar."
            )
            return False
        return True

    def check_rar_installed(self):
        if self.rar_path is None:
            QMessageBox.warning(
                self, "Ошибка", "Для работы с .rar архивами необходимо установить rar. / winrar"
            )
            return False
        return True

    def unarchive(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите архив", "", "Архивы (*.7z *.zip *.rar)"
        )
        if file_path:
            extract_path = QFileDialog.getExistingDirectory(self, "Выберите папку для извлечения")
            if extract_path:
                password = self.password_input.text() or None
                try:
                    if file_path.endswith(".zip"):
                        with pyzipper.AESZipFile(file_path, "r") as zip_ref:
                            if password:
                                zip_ref.setpassword(password.encode())
                            zip_ref.extractall(extract_path)
                    elif file_path.endswith(".rar"):
                        if not self.check_unrar_installed():
                            return
                        try:
                            with rarfile.RarFile(file_path, "r") as rar_ref:
                                if password:
                                    rar_ref.setpassword(password)
                                rar_ref.extractall(extract_path)
                        except rarfile.NeedFirstRarFile:
                            QMessageBox.warning(
                                self,
                                "Ошибка",
                                "Для работы с .rar архивами необходимо установить unrar.",
                            )
                            return
                    elif file_path.endswith(".7z"):
                        with py7zr.SevenZipFile(
                            file_path, mode="r", password=password
                        ) as seven_zip_ref:
                            seven_zip_ref.extractall(extract_path)
                    QMessageBox.information(self, "Успех", "Разархивирование завершено успешно!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при разархивировании: {str(e)}")

    def archive(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Выберите файлы для архивации", "", "Все файлы (*)"
        )
        if files:
            archive_type = self.archive_type_combo.currentText()
            archive_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить архив как", "", f"Архивы (*{archive_type})"
            )
            if archive_path:
                if not archive_path.endswith(archive_type):
                    archive_path += archive_type

                password = self.password_input.text() or None
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
                        QMessageBox.warning(
                            self, ":(", "Работа с .rar архивами пока что не поддерживается."
                        )
                        return False
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

                    QMessageBox.information(self, "Успех", "Архивация завершена успешно!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при архивации: {str(e)}")


class SwissKnifeApp(QWidget, ArchiveManager):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(SwissKnifeConfig.app_name)
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Выпадающий список для выбора типа архива
        self.archive_type_label = QLabel("Тип архива:", self)
        layout.addWidget(self.archive_type_label)

        self.archive_type_combo = QComboBox(self)
        self.archive_type_combo.addItem(".zip")
        self.archive_type_combo.addItem(".rar")
        self.archive_type_combo.addItem(".7z")
        layout.addWidget(self.archive_type_combo)

        self.password_label = QLabel("Пароль (необязательно):", self)
        layout.addWidget(self.password_label)

        # Контейнер для поля ввода пароля и кнопки показа
        password_layout = QHBoxLayout()

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Скрываем пароль звездочками
        password_layout.addWidget(self.password_input)

        self.toggle_password_btn = QPushButton("Видимость", self)
        self.toggle_password_btn.setCheckable(True)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_password_btn)

        layout.addLayout(password_layout)

        self.btn_unarchive = QPushButton("Разархивировать", self)
        self.btn_unarchive.clicked.connect(self.unarchive)
        layout.addWidget(self.btn_unarchive)

        self.btn_archive = QPushButton("Архивировать", self)
        self.btn_archive.clicked.connect(self.archive)
        layout.addWidget(self.btn_archive)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        """Переключает видимость пароля."""
        if self.toggle_password_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)  # Показываем пароль
            self.toggle_password_btn.setIcon(
                QIcon.fromTheme("visibility-off")
            )  # Иконка "глаз закрыт"
        else:
            self.password_input.setEchoMode(QLineEdit.Password)  # Скрываем пароль
            self.toggle_password_btn.setIcon(QIcon.fromTheme("visibility"))  # Иконка "глаз открыт"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")  # Автоматическая синхронизация с системной темой
    swiss_k_config = SwissKnifeConfig()
    app.setWindowIcon(QIcon(swiss_k_config.icon_path))  # Устанавливаем иконку для приложения
    window = SwissKnifeApp()
    window.setWindowIcon(QIcon(swiss_k_config.icon_path))  # Устанавливаем иконку для окна
    window.show()
    sys.exit(app.exec_())
