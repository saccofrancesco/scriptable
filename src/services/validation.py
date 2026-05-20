from __future__ import annotations
from datetime import date, time
from ..domain.models import Employee, Schedule, Shift


class WorkshiftError(ValueError):
    """User-facing validation error."""


def validate_employee_fields(
    first_name: str,
    last_name: str,
    monthly_target_hours: float,
    lunch_break_hours: float = 1.0,
) -> tuple[str, str, float]:
    first_name: str = first_name.strip()
    last_name: str = last_name.strip()
    if not first_name:
        raise WorkshiftError("First name is required.")
    if not last_name:
        raise WorkshiftError("Last name is required.")
    if monthly_target_hours < 0:
        raise WorkshiftError("Monthly target hours cannot be negative.")
    if lunch_break_hours < 0:
        raise WorkshiftError("Lunch break hours cannot be negative.")
    return first_name, last_name, monthly_target_hours


def require_employee(schedule: Schedule, employee_id: str) -> Employee:
    for employee in schedule.employees:
        if employee.id == employee_id:
            return employee
    raise WorkshiftError("Selected employee no longer exists.")


def require_shift(schedule: Schedule, shift_id: str) -> Shift:
    for shift in schedule.shifts:
        if shift.id == shift_id:
            return shift
    raise WorkshiftError("Selected shift no longer exists.")


def validate_shift_fields(
    schedule: Schedule,
    employee_id: str,
    shift_date: date,
    start_time: time,
    end_time: time,
    *,
    shift_id: str | None = None,
) -> None:
    require_employee(schedule, employee_id)
    if end_time <= start_time:
        raise WorkshiftError("Shift end time must be after start time.")

    for shift in schedule.shifts:
        if shift.id == shift_id:
            continue
        if shift.employee_id != employee_id:
            continue
        if shift.shift_date != shift_date:
            continue
        overlaps = start_time < shift.end_time and shift.start_time < end_time
        if overlaps:
            raise WorkshiftError(
                "This shift overlaps another shift for the same employee."
            )
