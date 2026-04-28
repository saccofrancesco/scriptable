from __future__ import annotations
from calendar import monthrange
from collections.abc import Iterable
from datetime import date, datetime
from ..domain.models import Employee, Schedule, Shift
from .view_models import EmployeeListItemVM, EmployeeWorkloadVM, ShiftRowVM


def month_start(value: date) -> date:
    return value.replace(day=1)


def add_months(value: date, delta: int) -> date:
    month_index: int = value.month - 1 + delta
    year: int = value.year + month_index // 12
    month: int = month_index % 12 + 1
    last_day: tuple[int, int] = monthrange(year, month)[1]
    day: int = min(value.day, last_day)
    return date(year, month, day)
