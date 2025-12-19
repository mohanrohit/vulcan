import db

import zodic as z

from flask import Blueprint
from flask import request

from datetime import datetime, timezone

from models import Project, Task


projects_api = Blueprint("projects", __name__, url_prefix="/projects")


@projects_api.get("")
def list_projects():
    with db.session() as session:
        db_projects = session.query(db.Project).all()

        projects = [Project.model_validate(db_project).dict() for db_project in db_projects]

    return { "projects": projects }


@projects_api.post("")
def create_project():
    schema = z.object({
        "name": (
            z.string().transform(str.strip)
            .refine(lambda name: len(name) > 0, message="We need a name for your new project")
        ),
        "description": z.string().transform(str.strip).optional()
    })


    try:
        data = schema.parse(request.json)
    except z.ZodError as e:
        return { "error": e.issues[0]["message"] }, 422

    db_project = db.Project(
        name=data["name"],
        description=data.get("description")
    )

    with db.session() as session:
        session.add(db_project)
        session.commit()

        new_project = Project.model_validate(db_project)

    return new_project.dict(), 201


@projects_api.get("/<int:project_id>")
def get_project(project_id: int):
    with db.session() as session:
        db_project = session.query(db.Project).get(project_id)

        if db_project is None:
            return { "error": f"There is no project with id {project_id}" }, 404

        project = Project.model_validate(db_project)

        return project.dict()


@projects_api.patch("/<int:project_id>")
def update_project(project_id: int):
    schema = z.object({
        "name": (
            z.string().transform(str.strip).optional()
            .refine(lambda name: len(name) > 0, message="We need a name for the project")
        ),
        "description": z.string().transform(str.strip).optional(),
    })

    with db.session() as session:
        db_project = session.query(db.Project).get(project_id)

        if db_project is None:
            return { "error": f"There is no project with id {project_id}" }, 404

        try:
            data = schema.parse(request.json)
        except z.ZodError as e:
            return { "error": e.issues[0]["message"] }, 422

        for key, value in data.items():
            if hasattr(db_project, key):
                setattr(db_project, key, value)

        session.commit()

        updated_project = Project.model_validate(db_project)

    return updated_project.dict()


@projects_api.delete("/<int:project_id>")
def delete_project(project_id: int):
    with db.session() as session:
        db_project = session.query(db.Project).get(project_id)

        if db_project is None:
            return { "error": f"There is no project with id {project_id}" }, 404

        session.delete(db_project)
        session.commit()

        deleted_project = Project.model_validate(db_project)

    return deleted_project.dict(), 200


@projects_api.post("/<int:project_id>/tasks")
def create_task(project_id: int):
    schema = z.object({
        "name": (
            z.string().transform(str.strip)
            .refine(lambda name: len(name) > 0, message="We need a name for your new task")
        ),
        "description": z.string().transform(str.strip).optional(),
        "due_by": z.datetime().optional(),
        "completed_at": z.datetime().optional()
    })

    with db.session() as session:
        db_project = session.query(db.Project).filter(db.Project.id == project_id).first()

        if not db_project:
            return { "error": f"There is no project with id {project_id}" }, 404

        try:
            data = schema.parse(request.json)
        except z.ZodError as e:
            return { "error": e.issues[0]["message"] }, 422

        db_task = db.Task(
            name=data["name"],
            description=data.get("description"),
            due_by=data.get("due_by"),
            completed_at=data.get("completed_at"),
            project=db_project
        )

        session.add(db_task)
        session.commit()

        new_task = Task.model_validate(db_task)

    return new_task.dict(), 201


@projects_api.get("/<int:project_id>/tasks")
def list_tasks(project_id: int):
    with db.session() as session:
        db_project = session.query(db.Project).filter(db.Project.id == project_id).first()

        if not db_project:
            return { "error": f"There is no project with id {project_id}" }, 404

        db_tasks = session.query(db.Task).filter(db_project.id == project_id).all()

        project = Project.model_validate(db_project)

        tasks = [Task.model_validate(db_task).dict() for db_task in db_tasks]

    return {
        "project": { "id": project.id, "name": project.name },

        "tasks": tasks
    }
