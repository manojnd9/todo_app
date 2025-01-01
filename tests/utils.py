from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

from todo_app.database import Base
from todo_app.main import app
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
