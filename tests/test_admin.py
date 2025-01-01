from starlette import status

from tests.utils import (
    override_get_current_user,
    override_get_db,
    client,
    TestSessionLocal,
    test_todo,
)

from todo_app.models import ToDos
from todo_app.routers.admin import get_current_user, get_db
from todo_app.main import app


# App dependencies overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == 200
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


def test_admin_delete_todos(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestSessionLocal()
    model = db.query(ToDos).filter(ToDos.id == 1).first()

    assert model is None
