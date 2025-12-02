# tests/test_movies.py

import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

# להוסיף את תיקיית השורש ל-PYTHONPATH לפני ביצוע import של app
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app  # noqa: E402
from app.database import engine, create_db_and_tables  # noqa: E402
from app.models import Movie  # noqa: E402


@pytest.fixture(scope="function", autouse=True)
def setup_db() -> Generator[None, None, None]:
    """
    לפני כל בדיקה:
    - לוודא שהטבלאות קיימות
    - לנקות את טבלת הסרטים
    """
    create_db_and_tables()

    with Session(engine) as session:
        movies = session.exec(select(Movie)).all()
        for m in movies:
            session.delete(m)
        session.commit()

    yield


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_health_endpoint(client: TestClient) -> None:
    """
    בדיקה ש־/health מחזיר סטטוס תקין ואת שם האפליקציה.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "Movieland API"


def test_list_movies_empty(client: TestClient) -> None:
    """
    בהתחלה, כשאין סרטים, GET /movies מחזיר רשימה ריקה.
    """
    response = client.get("/movies")
    assert response.status_code == 200
    assert response.json() == []


def test_get_movie_by_id(client: TestClient) -> None:
    """
    בדיקה שמוודאת שאפשר לקבל סרט לפי ID,
    וש-ID שלא קיים מחזיר 404.
    """
    payload = {
        "title": "Interstellar",
        "year": 2014,
        "description": "Space journey",
    }
    create_resp = client.post("/movies", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    movie_id = created["id"]

    get_resp = client.get(f"/movies/{movie_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()

    assert data["id"] == movie_id
    assert data["title"] == payload["title"]
    assert data["year"] == payload["year"]
    assert data["description"] == payload["description"]

    not_found_resp = client.get("/movies/999999")
    assert not_found_resp.status_code == 404


def test_create_movie(client: TestClient) -> None:
    """
    בדיקת יצירת סרט חדש (POST /movies).
    """
    payload = {
        "title": "The Matrix",
        "year": 1999,
        "description": "A hacker discovers the nature of reality.",
    }

    response = client.post("/movies", json=payload)
    data = response.json()

    assert response.status_code == 201
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["year"] == payload["year"]
    assert data["description"] == payload["description"]


def test_create_movie_rejects_year_too_old(client: TestClient) -> None:
    """
    שנה לפני 1900 צריכה להיכשל עם 422.
    """
    payload = {
        "title": "Very Old Movie",
        "year": 1500,
        "description": "Too old",
    }

    response = client.post("/movies", json=payload)
    assert response.status_code == 422


def test_create_movie_rejects_year_too_new(client: TestClient) -> None:
    """
    שנה אחרי 2100 צריכה להיכשל עם 422.
    """
    payload = {
        "title": "Far Future Movie",
        "year": 2500,
        "description": "Too new",
    }

    response = client.post("/movies", json=payload)
    assert response.status_code == 422


def test_update_movie(client: TestClient) -> None:
    """
    בדיקת עדכון סרט קיים (PUT /movies/{id}).
    """
    payload = {
        "title": "Old Title",
        "year": 2000,
        "description": "Old description",
    }
    create_resp = client.post("/movies", json=payload)
    movie_id = create_resp.json()["id"]

    updated = {
        "title": "New Title",
        "year": 2001,
        "description": "New description",
    }
    update_resp = client.put(f"/movies/{movie_id}", json=updated)
    data = update_resp.json()

    assert update_resp.status_code == 200
    assert data["id"] == movie_id
    assert data["title"] == updated["title"]
    assert data["year"] == updated["year"]
    assert data["description"] == updated["description"]


def test_delete_movie(client: TestClient) -> None:
    """
    בדיקת מחיקת סרט (DELETE /movies/{id}).
    """
    payload = {
        "title": "To be deleted",
        "year": 2010,
        "description": "Temp movie",
    }
    create_resp = client.post("/movies", json=payload)
    movie_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/movies/{movie_id}")
    assert delete_resp.status_code == 204

    list_resp = client.get("/movies")
    movies = list_resp.json()
    assert all(m["id"] != movie_id for m in movies)
