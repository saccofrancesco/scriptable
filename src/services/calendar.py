from __future__ import annotations
from datetime import date, timedelta
from ..domain.models import Employee, Schedule, Shift
from .calculations import month_start
from .formatting import format_full_date_label, format_time_range
from .view_models import CalendarDayVM


def build_day_tooltip(schedule: Schedule, day: date) -> str:
    employees_by_id: dict[str, Employee] = {
        employee.id: employee for employee in schedule.employees
    }
    shifts: list[Shift] = sorted(
        [shift for shift in schedule.shifts if shift.shift_date == day],
        key=lambda shift: (
            shift.start_time,
            (
                employees_by_id.get(shift.employee_id).full_name.casefold()
                if employees_by_id.get(shift.employee_id)
                else "unknown"
            ),
        ),
    )
    if not shifts:
        return f"{format_full_date_label(day)}\nNo shifts planned."
    lines: list[str] = [format_full_date_label(day)]
    for shift in shifts:
        employee: Employee = employees_by_id.get(shift.employee_id)
        name: str = employee.full_name if employee else "Unknown employee"
        lines.append(f"{format_time_range(shift.start_time, shift.end_time)}  {name}")
    return "\n".join(lines)


def build_calendar_grid(
    schedule: Schedule,
    selected_month: date,
    selected_day: date,
    today: date | None = None,
) -> list[list[CalendarDayVM]]:
    today: date = today or date.today()
    first_day: date = month_start(selected_month)
    start_offset: int = first_day.weekday()
    grid_start: date = first_day - timedelta(days=start_offset)
    employees_by_id: dict[str, Employee] = {
        employee.id: employee for employee in schedule.employees
    }

    cells: list[CalendarDayVM] = list()
    for index in range(42):
        day: date = grid_start + timedelta(days=index)
        day_shifts: list[Shift] = [
            shift for shift in schedule.shifts if shift.shift_date == day
        ]
        unique_employee_ids: list[str] = list()
        for shift in sorted(
            day_shifts,
            key=lambda shift: (
                employees_by_id.get(shift.employee_id).full_name.casefold()
                if employees_by_id.get(shift.employee_id)
                else "unknown"
            ),
        ):
            if shift.employee_id not in unique_employee_ids:
                unique_employee_ids.append(shift.employee_id)
        colors: tuple[str, ...] = tuple(
            employees_by_id[employee_id].color_hex
            for employee_id in unique_employee_ids[:3]
            if employee_id in employees_by_id
        )
        overflow: int = max(len(unique_employee_ids) - 3, 0)
        cells.append(
            CalendarDayVM(
                date=day,
                in_current_month=day.month == first_day.month
                and day.year == first_day.year,
                is_today=day == today,
                is_selected=day == selected_day,
                day_number=day.day,
                employee_colors=colors,
                overflow_count=overflow,
                tooltip=build_day_tooltip(schedule, day),
            )
        )

    return [cells[index : index + 7] for index in range(0, 42, 7)]
