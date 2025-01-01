from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext

# Local imports
from todo_app.database import SessionLocal
from todo_app.models import Users
from todo_app.routers.auth import get_current_user

# Router to connect with main:app
router = APIRouter(prefix="/users", tags=["users"])


# Function to inject in db dependency
def get_db():
    # Instance of local session by session maker
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Create DB dependency
db_dependency = Annotated[Session, Depends(get_db)]

# Create User Dependency
user_dependency = Annotated[dict, Depends(get_current_user)]

# Function to hash the password!
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User Data Return Model
class UserDataReturn(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    role: str
    phone_number: str | None


# API End-Points


@router.get("/get_user", status_code=status.HTTP_200_OK, response_model=UserDataReturn)
async def get_user_data(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed!")
    user_data = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found!")

    return_user = {
        "id": user_data.id,
        "email": user_data.email,
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "is_active": user_data.is_active,
        "role": user_data.role,
        "phone_number": user_data.phone_number
    }

    return return_user


@router.put("/change_password/{new_password}", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(
    db: db_dependency, user: user_dependency, new_password: str = Path(min_length=5)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorisation Failed")

    # Get user data from Users DB Table
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user_model.hashed_password = bcrypt_context.hash(new_password)

    db.add(user_model)
    db.commit()


@router.put("/update_phone/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(db: db_dependency, user: user_dependency, phone_number: str=Path(min_length=10)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed!')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found!')
    
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
