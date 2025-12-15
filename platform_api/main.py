from flask import Flask

from datetime import datetime, timezone


app = Flask(__name__)


@app.get("/health")
def health():
    now = datetime.now(timezone.utc).isoformat()

    # later: check db connection, redis, etc.
    return {
        "status": "ok",
        "timestamp": now
    }


@app.get("/")
def index():
    return { "message": "Hello, World!" }
