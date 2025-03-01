# controller.py
from PyQt5.QtWidgets import QMessageBox


class SwissKnifeController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Подключаем сигналы к слотам
        self.view.btn_unarchive.clicked.connect(self.unarchive)
        self.view.btn_archive.clicked.connect(self.archive)
        self.view.toggle_password_btn.clicked.connect(self.toggle_password_visibility)

    def toggle_password_visibility(self):
        self.view.toggle_password_visibility(self.view.toggle_password_btn.isChecked())

    def unarchive(self):
        file_path = self.view.get_file_path("Выберите архив", "Архивы (*.7z *.zip *.rar)")
        if file_path:
            extract_path = self.view.get_directory("Выберите папку для извлечения")
            if extract_path:
                password = self.view.get_password()
                try:
                    success = self.model.unarchive(file_path, extract_path, password)
                    if success:
                        self.view.show_message("Успех", "Разархивирование завершено успешно!")
                except Exception as e:
                    self.view.show_message("Ошибка", str(e), QMessageBox.Critical)

    def archive(self):
        files = self.view.get_files("Выберите файлы для архивации")
        if files:
            archive_type = self.view.get_archive_type()
            archive_path = self.view.get_save_path("Сохранить архив как", f"Архивы (*{archive_type})")
            if archive_path:
                if not archive_path.endswith(archive_type):
                    archive_path += archive_type

                password = self.view.get_password()
                try:
                    success = self.model.archive(files, archive_path, archive_type, password)
                    if success:
                        self.view.show_message("Успех", "Архивация завершена успешно!")
                except Exception as e:
                    self.view.show_message("Ошибка", str(e), QMessageBox.Critical)
