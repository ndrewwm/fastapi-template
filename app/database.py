"""API Backend."""

from sqlmodel import create_engine, SQLModel


sqlite_file_name = "app/app.db"
sqlite_uri = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_uri, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
