from typing import Optional

from .model import Model


class Project(Model):
    id: int
    name: str
    description: Optional[str]
