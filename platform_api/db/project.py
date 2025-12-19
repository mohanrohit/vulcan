from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from db import Model
from db import TimestampMixin


class Project(TimestampMixin, Model):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, default="", server_default="")

    tasks = relationship("Task", back_populates="project")
