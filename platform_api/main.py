from flask import Flask
from flask import Blueprint

from datetime import datetime, timezone


from projects import projects_api
from tasks import tasks_api


app = Flask(__name__)

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api_v1.register_blueprint(projects_api)
api_v1.register_blueprint(tasks_api)

app.register_blueprint(api_v1)


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

    return {
        "service": "platform_api",
        "version": "0.1.0",
        "timestamp": now,
        "endpoints": {
            "projects": "/projects",
            "tasks": "/tasks"
        }
    }
