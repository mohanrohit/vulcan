from typing import Optional

from datetime import datetime

# from pydantic import BaseModel
# from pydantic import ConfigDict

from .model import Model


class Task(Model):
    id: int
    # created_at: datetime
    # updated_at: datetime
    name: str
    description: Optional[str] = ""
    due_by: Optional[datetime]
    completed_at: Optional[datetime]
