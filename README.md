📘 Movieland – FastAPI Movie Catalogue

Movieland is a tiny movie catalogue API built as part of EX1 – FastAPI Foundations.
The project uses FastAPI, SQLModel, SQLite, and Pytest to demonstrate a clean CRUD API with a simple data layer.

🚀 Features

✔ `GET /movies` – List all movies  
✔ `POST /movies` – Create a new movie  
✔ `GET /movies/{id}` – Fetch a single movie  
✔ `PUT /movies/{id}` – Update a movie  
✔ `DELETE /movies/{id}` – Delete a movie  
✔ `GET /health` – Service health check  
✔ Year validation (1900–2100)  
✔ **Bonus:** CLI with Typer (`initdb`, `seed-demo`, `load-csv`)  
✔ SQLite database stored at: `data/movies.db`  

🛠 Project Structure
Movieland/
 ├── app/
 │   ├── main.py
 │   ├── models.py
 │   ├── database.py
 │   └── __init__.py
 ├── data/
 │   └── tmdb_5000_movies.csv
 ├── tests/
 │   └── test_movies.py
 ├── cli.py
 ├── pyproject.toml
 ├── Dockerfile
 └── README.md

📦 Setup (Local Development):

1️⃣ Install dependencies
uv sync

2️⃣ Run the API
uv run uvicorn app.main:app --reload

API will be available at:
Swagger UI → http://localhost:8000/docs
Movies list → http://localhost:8000/movies
Health check → http://localhost:8000/health

🧪 Running Tests
uv run pytest

You should get output similar to:
8 passed in x.xxs

🐳 Docker Support
Build image:
docker build -t movieland .

Run container:
docker run -p 8000:8000 movieland

Container will serve:
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/health

🎁 Bonus – CLI Commands

Initialize database:
uv run python cli.py initdb

Seed demo movies:
uv run python cli.py seed-demo

Import from CSV:
uv run python cli.py load-csv data/tmdb_5000_movies.csv --limit 100
(Use --limit 0 to import the entire file.)