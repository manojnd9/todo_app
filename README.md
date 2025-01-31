# ToDo App

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-FF7700?style=for-the-badge&logo=uvicorn&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)
![NeonDB](https://img.shields.io/badge/NeonDB-0093E9?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

## 🚀 Live Demo  

The application is deployed on **Render** and can be accessed here:  
🔗 [Live App](https://todo-app-deployment-8rb5.onrender.com)

## Overview  

This is a full-stack **ToDo App** with user authentication and task management.  
It includes a **FastAPI backend** and a **HTML frontend**, both managed in a monorepo.  
The backend is containerized with **Docker**, uses **NeonDB** for storage, and is deployed on **Render**.

Locally differnt database viz. SQLite or MySQL can be used.

---

## Features  

✔️ **User Authentication:** Sign up, log in, and manage sessions.  
✔️ **ToDo Management:** Create, update, and delete todos.  
✔️ **API Endpoints:** Built with FastAPI, documented via Swagger.  
✔️ **Database Storage:** Uses PostgreSQL (NeonDB) for persistence.  
✔️ **Dockerized Deployment:** Runs in a containerized environment.  
✔️ **CI/CD Integration:** Automates testing via GitHub Actions.  
✔️ **Live Deployment:** Hosted on Render (free tier) for public access.  


---

## Requirements
Make sure you have the following installed:

- Python 3.11+
- Poetry for dependency management

---

## Local Setup and Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:manojnd9/todo-app.git
   cd todo-app
   ```

2. **Install dependencies**
   Using Poetry:
   ```bash
   poetry install
   ```

3. **Create environment variables**
   Create a .env.dev file in the project root and add necessary keys.
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ```

4. **Run the application**
   Start the Uvicorn server:
   ```bash
   poetry shell
   cd todo_app
   uvicorn main:app --reload
   ```

5. **Access the application**
   Open your browser and go to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

   Swagger-API documentation is available at:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Acknowledgment  

This project was initially inspired by the course **"FastAPI - The Complete Course (Beginner + Advanced)"** by **Eric Roby**.  
I have extended the project by adding features such as:  
- Dockerized deployment 🐳  
- CI/CD workflow with GitHub Actions ✅  
- Deployment on Render with a NeonDB backend 🌍  
- Additional functionality and improvements  

This repository reflects my personal learning journey and enhancements beyond the original course material.  

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
