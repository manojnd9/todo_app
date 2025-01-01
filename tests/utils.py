from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from passlib.context import CryptContext

from todo_app.database import Base
from todo_app.main import app
from todo_app.models import ToDos, Users
from todo_app.routers.auth import bcrypt_context


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


@pytest.fixture(scope="function")
def test_user():
    user = Users(
        id=1,
        email="manoj@email.com",
        username="manojnd",
        first_name="manoj",
        last_name="d",
        hashed_password=bcrypt_context.hash("test1234"),
        is_active=True,
        role="admin",
        phone_number="+4912345678910",
    )

    db = TestSessionLocal()
    db.add(user)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM USERS;"))
        connection.commit()
