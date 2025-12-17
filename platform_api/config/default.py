import os
import dotenv

dotenv.load_dotenv()


VULCAN_ENV = os.getenv("VULCAN_ENV", "development")

DEBUG = VULCAN_ENV == "development"

DATABASE_URL = os.getenv("DATABASE_URL")

SQLALCHEMY_ECHO = DEBUG  # log SQL queries in development
SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE", "5"))
SQLALCHEMY_MAX_OVERFLOW = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", "10"))
SQLALCHEMY_POOL_PRE_PING = True  # check connections before using
