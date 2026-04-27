from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from ..domain.models import Schedule


@dataclass(slots=True)
class ViewState:
    selected_month: date
    selected_day: date
