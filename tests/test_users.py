from tests.utils import (
    override_get_current_user,
    override_get_db,
    client,
    TestSessionLocal,
    test_user,
)

from todo_app.models import Users
from todo_app.routers.users import get_current_user, get_db
from todo_app.main import app
from todo_app.routers.auth import bcrypt_context

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/users/get_user")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "manoj@email.com"
    assert response.json()["username"] == "manojnd"
    assert response.json()["first_name"] == "manoj"
    assert response.json()["last_name"] == "d"
    assert response.json()["is_active"] == True
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "+4912345678910"


def test_change_password_success(test_user):
    response = client.put("/users/change_password/password1234")
    assert response.status_code == 204
    db = TestSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert bcrypt_context.verify("password1234", model.hashed_password)


def test_change_phone_number_success(test_user):
    response = client.put("/users/update_phone/01234555555")
    assert response.status_code == 204
