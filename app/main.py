from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Movie, MovieCreate, MovieUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Movieland API", lifespan=lifespan)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "Movieland API"}

# returns all the movies in the DB - GET /movies
@app.get("/movies", response_model=List[Movie])
def list_movies(session: Session = Depends(get_session)) -> List[Movie]:
    movies = session.exec(select(Movie)).all()
    return movies

#Brings movie based on it's ID - GET /movies/{movie_id}
@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(
    movie_id: int,
    session: Session = Depends(get_session),
) -> Movie:
    movie = session.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


#Makes a new movie - POST /movies
@app.post("/movies", response_model=Movie, status_code=201)
def create_movie(
    movie: MovieCreate,
    session: Session = Depends(get_session),
) -> Movie:
    db_movie = Movie.model_validate(movie)

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie


#Updates movie{id} - PUT /movies/{movie_id}
@app.put("/movies/{movie_id}", response_model=Movie)
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    session: Session = Depends(get_session),
) -> Movie:
    """
    Update movie{id}
    """
    db_movie = session.get(Movie, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db_movie.title = movie.title
    db_movie.year = movie.year
    db_movie.description = movie.description

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

#delets movie{id} - DELETE /movies/{movie_id}
@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(
    movie_id: int,
    session: Session = Depends(get_session),
) -> None:
    """
    Delets movie{id}, returns 404 if it doesn't exist.
    """
    db_movie = session.get(Movie, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    session.delete(db_movie)
    session.commit()
