from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the .env.dev file in the root directory
dotenv_path = os.path.join(current_dir, "..", ".env.dev")

# Load the local environment attributes
load_dotenv(dotenv_path=dotenv_path)

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")
"""URL to create a location of this DataBase on the FastAPI application.
    Choose the relevant database URL from the env file.
    Available dbs...
    SQLLITE_DATABASE_URL, POSTGRESQL_DATABASE_URL, MYSQL_DATABASE_URL
"""

engine = create_engine(SQLALCHEMY_DATABASE_URL)
"""Engine to connect the database session with the fastAPI application.
    If SQLLite is used as DB, make sure to add these connect_args to the engine:
    connect_args={"check_same_thread": False}
"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Local Session that creates a DB in connection to the Engine that kind off gives a location on the network
where this DB exists.
"""

Base = declarative_base()
"""creates an object for the DB, which will be used to control the transactions with that DB"""
