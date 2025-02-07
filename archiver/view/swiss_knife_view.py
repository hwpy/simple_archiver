# view.py
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


class SwissKnifeView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Swiss Knife")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.archive_type_label = QLabel("Тип архива:", self)
        layout.addWidget(self.archive_type_label)

        self.archive_type_combo = QComboBox(self)
        self.archive_type_combo.addItem(".zip")
        self.archive_type_combo.addItem(".rar")
        self.archive_type_combo.addItem(".7z")
        layout.addWidget(self.archive_type_combo)

        self.password_label = QLabel("Пароль (необязательно):", self)
        layout.addWidget(self.password_label)

        password_layout = QHBoxLayout()

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)

        self.toggle_password_btn = QPushButton("Видимость", self)
        self.toggle_password_btn.setCheckable(True)
        password_layout.addWidget(self.toggle_password_btn)

        layout.addLayout(password_layout)

        self.btn_unarchive = QPushButton("Разархивировать", self)
        layout.addWidget(self.btn_unarchive)

        self.btn_archive = QPushButton("Архивировать", self)
        layout.addWidget(self.btn_archive)

        self.setLayout(layout)

    def toggle_password_visibility(self, checked: bool):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def show_message(self, title: str, message: str, icon=QMessageBox.Information):
        if not title or not message:
            return  # Пропускаем, если заголовок или сообщение не указаны
        msg_box = QMessageBox(self)  # Указываем self как родительский виджет
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

    def get_archive_type(self):
        return self.archive_type_combo.currentText()

    def get_password(self):
        return self.password_input.text() or None

    def get_file_path(self, title: str, filter: str):
        return QFileDialog.getOpenFileName(self, title, "", filter)[0]

    def get_directory(self, title: str):
        return QFileDialog.getExistingDirectory(self, title)

    def get_files(self, title: str):
        return QFileDialog.getOpenFileNames(self, title, "", "Все файлы (*)")[0]

    def get_save_path(self, title: str, filter: str):
        return QFileDialog.getSaveFileName(self, title, "", filter)[0]
