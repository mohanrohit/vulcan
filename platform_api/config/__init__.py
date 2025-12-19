import os

env = os.getenv("VULCAN_ENV", "development")

if env == "development":
    from .development import *
elif env == "testing":
    from .testing import *
elif env == "production":
    from .production import *
else:
    from .default import *
