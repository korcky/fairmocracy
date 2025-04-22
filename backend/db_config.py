from database import AbstractEngine, SQLEngine


DB_ENGINE = SQLEngine(url=f"sqlite:///database.sqlite3")


def get_db_engine() -> AbstractEngine:
    return DB_ENGINE
