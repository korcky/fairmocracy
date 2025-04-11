import json
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Cookie
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from api.models import Voter, Vote, VotingEvent, Party, Game
from database import AbstractEngine, SQLEnging
from database.sql import models as sql_models  # TODO remove

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)


user_router = APIRouter()
game_router = APIRouter()
common_router = APIRouter()

DB_ENGINE = SQLEnging(url=f"sqlite:///database.sqlite3")


def get_db_engine() -> AbstractEngine:
    return DB_ENGINE


@app.on_event("startup")
def on_startup():
    get_db_engine().startup_initialization()
    # Uncomment to create test game on startup
    test_game = sql_models.Game(
        name="Test Game", hash="1234", rounds=[
            sql_models.Round(round_number=0, parties=[sql_models.Party(name="red"), sql_models,Party(name="blue")], rules="FI")],
    )
    with Session(DB_ENGINE) as session:
        session.add(test_game)
        session.commit()


@user_router.get(
    "/{user_id}",
    tags=["user"],
)
async def get_user(user_id: str, db_engine: AbstractEngine = Depends(get_db_engine)):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@user_router.post(
    "/login",
    tags=["user"],
)
async def login(key: str | None = None, db_engine: AbstractEngine = Depends(get_db_engine)):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@game_router.get(
    "/current_state",
    tags=["voting"],
)
async def get_current_state(db_engine: AbstractEngine = Depends(get_db_engine)):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@game_router.post(
    "/cast_vote",
    tags=["voting"],
)
async def cast_vote(vote: Vote, db_engine: AbstractEngine = Depends(get_db_engine)):
    db_engine.cast_vote(vote)
    return Response(status_code=HTTPStatus.NO_CONTENT)

app.include_router(user_router, prefix="/v1/user")
app.include_router(game_router, prefix="/v1/voting")


# TODO refactor stuff below
@common_router.get("/games/")
async def read_games() -> list[sql_models.Game]:
    with Session(DB_ENGINE) as session:
        games = session.exec(select(sql_models.Game)).all()
        return games


@common_router.get("/games/{game_id}")
async def read_game(game_id: int) -> sql_models.Game:
    with Session(DB_ENGINE) as session:
        game = session.exec(select(sql_models.Game).where(sql_models.Game.id == game_id)).first()
        return game or Response(status_code=HTTPStatus.BAD_REQUEST)


@common_router.get("/parties/game/{game_id}")
async def read_parties_by_game(game_id: int) -> list[sql_models.Party]:
    with Session(DB_ENGINE) as session:
        game = session.exec(select(sql_models.Game).where(sql_models.Game.id == game_id)).first()
        if not game:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        game_state = json.loads(game.state)
        current_round_number = game_state["current_round"]
        rounds = session.exec(select(sql_models.Round).where(sql_models.Round.game_id == game_id)).all()
        current_round = next((round for round in rounds if round.round_number == current_round_number), None)
        if not current_round:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        return current_round.parties


@common_router.get(
    "/rounds/{game_id}",
    response_model=list[sql_models.Round],
)
async def get_rounds_by_game(game_id: int) -> list[sql_models.Round]:
    with Session(DB_ENGINE) as session:
        rounds = session.exec(select(sql_models.Round).where(sql_models.Round.game_id == game_id)).all()
        return rounds


@common_router.get(
    "/join",
    response_model=sql_models.Game,
)
async def get_game_by_hash(game_hash: str) -> sql_models.Game:
    with Session(DB_ENGINE) as session:
        game = session.exec(select(sql_models.Game).where(sql_models.Game.hash == game_hash)).first()
        if not game:
            return Response(status_code=HTTPStatus.NOT_FOUND)
        return game


@common_router.post(
    "/register",
    response_model=sql_models.Voter,
)
async def register_user(user: sql_models.Voter) -> sql_models.Voter:
    with Session(DB_ENGINE) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        print(user)
        return user


@common_router.post(
    "/register_to_vote",
    response_model=sql_models.Affiliation
)
async def register_to_vote(affiliation: sql_models.Affiliation) -> sql_models.Affiliation:
    with Session(DB_ENGINE) as session:
        round = session.exec(select(sql_models.Game).where(sql_models.Round.id == affiliation.round_id)).first() 
        if not round:
            print("no round")
            return Response(status_code=HTTPStatus.NOT_FOUND)
        party = session.exec(select(sql_models.Party).where(sql_models.Party.id == affiliation.party_id, sql_models.Party.round_id == affiliation.round_id)).first()
        if not party:
            print("no party")
            return Response(status_code=HTTPStatus.NOT_FOUND)
        voter = session.exec(select(sql_models.Voter).where(sql_models.Voter.id == affiliation.voter_id)).first()
        if not voter:
            print("no voter")
            return Response(status_code=HTTPStatus.NOT_FOUND)
        session.add(affiliation)
        session.commit()
        session.refresh(affiliation)
        return affiliation


app.include_router(common_router)
