from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from starlette import status
import pytest

from todo_app.database import Base
from todo_app.main import app
from todo_app.routers.auth import get_current_user
from todo_app.routers.todos import get_db
from todo_app.models import ToDos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
"""Test database URL"""

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
"""DB Engine to connect with test db"""

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Test session sqlalchemy db session connected with db engine"""
Base.metadata.create_all(bind=engine)


def override_get_db():
    """DB injection function to connect with local
    test db session. This is used to override the prod db dependency
    injecting function during testing,
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "manojndtest", "id": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)


# Todo test fixture


@pytest.fixture(scope="function")
def test_todo():
    todo = ToDos(
        title="Learn to code!",
        description="Need to learn!",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Learn to code!",
            "description": "Need to learn!",
            "priority": 5,
            "complete": False,
            "id": 1,
            "owner_id": 1,
        }
    ]


def test_read_single_todo(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "Learn to code!",
        "description": "Need to learn!",
        "priority": 5,
        "complete": False,
        "id": 1,
        "owner_id": 1,
    }


def test_read_single_todo_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found!"}


def test_create_todo(test_todo):

    request_data = {
        "title": "new todo!",
        "description": "new todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todo/", json=request_data)

    assert response.status_code == 201

    db = TestSessionLocal()

    model = db.query(ToDos).filter(ToDos.id == 2).first()

    assert model.title == request_data["title"]
    assert model.description == request_data["description"]
    assert model.priority == request_data["priority"]
    assert model.complete == request_data["complete"]


def test_update_todo(test_todo):
    # update data
    update_data = {
        "title": "Learn to code!",
        "description": "Need to learn!",
        "priority": 5,
        "complete": True,
    }
    response = client.put("/todo/1", json=update_data)
    assert response.status_code == 204

    db = TestSessionLocal()

    model = db.query(ToDos).filter(ToDos.id == 1).first()
    assert model.complete == update_data["complete"]


def test_update_todo_not_found(test_todo):
    # update data
    update_data = {
        "title": "Learn to code!",
        "description": "Need to learn!",
        "priority": 5,
        "complete": True,
    }
    response = client.put("/todo/2", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found!"}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == 204

    db = TestSessionLocal()

    model = db.query(ToDos).filter(ToDos.id == 1).first()

    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found!"}
