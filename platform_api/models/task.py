from typing import Optional

from datetime import datetime

from .model import Model


class Task(Model):
    id: int
    name: str
    description: Optional[str]
    due_by: Optional[datetime]
    completed_at: Optional[datetime]
