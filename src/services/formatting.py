from __future__ import annotations
from datetime import date, time


def format_month_label(value: date) -> str:
    return value.strftime("%B %Y")


def format_date_label(value: date) -> str:
    return f"{value.day} {value:%b %Y}"
