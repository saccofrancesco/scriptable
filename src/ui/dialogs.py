from __future__ import annotations
from datetime import date
from pathlib import Path
from typing import Sequence
from PyQt6.QtCore import QTime, Qt
from PyQt6.QtGui import QColor
from ..domain.models import Employee, Shift
from ..services.formatting import format_full_date_label
from .widgets import CardFrame, ColorSwatch, WeekdaySelector
from PyQt6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFileDialog,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class EmployeeDialog(QDialog):
    def __init__(
        self, employee: Employee | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Add person" if employee is None else "Edit person")
        self.setMinimumWidth(500)

        outer: QVBoxLayout = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(14)

        card: CardFrame = CardFrame(self, "dialogCard")
        card_layout: QVBoxLayout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(14)

        title: QLabel = QLabel(
            "Add person" if employee is None else "Edit person", self
        )
        title.setObjectName("panelTitle")

        form: QFormLayout = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(14)

        self._first_name: QLineEdit = QLineEdit(self)
        self._last_name: QLineEdit = QLineEdit(self)
        self._weekly_target: QDoubleSpinBox = QDoubleSpinBox(self)
        self._weekly_target.setRange(0.0, 200.0)
        self._weekly_target.setDecimals(2)
        self._weekly_target.setSingleStep(0.5)
        self._weekly_target.setSuffix(" h")

        self._lunch_break_hours: QDoubleSpinBox = QDoubleSpinBox(self)
        self._lunch_break_hours.setRange(0.0, 8.0)
        self._lunch_break_hours.setDecimals(2)
        self._lunch_break_hours.setSingleStep(0.25)
        self._lunch_break_hours.setSuffix(" h")
        self._lunch_break_hours.setValue(1.0)

        lunch_box: QWidget = QWidget(self)
        lunch_layout: QVBoxLayout = QVBoxLayout(lunch_box)
        lunch_layout.setContentsMargins(0, 0, 0, 0)
        lunch_layout.setSpacing(4)
        lunch_layout.addWidget(self._lunch_break_hours)
        lunch_hint: QLabel = QLabel(
            "Deducted from shifts when lunch is included in the day.",
            self,
        )
        lunch_hint.setObjectName("rowMeta")
        lunch_hint.setWordWrap(True)
        lunch_layout.addWidget(lunch_hint)

        self._weekday_selector: WeekdaySelector = WeekdaySelector(self)
        self._weekday_selector.selection_changed.connect(self._on_selection_changed)

        self._color_hex: str = "#2563eb"
        color_row: QHBoxLayout = QHBoxLayout()
        color_row.setSpacing(10)
        self._color_swatch: ColorSwatch = ColorSwatch(14, self)
        self._color_label: QLabel = QLabel(self._color_hex, self)
        self._color_label.setObjectName("rowMeta")
        self._color_button: QPushButton = QPushButton("Choose color", self)
        self._color_button.clicked.connect(lambda _=False: self._choose_color())
        color_row.addWidget(self._color_swatch)
        color_row.addWidget(self._color_label)
        color_row.addStretch(1)
        color_row.addWidget(self._color_button)
        color_widget: QWidget = QWidget(self)
        color_widget.setLayout(color_row)

        form.addRow("First name", self._first_name)
        form.addRow("Last name", self._last_name)
        form.addRow("Weekly target", self._weekly_target)
        form.addRow("Lunch break", lunch_box)
        form.addRow("Working days", self._weekday_selector)
        form.addRow("Color", color_widget)

        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok,
            parent=self,
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Save")
        button_box.button(QDialogButtonBox.StandardButton.Ok).setObjectName(
            "primaryButton"
        )
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setObjectName(
            "secondaryButton"
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(button_box)
        outer.addWidget(card)

        if employee is not None:
            self.set_employee(employee)
        else:
            self._weekday_selector.set_selected_days((0, 1, 2, 3, 4))

    def set_employee(self, employee: Employee) -> None:
        self._first_name.setText(employee.first_name)
        self._last_name.setText(employee.last_name)
        self._weekly_target.setValue(employee.weekly_target_hours)
        self._lunch_break_hours.setValue(employee.lunch_break_hours)
        self._weekday_selector.set_selected_days(employee.workdays)
        self._set_color(employee.color_hex)

    def _set_color(self, color_hex: str) -> None:
        self._color_hex: str = color_hex.lower()
        self._color_swatch.set_color(self._color_hex)
        self._color_label.setText(self._color_hex)

    def _choose_color(self) -> None:
        current: QColor = QColor(self._color_hex)
        color: QColorDialog = QColorDialog.getColor(
            current, self, "Choose employee color"
        )
        if color.isValid():
            self._set_color(color.name())

    def _on_selection_changed(self) -> None:
        # No-op for now; the button state is validated on save.
        pass

    def get_values(self) -> dict[str, object]:
        return {
            "first_name": self._first_name.text(),
            "last_name": self._last_name.text(),
            "weekly_target_hours": float(self._weekly_target.value()),
            "lunch_break_hours": float(self._lunch_break_hours.value()),
            "workdays": self._weekday_selector.selected_days(),
            "color_hex": self._color_hex,
        }

    def accept(self) -> None:
        if not self._first_name.text().strip():
            QMessageBox.warning(self, "Missing data", "First name is required.")
            return
        if not self._last_name.text().strip():
            QMessageBox.warning(self, "Missing data", "Last name is required.")
            return
        if not self._weekday_selector.selected_days():
            QMessageBox.warning(self, "Missing data", "Select at least one workday.")
            return
        super().accept()


class ShiftDialog(QDialog):
    def __init__(
        self,
        selected_day: date,
        employees: Sequence[Employee],
        shift: Shift | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._shift_date: date = shift.shift_date if shift is not None else selected_day
        self.setWindowTitle("Add shift" if shift is None else "Edit shift")
        self.setMinimumWidth(470)

        outer: QVBoxLayout = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(14)

        card: CardFrame = CardFrame(self, "dialogCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(14)

        title: QLabel = QLabel("Add shift" if shift is None else "Edit shift", self)
        title.setObjectName("panelTitle")
        subtitle: QLabel = QLabel(
            f"Selected day: {format_full_date_label(self._shift_date)}",
            self,
        )
        subtitle.setObjectName("panelSubtitle")
        subtitle.setWordWrap(True)

        form: QFormLayout = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(14)

        self._employee_combo: QComboBox = QComboBox(self)
        self._employee_combo.setMinimumWidth(220)
        for employee in employees:
            self._employee_combo.addItem(employee.full_name, employee.id)

        self._start_time: QTimeEdit = QTimeEdit(self)
        self._start_time.setDisplayFormat("HH:mm")
        self._start_time.setTime(QTime(9, 0))

        self._end_time: QTimeEdit = QTimeEdit(self)
        self._end_time.setDisplayFormat("HH:mm")
        self._end_time.setTime(QTime(18, 0))

        self._includes_lunch_break: QCheckBox = QCheckBox("Lunch break included", self)
        self._includes_lunch_break.setChecked(True)
        self._includes_lunch_break.setCursor(Qt.CursorShape.PointingHandCursor)
        self._includes_lunch_break.setToolTip(
            "Leave this checked for full-day shifts where lunch is part of the workday."
        )

        lunch_box: QWidget = QWidget(self)
        lunch_layout: QVBoxLayout = QVBoxLayout(lunch_box)
        lunch_layout.setContentsMargins(0, 0, 0, 0)
        lunch_layout.setSpacing(4)
        lunch_layout.addWidget(self._includes_lunch_break)
        lunch_hint = QLabel(
            "Uncheck it for morning or afternoon shifts where lunch happens outside work.",
            self,
        )
        lunch_hint.setObjectName("rowMeta")
        lunch_hint.setWordWrap(True)
        lunch_layout.addWidget(lunch_hint)

        form.addRow("Employee", self._employee_combo)
        form.addRow("Start time", self._start_time)
        form.addRow("End time", self._end_time)
        form.addRow("Lunch break", lunch_box)

        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok,
            parent=self,
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Save")
        button_box.button(QDialogButtonBox.StandardButton.Ok).setObjectName(
            "primaryButton"
        )
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setObjectName(
            "secondaryButton"
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addLayout(form)
        card_layout.addWidget(button_box)
        outer.addWidget(card)

        if shift is not None:
            self.set_shift(shift)

        self._employee_combo.setEnabled(bool(employees))

    def set_shift(self, shift: Shift) -> None:
        self._shift_date = shift.shift_date
        self._find_and_select_employee(shift.employee_id)
        self._start_time.setTime(QTime(shift.start_time.hour, shift.start_time.minute))
        self._end_time.setTime(QTime(shift.end_time.hour, shift.end_time.minute))
        self._includes_lunch_break.setChecked(shift.includes_lunch_break)

    def _find_and_select_employee(self, employee_id: str) -> None:
        for index in range(self._employee_combo.count()):
            if self._employee_combo.itemData(index) == employee_id:
                self._employee_combo.setCurrentIndex(index)
                return

    def get_values(self) -> dict[str, object]:
        return {
            "employee_id": self._employee_combo.currentData(),
            "shift_date": self._shift_date,
            "start_time": self._start_time.time().toPyTime(),
            "end_time": self._end_time.time().toPyTime(),
            "includes_lunch_break": self._includes_lunch_break.isChecked(),
        }

    def accept(self) -> None:
        if self._employee_combo.count() == 0:
            QMessageBox.warning(
                self, "Missing data", "Add at least one person before creating shifts."
            )
            return
        super().accept()


class DeleteConfirmDialog(QDialog):
    def __init__(self, title: str, message: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(460)

        outer: QVBoxLayout = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(14)

        card: CardFrame = CardFrame(self, "dialogCard")
        card_layout: QVBoxLayout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        title_label: QLabel = QLabel(title, self)
        title_label.setObjectName("panelTitle")
        message_label: QLabel = QLabel(message, self)
        message_label.setObjectName("panelSubtitle")
        message_label.setWordWrap(True)

        warning_label: QLabel = QLabel("This action cannot be undone.", self)
        warning_label.setObjectName("dangerHint")
        warning_label.setWordWrap(True)

        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok,
            parent=self,
        )
        self.confirm_button: QPushButton | None = button_box.button(
            QDialogButtonBox.StandardButton.Ok
        )
        self.confirm_button.setText("Delete")
        self.confirm_button.setObjectName("dangerButton")
        self.cancel_button: QPushButton | None = button_box.button(
            QDialogButtonBox.StandardButton.Cancel
        )
        self.cancel_button.setObjectName("secondaryButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        card_layout.addWidget(title_label)
        card_layout.addWidget(message_label)
        card_layout.addWidget(warning_label)
        card_layout.addWidget(button_box)
        outer.addWidget(card)


class InfoDialog(QDialog):
    def __init__(
        self,
        title: str,
        message: str,
        parent: QWidget | None = None,
        button_text: str = "Close",
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(460)

        outer: QVBoxLayout = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(14)

        card: CardFrame = CardFrame(self, "dialogCard")
        card_layout: QVBoxLayout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        title_label: QLabel = QLabel(title, self)
        title_label.setObjectName("panelTitle")
        message_label: QLabel = QLabel(message, self)
        message_label.setObjectName("panelSubtitle")
        message_label.setWordWrap(True)

        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok, parent=self
        )
        self.confirm_button: QPushButton | None = button_box.button(
            QDialogButtonBox.StandardButton.Ok
        )
        self.confirm_button.setText(button_text)
        self.confirm_button.setObjectName("primaryButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        card_layout.addWidget(title_label)
        card_layout.addWidget(message_label)
        card_layout.addWidget(button_box)
        outer.addWidget(card)


class ExportDialog(QDialog):
    def __init__(self, default_path: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export .xlsx")
        self.setMinimumWidth(560)
        self._file_path: str = ""

        outer: QVBoxLayout = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(14)

        card: CardFrame = CardFrame(self, "dialogCard")
        card_layout: QVBoxLayout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(14)

        title: QLabel = QLabel("Export .xlsx", self)
        title.setObjectName("panelTitle")

        form: QFormLayout = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setVerticalSpacing(12)
        form.setHorizontalSpacing(14)

        self._path_edit: QLineEdit = QLineEdit(default_path, self)
        self._path_edit.setClearButtonEnabled(True)
        self._path_edit.setPlaceholderText("Choose a destination for the workbook")

        browse_button: QPushButton = QPushButton("Browse", self)
        browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_button.setObjectName("secondaryButton")
        browse_button.clicked.connect(lambda _=False: self._choose_file())

        path_row: QWidget = QWidget(self)
        path_row_layout: QHBoxLayout = QHBoxLayout(path_row)
        path_row_layout.setContentsMargins(0, 0, 0, 0)
        path_row_layout.setSpacing(8)
        path_row_layout.addWidget(self._path_edit, 1)
        path_row_layout.addWidget(browse_button)

        path_hint: QLabel = QLabel("The file will be saved as .xlsx.", self)
        path_hint.setObjectName("rowMeta")
        path_hint.setWordWrap(True)

        path_box: QWidget = QWidget(self)
        path_box_layout: QVBoxLayout = QVBoxLayout(path_box)
        path_box_layout.setContentsMargins(0, 0, 0, 0)
        path_box_layout.setSpacing(4)
        path_box_layout.addWidget(path_row)
        path_box_layout.addWidget(path_hint)

        form.addRow("File", path_box)

        button_box: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok,
            parent=self,
        )
        self.confirm_button: QPushButton | None = button_box.button(
            QDialogButtonBox.StandardButton.Ok
        )
        self.confirm_button.setText("Export")
        self.confirm_button.setObjectName("primaryButton")
        self.cancel_button: QPushButton | None = button_box.button(
            QDialogButtonBox.StandardButton.Cancel
        )
        self.cancel_button.setObjectName("secondaryButton")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(button_box)
        outer.addWidget(card)

    def _choose_file(self) -> None:
        current: str = self._path_edit.text().strip()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Choose export location",
            current,
            "Excel Workbook (*.xlsx)",
        )
        if file_path:
            self._path_edit.setText(file_path)

    def file_path(self) -> str:
        return self._file_path

    def accept(self) -> None:
        raw_path: str = self._path_edit.text().strip()
        if not raw_path:
            QMessageBox.warning(
                self, "Missing data", "Choose a file name for the export."
            )
            return
        path: Path = Path(raw_path).expanduser()
        if path.suffix.lower() != ".xlsx":
            path: Path = path.with_suffix(".xlsx")
        self._file_path = str(path)
        super().accept()
