Movieland – FastAPI Movie Catalogue

A full CRUD API built with FastAPI, SQLModel, SQLite, uv, Pytest, Typer CLI, and Docker.

The API allows users to list, create, update, and delete movies through clean endpoints and optionally run inside Docker.

🧩 Project Overview
Component	Description
Framework	FastAPI
 – high-performance Python web framework
ORM Layer	SQLModel
 – SQLAlchemy + Pydantic
Database	SQLite – lightweight file-based DB (stored at data/movies.db)
Environment	uv – fast Python package manager / venv
Testing	pytest + FastAPI TestClient
CLI Utility	Typer – database initialization, seeding & CSV import
Container	Docker – run API in an isolated environment
🚀 Run Locally
1️⃣ Install dependencies
uv sync

2️⃣ Run the API
uv run uvicorn app.main:app --reload


The API will be available at:

Swagger UI → http://localhost:8000/docs

Movies list → http://localhost:8000/movies

Health check → http://localhost:8000/health

🧪 Running Tests
uv run pytest


Expected output:

8 passed in X.XXs

✔ What the tests validate:

POST /movies – creating a movie works

GET /movies – listing works

GET /movies/{id} – fetching works / returns 404 correctly

PUT /movies/{id} – updating works

DELETE /movies/{id} – deleting works

Year validation – rejects <1900 or >2100 (422)

🐳 Run with Docker
1️⃣ Build the Docker image
docker build -t movieland .

2️⃣ Run the container
docker run -p 8000:8000 movieland


Open in browser:

http://localhost:8000

http://localhost:8000/docs

http://localhost:8000/health

🎁 Bonus – Typer CLI Commands

Run any CLI command with:

uv run python cli.py <command>

🏗 Initialize database
uv run python cli.py initdb

🌱 Seed demo movies
uv run python cli.py seed-demo

📥 Import from CSV
uv run python cli.py load-csv data/tmdb_5000_movies.csv --limit 100


(Use --limit 0 to load the entire file.)

📁 Project Structure
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
 ├── Dockerfile
 ├── README.md
 ├── pyproject.toml
 └── uv.lock
