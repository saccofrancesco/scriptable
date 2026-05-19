from __future__ import annotations
from pathlib import Path
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication

APP_STYLESHEET: str = """
* {
    font-family: "Avenir Next", "Segoe UI", "Inter", "Helvetica Neue", "Arial";
    font-size: 12px;
    color: #0f172a;
}

QWidget {
    background: transparent;
}

QMainWindow {
    background: #eef2f7;
}

QDialog {
    background: #eef2f7;
}

QFrame#panelFrame,
QFrame#cardFrame,
QFrame#dialogCard {
    background: #ffffff;
    border: 1px solid #d9e0ea;
    border-radius: 16px;
}

QLabel#panelTitle {
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
}

QLabel#panelSubtitle {
    color: #64748b;
    font-size: 11px;
}

QLabel#rowTitle {
    font-weight: 600;
    color: #0f172a;
}

QLabel#workloadTitle {
    font-size: 12px;
    font-weight: 600;
    color: #0f172a;
}

QLabel#rowMeta {
    color: #64748b;
    font-size: 11px;
}

QLabel#workloadMeta {
    color: #64748b;
    font-size: 10px;
}

QLabel#calendarDayLabel {
    font-size: 10px;
    font-weight: 600;
    color: #0f172a;
}

QLabel#calendarOverflow {
    color: #475569;
    background: #e2e8f0;
    padding: 0 4px;
    border-radius: 6px;
    font-size: 10px;
}

QLabel#emptyState {
    color: #64748b;
    font-style: italic;
    padding: 8px 4px;
}

QLabel#dangerHint {
    color: #be123c;
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-radius: 10px;
    padding: 6px 8px;
    font-size: 11px;
}

QPushButton,
QToolButton,
QLineEdit,
QDoubleSpinBox,
QTimeEdit,
QComboBox {
    border: 1px solid #d8e0ea;
    border-radius: 8px;
    background: #ffffff;
}

QPushButton {
    padding: 6px 10px;
}

QPushButton:hover,
QToolButton:hover {
    background: #f1f5f9;
}

QPushButton:pressed,
QToolButton:pressed {
    background: #e2e8f0;
}

QPushButton#primaryButton {
    background: #2563eb;
    border-color: #2563eb;
    color: #ffffff;
}

QPushButton#primaryButton:hover {
    background: #1d4ed8;
}

QPushButton#dangerButton {
    background: #fff1f2;
    border-color: #fecdd3;
    color: #be123c;
}

QPushButton#dangerButton:hover {
    background: #ffe4e6;
}

QPushButton#secondaryButton {
    background: #ffffff;
    border-color: #d8e0ea;
    color: #0f172a;
}

QPushButton#secondaryButton:hover {
    background: #f8fafc;
}

QToolButton#weekdayButton {
    padding: 5px 8px;
    border-radius: 999px;
    min-width: 40px;
}

QToolButton#weekdayButton:checked {
    background: #dbeafe;
    border-color: #2563eb;
    color: #1d4ed8;
}

QLineEdit,
QDoubleSpinBox,
QTimeEdit,
QComboBox {
    padding: 5px 8px;
}

QLineEdit:focus,
QDoubleSpinBox:focus,
QTimeEdit:focus,
QComboBox:focus {
    border-color: #2563eb;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    width: 0px;
    height: 0px;
}

QComboBox::drop-down:hover {
    background: #f1f5f9;
}

QComboBox QAbstractItemView {
    border: 1px solid #d8e0ea;
    background: #ffffff;
    selection-background-color: #dbeafe;
    selection-color: #0f172a;
    border-radius: 12px;
    outline: 0;
    padding: 4px;
    show-decoration-selected: 0;
}

QComboBox QAbstractItemView::item {
    min-height: 22px;
    padding: 4px 10px;
    margin: 2px 4px;
    border-radius: 8px;
}

QComboBox QAbstractItemView::item:hover {
    background: #f1f5f9;
}

QComboBox QAbstractItemView::item:selected {
    background: #dbeafe;
    border-radius: 8px;
}

QAbstractSpinBox {
    padding-right: 24px;
}

QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    subcontrol-origin: border;
    width: 18px;
    border: none;
    background: transparent;
}

QAbstractSpinBox::up-button {
    subcontrol-position: top right;
    border-top-right-radius: 7px;
}

QAbstractSpinBox::down-button {
    subcontrol-position: bottom right;
    border-bottom-right-radius: 7px;
}

QAbstractSpinBox::up-arrow,
QAbstractSpinBox::down-arrow {
    width: 0px;
    height: 0px;
    image: none;
}

QAbstractSpinBox::up-button:hover,
QAbstractSpinBox::down-button:hover {
    background: #f1f5f9;
}

QAbstractSpinBox::up-button:pressed,
QAbstractSpinBox::down-button:pressed {
    background: #e2e8f0;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background: #cbd5e1;
    border-radius: 5px;
    min-width: 24px;
}

QScrollBar::handle:horizontal:hover {
    background: #94a3b8;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 5px;
    border: 1px solid #cbd5e1;
    background: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #94a3b8;
    background: #f8fafc;
}

QCheckBox::indicator:checked {
    border-color: #2563eb;
    background-color: #2563eb;
    background-image: url("CHECK_SVG_PATH");
    background-repeat: no-repeat;
    background-position: center;
}

QCheckBox::indicator:checked:hover {
    border-color: #1d4ed8;
    background-color: #1d4ed8;
    background-image: url("CHECK_SVG_PATH");
    background-repeat: no-repeat;
    background-position: center;
}

QCheckBox::indicator:disabled {
    border-color: #e2e8f0;
    background: #f8fafc;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QScrollBar::add-line,
QScrollBar::sub-line {
    height: 0px;
}

QProgressBar {
    background: #e2e8f0;
    border: 1px solid #d9e0ea;
    border-radius: 10px;
    text-align: left;
    min-height: 10px;
    padding: 1px;
}

QProgressBar::chunk {
    background: #2563eb;
    border-radius: 8px;
}
"""


def apply_theme(app: QApplication) -> None:
    check_svg: str = (Path(__file__).resolve().parent / "assets" / "check.svg").as_posix()
    stylesheet: str = APP_STYLESHEET.replace("CHECK_SVG_PATH", check_svg)
    app.setFont(QFont("Helvetica Neue"))
    palette: QPalette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#eef2f7"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f8fafc"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#0f172a"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#0f172a"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#2563eb"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)
    app.setStyleSheet(stylesheet)
