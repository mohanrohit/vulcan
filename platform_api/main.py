from flask import Flask
from flask import request

from datetime import datetime, timezone


from tasks import tasks_api


app = Flask(__name__)

app.register_blueprint(tasks_api)


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
    now = datetime.now(timezone.utc).isoformat()

    print(f"[{now}] request from {request.remote_addr}")

    return {
        "service": "tasks-api",
        "version": "0.1.0",
        "timestamp": now,
        "endpoints": {
            "tasks": "/tasks"
        }
    }
