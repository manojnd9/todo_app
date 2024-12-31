"""
Models is a way for SQLAlchemy to be able to understand what kind of database tables
we are going to be creating in the future! 

A database_model is the actual record that is inside a database table!
"""

from todo_app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class ToDos(Base):
    # This is for SQLAlchemy to know what to name the db table later on!
    __tablename__ = "todos"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
