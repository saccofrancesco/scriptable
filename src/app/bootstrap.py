from __future__ import annotations
import sys
from PyQt6.QtWidgets import QApplication
from ..ui.main_window import MainWindow
from ..ui.theme import apply_theme
from .controller import WorkshiftController


def create_application(
    argv: list[str] | None = None,
) -> tuple[QApplication, WorkshiftController, MainWindow]:
    app: QApplication = QApplication(argv or sys.argv)
    app.setApplicationName("Workshift")
    app.setOrganizationName("Workshift")
    app.setOrganizationDomain("local")
    app.setStyle("Fusion")
    apply_theme(app)
    controller: WorkshiftController = WorkshiftController()
    window: MainWindow = MainWindow(controller)
    return app, controller, window


def main(argv: list[str] | None = None) -> int:
    app, _, window = create_application(argv)
    window.show()
    return app.exec()
