from fastapi import FastAPI

from todo_app.routers import auth, todos, admin, users
from todo_app.models import Base
from todo_app.database import engine

# Call the DB creator. This is effective only for the first time
# to create the local database within FastAPI application
Base.metadata.create_all(bind=engine)


# FastAPI main application
app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "Healthy"}


# Include the routers to enable main:app to route to
# defined endpoints
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
