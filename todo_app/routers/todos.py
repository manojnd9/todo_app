# Third party imports
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

# Local imports
from todo_app.models import ToDos
from todo_app.database import SessionLocal
from todo_app.routers.auth import get_current_user

# Instantiate FastAPI Router
router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Jinja set up
templates = Jinja2Templates(directory="todo_app/templates")


# Pydantic basemodel to mimic Todos table
class TodosRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(gt=0, le=5)
    complete: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example_schema": {
                "title": "Water Plants",
                "description": "inside and outside",
                "priority": 5,
                "complete": False,
            }
        }
    }


### Pages ###


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todos = db.query(ToDos).filter(ToDos.owner_id == user.get("id")).all()
        return templates.TemplateResponse(
            "todo.html", {"request": request, "todos": todos, "user": user}
        )
    except Exception as e:
        print(f"Error: {e}")
        return redirect_to_login()


### End Points ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    # Validate user
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Authentication Failed!",
        )
    return db.query(ToDos).filter(ToDos.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    # Validate user
    if user is None:
        raise HTTPException(status_code=401, detail="User not authorised!")
    todo_model = (
        db.query(ToDos)
        .filter(ToDos.id == todo_id, ToDos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found!")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: db_dependency, user: user_dependency, todo_request: TodosRequest
):
    # Validate User
    if user is None:
        raise HTTPException(status_code=401, detail="User authentication failed!")

    todo_model = ToDos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    user: user_dependency,
    todo_request: TodosRequest,
    todo_id: int = Path(gt=0),
):
    # Validate the user
    if user is None:
        raise HTTPException(status_code=401, detail="User not authorised!")

    todo_model = (
        db.query(ToDos)
        .filter(ToDos.id == todo_id, ToDos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found!")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    # Validate the user
    if user is None:
        raise HTTPException(status_code=401, detail="User is not authorised!")

    todo_model = (
        db.query(ToDos)
        .filter(ToDos.id == todo_id, ToDos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found!")

    db.query(ToDos).filter(
        ToDos.id == todo_id, ToDos.owner_id == user.get("id")
    ).delete()
    db.commit()
