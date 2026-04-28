from __future__ import annotations
from datetime import date, time
from PyQt6.QtCore import QObject, pyqtSignal
from ..domain.models import Employee, Schedule, Shift
from ..services.calculations import (
    add_months,
    build_daily_shift_rows,
    build_employee_workloads,
    employee_display_rows,
)
from ..services.calendar import build_calendar_grid
from ..services.export import export_schedule_xlsx
from ..services.formatting import format_month_label
from ..services.validation import (
    WorkshiftError,
    require_employee,
    require_shift,
    validate_employee_fields,
    validate_shift_fields,
)
from .state import SessionState, ViewState, create_default_view_state
