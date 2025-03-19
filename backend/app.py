from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import Response
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from models import Game, VotingEvent

app = FastAPI()

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/games/")
async def read_games() -> list[Game]:
    with Session(engine) as session:
        games = session.exec(select(Game)).all()
        return games


@app.get("/games/{game_id}")
async def read_game(game_id: int) -> Game:
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        return game or Response(status_code=HTTPStatus.BAD_REQUEST)
