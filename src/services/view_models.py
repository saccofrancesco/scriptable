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
