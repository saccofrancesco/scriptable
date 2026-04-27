from __future__ import annotations
from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Workshift")
        self.resize(1500, 960)
        self.setMinimumSize(1280, 700)
