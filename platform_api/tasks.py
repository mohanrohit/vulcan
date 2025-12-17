import db

import zodic as z

from flask import Blueprint
from flask import request

from datetime import datetime, timezone

from models import Task


tasks_api = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_api.get("")
def list_tasks():
    with db.session() as session:
        db_tasks = session.query(db.Task).all()

        tasks = [Task.model_validate(db_task).dict() for db_task in db_tasks]

    return { "tasks": tasks }


@tasks_api.post("")
def create_task():
    schema = z.object({
        "name": (
            z.string().transform(str.strip)
            .refine(lambda name: len(name) > 0, message="We need a name for your new task")
        ),
        "description": z.string().transform(str.strip).optional(),
        "due_by": z.datetime().optional(),
        "completed_at": z.datetime().optional()
    })


    try:
        data = schema.parse(request.json)
    except z.ZodError as e:
        return { "error": e.issues[0]["message"] }, 422

    db_task = db.Task(
        name=data["name"],
        description=data.get("description"),
        due_by=data.get("due_by"),
        completed_at=data.get("completed_at")
    )

    with db.session() as session:
        session.add(db_task)
        session.commit()

        new_task = Task.model_validate(db_task)

    return new_task.dict(), 201


@tasks_api.get("/<int:task_id>")
def get_task(task_id: int):
    with db.session() as session:
        db_task = session.query(db.Task).get(task_id)

        if db_task is None:
            return { "error": f"There is no task with id {task_id}" }, 404

        task = Task.model_validate(db_task)

        return task.dict()


@tasks_api.patch("/<int:task_id>")
def update_task(task_id: int):
    schema = z.object({
        "name": (
            z.string().transform(str.strip).optional()
            .refine(lambda name: len(name) > 0, message="We need a name for the task")
        ),
        "description": z.string().transform(str.strip).optional(),
        "due_by": z.datetime().optional(),
        "completed_at": z.datetime().optional()
    })

    with db.session() as session:
        db_task = session.query(db.Task).get(task_id)

        if db_task is None:
            return { "error": f"There is no task with id {task_id}" }, 404

        try:
            data = schema.parse(request.json)
        except z.ZodError as e:
            return { "error": e.issues[0]["message"] }, 422

        for key, value in data.items():
            if hasattr(db_task, key):
                setattr(db_task, key, value)

        session.commit()

        updated_task = Task.model_validate(db_task)

    return updated_task.dict()


@tasks_api.delete("/<int:task_id>")
def delete_task(task_id: int):
    with db.session() as session:
        db_task = session.query(db.Task).get(task_id)

        if db_task is None:
            return { "error": f"There is no task with id {task_id}" }, 404

        session.delete(db_task)
        session.commit()

        deleted_task = Task.model_validate(db_task)

    return deleted_task.dict(), 200


@tasks_api.put("/<int:task_id>/complete")
def mark_task_complete(task_id: int):
    schema = z.object({
        "completed_at": z.datetime().optional()
    })

    with db.session() as session:
        db_task = session.query(db.Task).filter(db.Task.id == task_id).first()

        if not db_task:
            return { "error": f"There is no task with id {task_id}" }, 404

        try:
            data = schema.parse(request.json)
        except z.ZodError as e:
            return { "error": e.issues[0]["message"] }, 422

        db_task.completed_at = data.get("completed_at") or datetime.now(tz=timezone.utc)

        session.commit()

        task = Task.model_validate(db_task)

    return task.dict()


@tasks_api.put("/<int:task_id>/incomplete")
def mark_task_incomplete(task_id: int):
    with db.session() as session:
        db_task = session.query(db.Task).filter(db.Task.id == task_id).first()

        if not db_task:
            return { "error": f"There is no task with id {task_id}" }, 404

        db_task.completed_at = None

        session.commit()

        task = Task.model_validate(db_task)

    return task.dict()
