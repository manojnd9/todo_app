from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from todo_app.routers import auth, todos, admin, users
from todo_app.models import Base
from todo_app.database import engine

# Call the DB creator. This is effective only for the first time
# to create the local database within FastAPI application
Base.metadata.create_all(bind=engine)

# FastAPI main application
app = FastAPI()

# Jinja
templates = Jinja2Templates(directory="todo_app/templates")

# Mount the static files path to app, so that FastAPI knows where to
# find them
app.mount("/static", StaticFiles(directory="todo_app/static"), name="static")


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/health")
def health_check():
    return {"status": "Healthy"}


# Include the routers to enable main:app to route to
# defined endpoints
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
