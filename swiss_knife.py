# main.py
import sys

import qdarktheme
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from config.swiss_knife_config import SwissKnifeConfig
from controller.swiss_knife_controller import SwissKnifeController
from model.archiver_manager import ArchiveManager
from view.swiss_knife_view import SwissKnifeView


class SwissKnifeApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        qdarktheme.setup_theme("auto")
        self.config = SwissKnifeConfig()
        self.view = SwissKnifeView()
        self.model = ArchiveManager()
        self.controller = SwissKnifeController(self.view, self.model)

        self.view.setWindowIcon(QIcon(self.config.icon_path))
        self.view.show()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = SwissKnifeApp()
    app.run()
