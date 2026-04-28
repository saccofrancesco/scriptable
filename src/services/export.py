from __future__ import annotations
from datetime import date
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from ..domain.models import Schedule
from .calculations import build_employee_workloads
from .formatting import contrast_text_color, format_month_label


def _solid_fill(color_hex: str) -> PatternFill:
    return PatternFill(fill_type="solid", fgColor=color_hex.replace("#", "").upper())


def _font_color(color_hex: str) -> str:
    return f"FF{color_hex.replace('#', '').upper()}"


def _apply_border(cell) -> None:
    thin: Side = Side(style="thin", color="D7DCE3")
    cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)


def _style_header_row(sheet, row_index: int, columns: int) -> None:
    fill: PatternFill = PatternFill(fill_type="solid", fgColor="EAF0FF")
    for column in range(1, columns + 1):
        cell = sheet.cell(row=row_index, column=column)
        cell.font = Font(bold=True, color="0F172A")
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        _apply_border(cell)
