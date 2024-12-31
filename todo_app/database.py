from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://root:test1234!@127.0.0.1:3306/TodoApplicationDatabase"
)
"""URL to create a location of this DataBase on the FastAPI application.
    Give path where database is located.
    - For sqllite, if db is created locally within the application, the URL looks like this:
    sqlite:///./todosapp.db
    - For PostgreSQL
    postgresql://postgres:test1234!@localhost/TodoApplicationDatabase
"""

engine = create_engine(SQLALCHEMY_DATABASE_URL)
"""Engine to connect the database session with the fastAPI application"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Local Session that creates a DB in connection to the Engine that kind off gives a location on the network
where this DB exists.
"""

Base = declarative_base()
"""creates an object for the DB, which will be used to control the transactions with that DB"""
