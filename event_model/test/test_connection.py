import json
from datetime import datetime, timezone
import iso8601

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from event_model.pybossa_model.task_run import TaskRun
from event_model.pybossa_model.task import Task
from event_model.pybossa_model.project import Project
from event_model.pybossa_model.category import Category
from event_model.pybossa_model.user import User


def get_session(echo=False):
    engine = create_engine(
        "postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard",
        echo=echo,
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_task_run_events(session):
    task_run_query = session.query(TaskRun).order_by(TaskRun.id)
    for task_run in task_run_query:
        if is_task_completed(session, task_run.task_id, task_run.project_id):
            yield recreate_webhook(session, task_run, event="task_completed")
        else:
            yield recreate_webhook(session, task_run, event="in_progress")


def is_task_completed(conn, task_id, project_id):
    # TODO: Fix this old code to not use Python formatting for SQL queries.
    # Also: NEVER USE PYTHON FORMATTERS FOR SQL!
    sql_query = (
        (
            "select count(id) from task_run \
                 where task_run.task_id=%s and \
                 task_run.project_id=%s"
        )
        % (task_id, project_id)
    )
    n_answers = conn.scalar(sql_query)
    sql_query = (
        (
            "select n_answers from task \
                 where task.id=%s"
        )
        % task_id
    )
    task_n_answers = conn.scalar(sql_query)
    return (n_answers) >= task_n_answers


def recreate_webhook(session, task_run, event):
    project = (
        session.query(Project)
        .filter_by(id=task_run.project_id)
        .one()
    )
    created = iso8601.parse_date(task_run.created)
    finish_time = iso8601.parse_date(task_run.finish_time)
    elapsed_time = finish_time - created
    total_seconds = int(elapsed_time.total_seconds())
    payload = dict(
        event=event,
        project_short_name=project.short_name,
        project_id=project.id,
        task_id=task_run.task_id,
        task_run_id=task_run.id,
        user_id=task_run.user_id,
        created=created.isoformat(),
        finish_time=finish_time.isoformat(),
        elapsed_time=total_seconds,
        result_id=0,
        fired_at=datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    )
    return json.dumps(payload)


def test_has_pybossa_data(session):
    for user in session.query(User).order_by(User.id).limit(5):
        print(user.fullname)


if __name__ == "__main__":
    session = get_session(echo=False)
    #test_has_pybossa_data(session)
    for event_dict in get_task_run_events(session):
        print(event_dict)
