from typing import Optional

from sqlmodel import Field, SQLModel


class MovieBase(SQLModel):
    title: str
    year: int = Field(
        ge=1900,
        le=2100,
        description="Movie release year between 1900 and 2100",
    )
    description: Optional[str] = None

class Movie(MovieBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class MovieCreate(MovieBase):
    """מודל לקלט ביצירה (POST)."""
    pass

class MovieUpdate(MovieBase):
    """מודל לקלט בעדכון (PUT)."""
    pass
