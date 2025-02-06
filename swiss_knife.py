import os
import subprocess
import sys

import py7zr
import pyzipper
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

from packages.platform_settings import Platform
from config import SwissKnifeConfig


class SimpleArchiverApp(QWidget):
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
        self.password_input.setEchoMode(
            QLineEdit.Password
        )  # Скрываем пароль звездочками
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
            self.toggle_password_btn.setIcon(
                QIcon.fromTheme("visibility")
            )  # Иконка "глаз открыт"

    def unarchive(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите архив", "", "Архивы (*.7z *.zip *.rar)"
        )
        if file_path:
            extract_path = QFileDialog.getExistingDirectory(
                self, "Выберите папку для извлечения"
            )
            if extract_path:
                password = self.password_input.text() or None
                try:
                    if file_path.endswith(".zip"):
                        with pyzipper.AESZipFile(file_path, "r") as zip_ref:
                            if password:
                                zip_ref.setpassword(password.encode())
                            zip_ref.extractall(extract_path)
                    elif file_path.endswith(".rar"):
                        try:
                            with rarfile.RarFile(file_path, "r") as rar_ref:
                                if password:
                                    rar_ref.setpassword(password)
                                rar_ref.extractall(extract_path)
                        except rarfile.NeedFirstRarFile:
                            QMessageBox.warning(
                                self,
                                "Ошибка",
                                "Для работы с .rar архивами необходимо установить unrar.\n"
                                "Установите его с помощью команды: brew install unrar",
                            )
                            return
                    elif file_path.endswith(".7z"):
                        with py7zr.SevenZipFile(
                            file_path, mode="r", password=password
                        ) as seven_zip_ref:
                            seven_zip_ref.extractall(extract_path)
                    QMessageBox.information(
                        self, "Успех", "Разархивирование завершено успешно!"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Ошибка", f"Ошибка при разархивировании: {str(e)}"
                    )

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
                        # Используем pyzipper с явным указанием параметров шифрования
                        with (
                            pyzipper.AESZipFile(
                                archive_path,
                                "w",
                                compression=pyzipper.ZIP_DEFLATED,  # Используем стандартное сжатие
                                encryption=pyzipper.WZ_AES
                                if password
                                else None,  # Шифрование только при наличии пароля
                            ) as zip_ref
                        ):
                            if password:
                                zip_ref.setpassword(password.encode())
                            for file in files:
                                zip_ref.write(file, os.path.basename(file))

                    elif archive_type == ".rar":
                        # Проверка наличия rar
                        if not self.check_rar_installed():
                            QMessageBox.warning(
                                self,
                                "Ошибка",
                                "Для создания .rar архивов необходимо установить rar.\n"
                                "Установите его с помощью команды: brew install rar",
                            )
                            return
                        # Используем команду rar для создания архива
                        rar_cmd = ["rar", "a", archive_path] + files
                        if password:
                            rar_cmd.insert(2, f"-p{password}")
                        subprocess.run(rar_cmd, check=True)
                    elif archive_type == ".7z":
                        with py7zr.SevenZipFile(
                            archive_path, "w", password=password
                        ) as seven_zip_ref:
                            for file in files:
                                seven_zip_ref.write(file, os.path.basename(file))
                    QMessageBox.information(
                        self, "Успех", "Архивация завершена успешно!"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Ошибка", f"Ошибка при архивации: {str(e)}"
                    )

    def check_rar_installed(self):
        """Проверяет, установлен ли rar."""
        try:
            subprocess.run(["rar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    swiss_k_config = SwissKnifeConfig()
    app.setWindowIcon(QIcon(swiss_k_config.icon_path))  # Устанавливаем иконку для приложения
    window = SimpleArchiverApp()
    window.setWindowIcon(QIcon(swiss_k_config.icon_path))  # Устанавливаем иконку для окна
    window.show()
    sys.exit(app.exec_())
