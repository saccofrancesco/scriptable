import sys
from PyQt6.QtWidgets import QApplication
from src.components.main_window import MainWindow


def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 500)
    window.show()

    sys.exit(app.exec())
