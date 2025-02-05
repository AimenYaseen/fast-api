from sqlmodel import create_engine, SQLModel
from . import models

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_models():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_models()

"""
Run this file like this =>  python -m sql_model.main
"""