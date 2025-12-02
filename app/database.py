from collections.abc import Generator

from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///data/movies.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """יוצר את כל הטבלאות במסד הנתונים לפי המודלים."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Generator שמחזיר Session לעבודה מול מסד הנתונים (ל־FastAPI Depends).
    FastAPI יודע לסגור את ה־Session בסיום הבקשה.
    """
    with Session(engine) as session:
        yield session
