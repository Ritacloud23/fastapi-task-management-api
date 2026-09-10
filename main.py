from fastapi import BackgroundTasks, FastAPI, HTTPException
from sqlmodel import select

from database import create_db_and_tables
from dependencies import APIKeyDep, PaginationDep, SessionDep
from models import (
    Task,
    TaskCreate,
    TaskPublic,
    TaskUpdate,
    User,
    UserCreate,
    UserPublic,
)

app = FastAPI(title="Task Management API")



@app.on_event("startup")
def on_startup():
    create_db_and_tables()



@app.get("/")
def home():
    return {
        "message": "Task Management API is running"
    }


@app.post(
    "/users",
    response_model=UserPublic,
)
def create_user(
    user: UserCreate,
    session: SessionDep,
    api_key: APIKeyDep,
):
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    "/users",
    response_model=list[UserPublic],
)
def get_users(
    session: SessionDep,
    pagination: PaginationDep,
):
    users = session.exec(
        select(User)
        .offset(pagination.offset)
        .limit(pagination.limit)
    ).all()

    return users


@app.get(
    "/users/{user_id}",
    response_model=UserPublic,
)
def get_user(
    user_id: int,
    session: SessionDep,
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user



@app.post(
    "/tasks",
    response_model=TaskPublic,
)
def create_task(
    task: TaskCreate,
    session: SessionDep,
    api_key: APIKeyDep,
):
    user = session.get(User, task.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    db_task = Task.model_validate(task)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@app.get(
    "/tasks",
    response_model=list[TaskPublic],
)
def get_tasks(
    pagination: PaginationDep,
    session: SessionDep,
):
    tasks = session.exec(
        select(Task)
        .offset(pagination.offset)
        .limit(pagination.limit)
    ).all()

    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=TaskPublic,
)
def get_task(
    task_id: int,
    session: SessionDep,
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task



def generate_completion_report(task_id: int):
    print(
        f"Completion report generated for task {task_id}"
    )


@app.put(
    "/tasks/{task_id}",
    response_model=TaskPublic,
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    background_tasks: BackgroundTasks,
    session: SessionDep,
    api_key: APIKeyDep,
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = task_update.model_dump(
        exclude_unset=True
    )

    task.sqlmodel_update(update_data)

    session.add(task)
    session.commit()
    session.refresh(task)

    if task.status == "completed":
        background_tasks.add_task(
            generate_completion_report,
            task.id,
        )

    return task




@app.delete(
    "/tasks/{task_id}",
)
def delete_task(
    task_id: int,
    session: SessionDep,
    api_key: APIKeyDep,
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    session.delete(task)
    session.commit()

    return {
        "message": "Task deleted successfully"
    }