from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, FastAPI, Cookie
from fastapi.responses import Response, JSONResponse
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from models import Game, VotingEvent, Party, Voter, Vote

app = FastAPI()
user_router = APIRouter()
game_router = APIRouter()
common_router = APIRouter()

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

FRONTEND_URL = "http://localhost:3000"

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@common_router.get("/games/")
async def read_games() -> list[Game]:
    with Session(engine) as session:
        games = session.exec(select(Game)).all()
        return games


@common_router.get("/games/{game_id}")
async def read_game(game_id: int) -> Game:
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        return game or Response(status_code=HTTPStatus.BAD_REQUEST)


@common_router.get("/parties/game/{game_id}")
async def read_parties_by_game(game_id: int) -> list[Party]:
    with Session(engine) as session:
        parties = session.exec(select(Party).where(Party.game_id == game_id)).all()
        return parties

@user_router.get(
    "/{user_id}",
    tags=["user"],
)
async def get_user(user_id: str):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@user_router.post(
    "/login",
    tags=["user"],
)
async def login(key: str | None = None):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@game_router.get(
    "/current_state/{game_id}",
    tags=["voting"],
)
async def get_current_state(game_id: int):
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        if not game:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        
        return {"game_id": game.id, "state": game.state, "current_voting_event":game.current_voting_event, "current_voting_event": game.current_voting_event}
        #return game.state
    
    


@game_router.post(
    "/cast_vote",
    tags=["voting"],
)
async def post_vote(user_id: str, vote_id: str, vote: str, extra: dict[str, str] | None = None):
    with Session(engine) as session:
        voter = session.exec(select(Voter).where(Voter.id == user_id)).first()
        voting_event = session.exec(select(VotingEvent).where(VotingEvent.id == vote_id)).first()

        if not voter or not voting_event:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        
        vote = Vote(voter_id=voter.id, voting_event_id=voting_event.id, vote=vote,)
        session.add(vote)
        session.commit()
        return {"message":"Vote cast successfully"}
@common_router.get(
    "/join",
    response_model = Game
)
async def get_game_by_hash(game_hash: str) -> Game:
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.hash == game_hash)).first()
        print(game.parties)
        if not game:
            return Response(status_code=HTTPStatus.NOT_FOUND)
        return game

@common_router.post(
    "/register",
    response_model = Game
)
async def register(voter: Voter) -> Game:
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == voter.game_id)).first()
        if not game:
            print("no game")
            return Response(status_code=HTTPStatus.NOT_FOUND)
        print(voter.party_id)
        print(voter.game_id)
        party = session.exec(select(Party).where(Party.id == voter.party_id, Party.game_id == voter.game_id)).first()
        if not party:
            print("no party")
            return Response(status_code=HTTPStatus.NOT_FOUND)
        voter = Voter(name=voter.name, party_id=party.id, game_id=game.id)
        session.add(voter)
        session.commit()
        return game

@common_router.post(
    "/start_game",
    tags=["game"],
)

async def start_game(game_id:int):
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        if not game:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        game.state = "active"
        session.add(game)
        session.commit()
        return {"message":"Game started"}
    
@common_router.post(
    "/end_game",
    tags=["game"],
)
async def end_game(game_id:int):
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        if not game:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        
        game.state = "ended"
        session.add(game)
        session.commit()
        return {"message":"Game ended"}

@common_router.post(
    "/next_issue/{game_id}",
    tags=["voting"],
)

async def next_issue(game_id: int):
    with Session(engine) as session:
        game = session.exec(select(Game).where(Game.id == game_id)).first()
        if not game:
            return Response(status_code=HTTPStatus.BAD_REQUEST)
        game.current_voting_event += 1
        session.add(game)
        session.commit()
        return {"message":"Moved to next issue"}
# Uncomment to create test game on startup
#test_game = Game(name="Test Game", state="test", hash="1234", rounds=[], parties=[Party(name="red"), Party(name="blue")], voters=[])
#with Session(engine) as session:
#    session.add(test_game)
#    session.commit()


app.include_router(common_router)
app.include_router(user_router, prefix="/v1/user")
app.include_router(game_router, prefix="/v1/voting")
