from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time
from uuid import uuid4


def _new_id() -> str:
    return uuid4().hex
