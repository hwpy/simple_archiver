import ctypes
from PyQt5.QtCore import Qt, QRect, QPoint, QRectF
from PyQt5.QtGui import QRegion, QPainterPath, QBrush, QColor, QPainter
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
)

from config.swiss_knife_config import SwissKnifeConfig
from utils.platform_settings import Platform
from swiss_knife import SwissKnifeApp


class UI:
    def __init__(self, app: SwissKnifeApp):
        # Устанавливаем размер и заголовок окна
        app.setWindowTitle(SwissKnifeConfig.app_name)

        app.setGeometry(100, 100, 400, 200)

        content_layout = QVBoxLayout()

        # Выпадающий список для выбора типа архива
        app.archive_type_label = QLabel("Тип архива:", app)
        content_layout.addWidget(app.archive_type_label)

        app.archive_type_combo = QComboBox(app)
        app.archive_type_combo.addItem(".zip")
        app.archive_type_combo.addItem(".rar")
        app.archive_type_combo.addItem(".7z")
        content_layout.addWidget(app.archive_type_combo)

        app.password_label = QLabel("Пароль (необязательно):", app)
        content_layout.addWidget(app.password_label)

        # Контейнер для поля ввода пароля и кнопки показа
        password_layout = QHBoxLayout()

        app.password_input = QLineEdit(app)
        app.password_input.setEchoMode(QLineEdit.Password)  # Скрываем пароль звездочками
        password_layout.addWidget(app.password_input)

        app.toggle_password_btn = QPushButton("Видимость", app)
        app.toggle_password_btn.setCheckable(True)
        app.toggle_password_btn.clicked.connect(app.toggle_password_visibility)
        password_layout.addWidget(app.toggle_password_btn)

        content_layout.addLayout(password_layout)

        app.btn_unarchive = QPushButton("Разархивировать", app)
        app.btn_unarchive.clicked.connect(app.unarchive)
        content_layout.addWidget(app.btn_unarchive)

        app.btn_archive = QPushButton("Архивировать", app)
        app.btn_archive.clicked.connect(app.archive)
        content_layout.addWidget(app.btn_archive)

class UIWindows(UI):
    def __init__(self, app: SwissKnifeApp):
        super.__init__()
        # Убираем стандартные рамки окна и делаем фон прозрачным
        app.setWindowFlags(Qt.FramelessWindowHint)
        app.setAttribute(Qt.WA_TranslucentBackground)

        # Применяем закругленные углы через WinAPI
        app.setWindowRoundedCorners()

        # Основной макет
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Панель заголовка с кнопками управления
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(0, 0, 0, 0)
        title_bar.setSpacing(10)

        # Кнопки управления окном
        app.btn_minimize = QPushButton("—", app)
        app.btn_minimize.setFixedSize(25, 25)
        app.btn_minimize.clicked.connect(app.showMinimized)

        app.btn_close = QPushButton("✕", app)
        app.btn_close.setFixedSize(25, 25)
        app.btn_close.clicked.connect(app.close)

        # Растягивающий элемент для выравнивания кнопок справа
        title_bar.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        title_bar.addWidget(app.btn_minimize)
        title_bar.addWidget(app.btn_close)


        main_layout.addLayout(title_bar)
        main_layout.addLayout(app.content_layout)
        app.setLayout(main_layout)

        # Стилизация кнопок управления
        app.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                border-radius: 3px;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton#btn_close:hover {
                background-color: #ff4444;
            }
        """)
        app.btn_close.setObjectName("btn_close")

    def mousePressEvent(self, event):
        """Перехват нажатия мыши для перемещения окна"""
        self.app.mouse_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        """Обработка перемещения окна"""
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.mouse_pos)
            self.app.move(self.app.x() + delta.x(), self.app.y() + delta.y())
            self.app.mouse_pos = event.globalPos()

    def setWindowRoundedCorners(self):
        """Применяет закругленные углы для окна через WinAPI."""
        try:
            hwnd = self.app.winId()
            DWMWA_WINDOW_CORNER_PREFERENCE = 33  # Параметр для закругленных углов
            DWM_WINDOW_CORNER_PREFERENCE = 2  # Закругленные углы
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWM_WINDOW_CORNER_PREFERENCE)),
                ctypes.sizeof(ctypes.c_int)
            )
        except Exception as e:
            print("Ошибка при установке закругленных углов:", e)

    def paintEvent(self, event):
        """Рисует закругленные углы и фон окна."""
        path = QPainterPath()
        radius = 5  # Радиус закругления
        rect = QRect(0, 0, self.app.width(), self.app.height())
        rect_f = QRectF(rect)  # Преобразование в QRectF
        path.addRoundedRect(rect_f, radius, radius)

        # Применяем маску для закругления
        region = QRegion(path.toFillPolygon().toPolygon())
        self.app.setMask(region)

        # Рисуем фон
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(path, QBrush(QColor("#2d2d2d")))

def gen_ui(app: SwissKnifeApp):
    ui = UI(app)
    if Platform.OS == Platform.Windows:
        ui = UIWindows(app)
    return ui