from sqlalchemy import Column, Integer, String, DateTime, Text

from db import Model
from db import TimestampMixin


class Task(TimestampMixin, Model):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name = Column(String, nullable=False)

    description = Column(Text, default="", server_default="")

    due_by = Column(DateTime(timezone=True), nullable=True)

    completed_at = Column(DateTime(timezone=True), nullable=True)
