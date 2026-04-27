from __future__ import annotations
from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True, slots=True)
class EmployeeListItemVM:
    id: str
    full_name: str
    color_hex: str
    weekly_target_hours: float
    workdays: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class ShiftRowVM:
    id: str
    employee_id: str
    employee_name: str
    color_hex: str
    start_time: time
    end_time: time
    duration_hours: float


@dataclass(frozen=True, slots=True)
class CalendarDayVM:
    date: date
    in_current_month: bool
    is_today: bool
    is_selected: bool
    day_number: int
    employee_colors: tuple[str, ...]
    overflow_count: int
    tooltip: str
