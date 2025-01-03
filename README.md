# ToDo App

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-FF7700?style=for-the-badge&logo=uvicorn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)

## Overview
This is a simple ToDo app backend built using:

- **Python**: Programming language for backend logic.
- **FastAPI**: Framework for building APIs.
- **Uvicorn**: ASGI server for running the application.
- **PostgreSQL**: Data Base Management System

The backend exposes APIs for managing ToDo tasks with basic operations like Create, Read, Update, and Delete (CRUD).

---

## Features
- Create a new ToDo task
- Retrieve all ToDo tasks or a single task
- Update an existing task
- Delete a task

---

## Requirements
Make sure you have the following installed:

- Python 3.11+
- Poetry for dependency management

---

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:your-username/todo-app.git
   cd todo-app
   ```

2. **Install dependencies**
   Using Poetry:
   ```bash
   poetry install
   ```

3. **Run the application**
   Start the Uvicorn server:
   ```bash
   poetry shell
   cd todo_app
   uvicorn main:app --reload
   ```

4. **Access the application**
   Open your browser and go to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

   Swagger-API documentation is available at:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

---

## License
This project is not yet licensed.
