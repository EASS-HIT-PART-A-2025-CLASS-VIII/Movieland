import csv
from pathlib import Path
from typing import Optional

import typer
from sqlmodel import Session

from app.database import create_db_and_tables, engine
from app.models import Movie

app = typer.Typer(help="Command line tools for Movieland API.")


# -------------------------------
# initdb - יצירת מסד נתונים
# -------------------------------
@app.command()
def initdb() -> None:
    """
    Create the database file (movies.db) and all tables.
    """
    create_db_and_tables()
    typer.echo("✅ Database and tables created successfully.")


# -------------------------------
# seed_demo - הזרעה בסיסית
# -------------------------------
@app.command()
def seed_demo() -> None:
    """
    Insert a handful of demo movies into the database.
    """
    demo_movies = [
        ("The Matrix", 1999, "A hacker discovers the nature of reality."),
        ("Inception", 2010, "Dream within a dream."),
        ("Interstellar", 2014, "A space journey to save humanity."),
        ("The Dark Knight", 2008, "Batman vs Joker."),
        ("Pulp Fiction", 1994, "Non-linear crime stories."),
        ("Spirited Away", 2001, "Girl enters the spirit world."),
        ("The Lord of the Rings", 2001, "The Fellowship begins."),
        ("Toy Story", 1995, "Toys come alive."),
    ]

    with Session(engine) as session:
        _insert_movies(session, demo_movies)

    typer.echo(f"✅ Inserted {len(demo_movies)} demo movies.")


# -------------------------------
# load_csv - טעינת CSV
# -------------------------------
@app.command()
def load_csv(
    csv_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Path to a CSV file containing movies.",
    ),
    title_column: str = typer.Option("title", help="Column containing the movie title."),
    year_column: str = typer.Option("release_date", help="Column with year or YYYY-MM-DD."),
    description_column: Optional[str] = typer.Option(
        "overview", help="Column with movie description."
    ),
    limit: Optional[int] = typer.Option(
        100, help="Maximum number of rows to import (0 = no limit)."
    ),
) -> None:
    """
    Load movies from CSV into the database.
    """
    movies_to_insert: list[tuple[str, int, Optional[str]]] = []

    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):

            # Respect limit
            if limit and limit > 0 and i > limit:
                break

            # Extract fields
            try:
                title = row[title_column].strip()
                year_raw = row[year_column].strip()

                # Year may be "1999-03-31" → take first 4 chars
                year = int(year_raw.split("-")[0])

                description = (
                    row[description_column].strip()
                    if description_column and row.get(description_column)
                    else None
                )

                if not title or not year:
                    continue

                movies_to_insert.append((title, year, description))

            except Exception:
                # Skip bad rows
                continue

    if not movies_to_insert:
        typer.echo("⚠ No valid rows found. Check column names.")
        raise typer.Exit(code=1)

    with Session(engine) as session:
        _insert_movies(session, movies_to_insert)


    typer.echo(f"✅ Imported {len(movies_to_insert)} movies from CSV.")


# -------------------------------
# Helper function - לא נקראת ישירות
# -------------------------------
def _insert_movies(session: Session, movies: list[tuple[str, int, Optional[str]]]) -> None:
    """
    Internal helper to insert list of (title, year, description) tuples.
    """
    for title, year, description in movies:
        session.add(Movie(title=title, year=year, description=description))
    session.commit()


# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    app()
