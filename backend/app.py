import json
import logging
from http import HTTPStatus
from typing import Annotated
from round import Round

from fastapi import APIRouter, Depends, FastAPI, Cookie
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from api.voting_systems import AbstractVotingSystem, VotingResult, MajorityVotingSystem
from api.models import Voter, Vote, VotingEvent, Party, Game, Round, Affiliation, VotingSystem
from database import AbstractEngine, SQLEngine
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

DB_ENGINE = SQLEngine(url=f"sqlite:///database.sqlite3")
# I guess we should store configuration for voting system in DB
# and initialize class for a voting system using this data during 
# the calculation of the voting event result
AVAILABLE_VOTING_SYSTEMS = {
    VotingSystem.MAJORITY: MajorityVotingSystem(),
}


def get_db_engine() -> AbstractEngine:
    return DB_ENGINE


@app.on_event("startup")
def on_startup():
    get_db_engine().startup_initialization()
    # Uncomment to create test game on startup
    try:
        game = get_db_engine().get_game(game_id=1)
    except Exception as e:
        test_game = sql_models.Game(
            name="Test Game", hash="1234", rounds=[
                sql_models.Round(round_number=0, parties=[sql_models.Party(name="red"), sql_models.Party(name="blue")], rules="FI")],
        )
        with Session(DB_ENGINE.engine) as session:
            session.add(test_game)
            session.commit()
            session.refresh(test_game)
            test_game.current_round_id = test_game.rounds[0].id
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
    "/current_state/{game_id}",
    tags=["voting"],
)
async def get_current_state(game_id: int, db_engine: AbstractEngine = Depends(get_db_engine)):
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        if not game:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        
        return {"current_round": game.current_round, "current_voting_event": game.current_voting_event, "status": game.status}
    
@game_router.post(
    "/cast_vote",
    tags=["voting"],
)
async def cast_vote(vote: Vote, db_engine: AbstractEngine = Depends(get_db_engine)):
    db_engine.cast_vote(vote)
    return Response(status_code=HTTPStatus.NO_CONTENT)

app.include_router(user_router, prefix="/v1/user")
app.include_router(game_router, prefix="/v1/voting")


# TODO refactor stuff below (especially pathes and tags)
@common_router.get(
    "/game/{game_id}/parties",
    response_model=list[Party],
)
async def read_parties_by_game(game_id: int, db_engine: AbstractEngine = Depends(get_db_engine)) -> list[Party]:
    return db_engine.get_parties(game_id=game_id)


@common_router.get(
    "/game/{game_id}/rounds",
    response_model=list[Round],
)
async def get_rounds_by_game(game_id: int, db_engine: AbstractEngine = Depends(get_db_engine)) -> list[Round]:
    return db_engine.get_rounds(game_id=game_id)


@common_router.get(
    "/join",
    response_model=Game,
)
async def get_game_by_hash(game_hash: str, db_engine: AbstractEngine = Depends(get_db_engine)) -> Game:
    try:
        return db_engine.get_game_by_hash(game_hash=game_hash)
    except Exception:
        return Response(status_code=HTTPStatus.NOT_FOUND)


@common_router.post(
    "/register",
    response_model=Voter,
)
async def register_user(user: Voter, db_engine: AbstractEngine = Depends(get_db_engine)) -> Voter:
    return db_engine.add_voter(voter=user)


@common_router.post(
    "/register_to_vote",
    response_model=Affiliation
)
async def register_to_vote(affiliation: Affiliation, db_engine: AbstractEngine = Depends(get_db_engine)) -> Affiliation:
    # TODO: accept juat party_id and add check for round
    return db_engine.add_affiliation(affiliation=affiliation)


# TODO: get voting event through Dependency?
@common_router.post(
    "/voting_event/{voting_event_id}/conclude",
)
async def conclude_voting(voting_event_id: int, db_engine: AbstractEngine = Depends(get_db_engine)):
    voting_event = db_engine.get_voting_event(voting_event_id=voting_event_id)
    voting_system = AVAILABLE_VOTING_SYSTEMS.get(voting_event.voting_system)
    if not voting_system:
        logging.error(
            f"Unknown voting system ({voting_event.voting_system}) for voting event {voting_event_id}"
        )
        return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    votes = db_engine.get_votes(voting_event_id=voting_event_id)
    result, side_effects = voting_system.voting_result(votes=votes)
    # TODO:
    # 1. save result to DB
    # 2. work with side effects
    return Response(status_code=HTTPStatus.OK, content={"voting_event_result": result})


app.include_router(common_router)
