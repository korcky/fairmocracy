from http import HTTPStatus

from fastapi import APIRouter, FastAPI
from fastapi.responses import Response
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from models import Game, VotingEvent

app = FastAPI()
user_router = APIRouter()
game_router = APIRouter()
common_router = APIRouter()

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


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
    "/current_state",
    tags=["voting"],
)
async def get_current_state():
    return Response(status_code=HTTPStatus.NO_CONTENT)


@game_router.post(
    "/cast_vote",
    tags=["voting"],
)
async def post_vote(user_id: str, vote_id: str, vote: str, extra: dict[str, str] | None = None):
    return Response(status_code=HTTPStatus.NO_CONTENT)


app.include_router(common_router)
app.include_router(user_router, prefix="/v1/user")
app.include_router(game_router, prefix="/v1/voting")
