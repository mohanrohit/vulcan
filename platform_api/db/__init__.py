import config

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

engine = create_engine(
    config.DATABASE_URL,
    pool_pre_ping=config.SQLALCHEMY_POOL_PRE_PING,
    pool_size=config.SQLALCHEMY_POOL_SIZE,
    max_overflow=config.SQLALCHEMY_MAX_OVERFLOW,
    echo=config.SQLALCHEMY_ECHO
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def session():
    return Session()


from .model import Model

from .timestamp_mixin import TimestampMixin

from .project import Project
from .task import Task
