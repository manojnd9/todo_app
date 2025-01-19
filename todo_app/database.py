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

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
"""URL to create a location of this DataBase on the FastAPI application.
"""

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
    ),
)
"""Engine to connect the database session with the fastAPI application.
"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Local Session that creates a DB in connection to the Engine that kind off gives a location on the network
where this DB exists.
"""

Base = declarative_base()
"""creates an object for the DB, which will be used to control the transactions with that DB"""
