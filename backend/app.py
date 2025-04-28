import asyncio
import json
import signal
import logging
import io
from http import HTTPStatus
from sqlite3 import IntegrityError as DBIntegrityError
from sqlalchemy.exc import IntegrityError as SAIntegrityError
from pandas.errors import EmptyDataError, ParserError
from typing import Annotated
import functools
from fastapi import APIRouter, Depends, FastAPI, Cookie
from fastapi.responses import Response, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from database.abstract_engine import NoDataFoundError
import dummy_data
from api.voting_systems import AbstractVotingSystem, VotingResult, MajorityVotingSystem
from api.models import (
    Voter,
    Vote,
    VotingEvent,
    Party,
    Game,
    Round,
    Affiliation,
    VotingSystem,
    GameStatus,
)
from api.sse_connection_manager import SSEConnectionManager
from database import AbstractEngine, SQLEngine
from db_config import get_db_engine
from configurations.config_reader import VotingConfigReader

app = FastAPI()


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


user_router = APIRouter()
game_router = APIRouter()
common_router = APIRouter()

# I guess we should store configuration for voting system in DB
# and initialize class for a voting system using this data during
# the calculation of the voting event result
AVAILABLE_VOTING_SYSTEM_CLS = {
    VotingSystem.MAJORITY: MajorityVotingSystem,
}

connection_manager = SSEConnectionManager()

"""
Decorator to broadcast game state changes to all connected clients using SSE
"""


def broadcast_game_state(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        engine = get_db_engine()
        response = await f(*args, **kwargs)
        game_id = (
            kwargs.get("game_id")
            or getattr(response, "game_id", None)
            or engine.get_active_game().id
        )
        game = engine.get_game(game_id=game_id)
        state = game.state
        await connection_manager.broadcast(state)
        return response

    return wrapper


@app.on_event("startup")
def on_startup():
    engine = get_db_engine()
    engine.startup_initialization()

    try:
        engine.get_active_game()
    except NoDataFoundError:
        dummy_data.initialize(number_of_voters=0)


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, connection_manager.close)
    except NotImplementedError:
        pass


@user_router.get(
    "/{user_id}",
    tags=["user"],
)
# @broadcast_game_state
async def get_user(user_id: str, db_engine: AbstractEngine = Depends(get_db_engine)):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@user_router.post(
    "/login",
    tags=["user"],
)
@broadcast_game_state
async def login(
    key: str | None = None, db_engine: AbstractEngine = Depends(get_db_engine)
):
    return Response(status_code=HTTPStatus.NO_CONTENT)


@game_router.get(
    "/current_state/{game_id}",
    tags=["voting"],
)
async def get_current_state(
    game_id: int, db_engine: AbstractEngine = Depends(get_db_engine)
):
    game = db_engine.get_game(game_id=game_id)
    if not game:
        return Response(status_code=HTTPStatus.BAD_REQUEST)
    return game.state


@game_router.post(
    "/cast_vote",
    tags=["voting"],
    status_code=HTTPStatus.OK,
)
@broadcast_game_state
async def cast_vote(vote: Vote, db_engine: AbstractEngine = Depends(get_db_engine)):
    # TODO probably some more checks ...
    voting_event = db_engine.get_voting_event(vote.voting_event_id)
    round = db_engine.get_round(voting_event.round_id)
    game = db_engine.get_game(round.game_id)
    if not game:
        raise ValueError("Game not found for the given voting event ID")
    # check that the voting event is active
    if not game.status == GameStatus.STARTED:
        raise ValueError("Game is not started")
    if not game.current_voting_event_id == vote.voting_event_id:
        raise ValueError("Voting event is not active")
    votes = db_engine.get_votes(vote.voting_event_id)
    # check that the voter hasn't voted in this event yet
    if any(lambda v: v.voter_id == vote.voter_id for v in votes):
        raise ValueError("Voter has already voted in this event")
    # if this will be the last vote,
    # set current_voting_event_id (if there are more voting events left in the round)
    # or set current_round_id and status to waiting (if there are more rounds left)
    # or set status to ended (if there are no more voting events or rounds left)
    if len(votes) == game.n_voters - 1:
        try:
            print("Last voter, starting next event!")
            db_engine.start_next_event(game.id)
        except:
            try:
                print("No next event, starting next round!")
                db_engine.start_next_round(game.id)
            except:
                print("No next round, ending game!")
                db_engine.update_game_status(game.id, GameStatus.ENDED)
    # Vote debug logging
    print(
        f"Vote received: voter_id={vote.voter_id}, "
        f"round_id={voting_event.round_id}, "
        f"event_id={vote.voting_event_id}, "
        f"value={vote.value}"
    )
    db_engine.cast_vote(vote)
    content = {
        "voter_id": vote.voter_id,
        "round_id": voting_event.round_id,
        "voting_event_id": vote.voting_event_id,
        "value": vote.value,
    }
    resp = JSONResponse(status_code=HTTPStatus.OK, content=content)
    resp.game_id = game.id
    return resp


app.include_router(user_router, prefix="/v1/user")
app.include_router(game_router, prefix="/v1/voting")


# TODO refactor stuff below (especially pathes and tags)
@common_router.get(
    "/game/{game_id}/parties",
    response_model=list[Party],
)
async def read_parties_by_game(
    game_id: int, db_engine: AbstractEngine = Depends(get_db_engine)
) -> list[Party]:
    try:
        return db_engine.get_parties(game_id=game_id)
    except NoDataFoundError:
        return []


@common_router.get(
    "/game/{game_id}",
    response_model=Game,
)
async def read_game(
    game_id: int,
    db_engine: AbstractEngine = Depends(get_db_engine),
) -> Game:
    return db_engine.get_game(game_id=game_id)


@common_router.get(
    "/game/{game_id}/rounds",
    response_model=list[Round],
)
async def get_rounds_by_game(
    game_id: int, db_engine: AbstractEngine = Depends(get_db_engine)
) -> list[Round]:
    return db_engine.get_rounds(game_id=game_id)


@common_router.get(
    "/join",
    response_model=Game,
)
async def get_game_by_hash(
    game_hash: str, db_engine: AbstractEngine = Depends(get_db_engine)
) -> Game:
    try:
        return db_engine.get_game_by_hash(game_hash=game_hash)
    except Exception:
        return Response(status_code=HTTPStatus.NOT_FOUND)


@common_router.post(
    "/register",
    response_model=Voter,
)
@broadcast_game_state
async def register_user(
    user: Voter, db_engine: AbstractEngine = Depends(get_db_engine)
) -> JSONResponse:
    voter = db_engine.add_voter(voter=user)
    payload = {
        "id": voter.id,
        "name": voter.name,
        "game_id": voter.game_id,
        "extra_info": voter.extra_info,
    }
    resp = JSONResponse(status_code=HTTPStatus.OK, content=payload)
    resp.game_id = voter.game_id
    return resp


@common_router.post("/register_to_vote", response_model=Affiliation)
@broadcast_game_state
async def register_to_vote(
    affiliation: Affiliation, db_engine: AbstractEngine = Depends(get_db_engine)
) -> Affiliation:
    voter = db_engine.get_voter(affiliation.voter_id)
    game = db_engine.get_game(voter.game_id)
    round = db_engine.get_round(affiliation.round_id)
    if not round:
        raise ValueError("Round not found")
    n_affiliations = len(db_engine.get_affiliations_for_round(affiliation.round_id))
    n_players = len(db_engine.get_voters(voter.game_id))
    # if the number of affiliations for this round is equal to the number of players in the game, set the game state as started
    # and set the current_voting_event_id to the id of the first voting event of the round (we will assume they are ordered by PK)
    if n_affiliations == n_players - 1:
        db_engine.update_game_status(game.id, GameStatus.STARTED)
        if not game.current_round_id:
            db_engine.start_next_round(game.id)
        if not game.current_voting_event_id:
            db_engine.start_next_event(game.id)
    new_aff = db_engine.add_affiliation(affiliation=affiliation)
    payload = {
        "id": new_aff.id,
        "voter_id": new_aff.voter_id,
        "party_id": new_aff.party_id,
        "round_id": new_aff.round_id,
    }
    resp = JSONResponse(status_code=HTTPStatus.OK, content=payload)
    resp.game_id = game.id
    return resp


@common_router.post("/upload_config")
@broadcast_game_state
async def upload_config(
    file: UploadFile = File(...), db_engine: AbstractEngine = Depends(get_db_engine)
):
    try:
        raw_bytes = await file.read()
        try:
            csv_text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("File must be UTF-8 encoded CSV")

        file_like = io.StringIO(csv_text)
        reader = VotingConfigReader(file_like)
        game = reader.get_game()

        resp = JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Game created successfully!",
                "game_code": game.hash,
                "game_id": game.id,
                "game_name": game.name,
            },
        )
        resp.game_id = game.id
        return resp

    ### Database constraint violations ###
    except SAIntegrityError as e:
        # The raw DBAPI error is in e.orig
        msg = str(e.orig).lower()

        if "not null constraint failed: game.n_voters" in msg:
            detail = "Configuration error: 'number_of_voters' is required."
        elif "unique constraint failed: game.hash" in msg:
            detail = "Configuration error: Game code collision—try again."
        elif "foreign key constraint failed" in msg:
            detail = "Configuration error: Your CSV references a non-existent entity."
        else:
            detail = "Invalid configuration (DB constraint): " + msg

        return JSONResponse(status_code=400, content={"error": detail})

    except DBIntegrityError as e:
        # Raw sqlite3 error
        msg = str(e).lower()

        if "not null constraint failed: game.n_voters" in msg:
            detail = "Configuration error: 'number_of_voters' is required."
        elif "unique constraint failed: game.hash" in msg:
            detail = "Configuration error: Game code collision—try again."
        elif "foreign key constraint failed" in msg:
            detail = "Configuration error: Your CSV references a non-existent entity."
        else:
            detail = "Invalid configuration (SQLite): " + msg

        return JSONResponse(status_code=400, content={"error": detail})

    ### CSV parsing errors ###
    except EmptyDataError:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Uploaded CSV is empty or malformed—please provide a valid CSV file."
            },
        )
    except ParserError as e:
        return JSONResponse(status_code=400, content={"error": f"CSV parse error: {e}"})

    ### Missing columns or bad round indices ###
    except KeyError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"Configuration error: missing required column '{e.args[0]}'."
            },
        )
    except IndexError as e:
        return JSONResponse(
            status_code=400, content={"error": f"Configuration error: {e}"}
        )

    ### Any other validation or type errors ###
    except ValueError as e:
        return JSONResponse(
            status_code=400, content={"error": f"Configuration error: {e}"}
        )

    ### Fallback for all other unexpected errors ###
    except Exception as e:
        print("Unexpected error in upload_config")
        return JSONResponse(
            status_code=500, content={"error": "Unexpected error: " + str(e)}
        )

@common_router.post("/upload_config")
@broadcast_game_state
async def upload_config(file: UploadFile = File(...), db_engine: AbstractEngine = Depends(get_db_engine)):
    try:
        contents = await file.read()
        file_like = io.StringIO(contents.decode('utf-8'))
        reader = VotingConfigReader(file_like)
        game = reader.get_game()

        print(f"Game Created: {game.id}, Status: {game.status}, Name: {game.name}")
        
        await connection_manager.broadcast(game.status)

        return JSONResponse(content={
                "message": "Game created successfully!",
                "game_code": game.hash,  
                "game_id": game.id,
                "game_name": game.name
            })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# TODO: get voting event through Dependency?
@common_router.post(
    "/voting_event/{voting_event_id}/conclude",
)
# @broadcast_game_state
async def conclude_voting(
    voting_event_id: int, db_engine: AbstractEngine = Depends(get_db_engine)
):
    voting_event = db_engine.get_voting_event(voting_event_id=voting_event_id)
    voting_system_cls = AVAILABLE_VOTING_SYSTEM_CLS.get(voting_event.voting_system)
    if not voting_system_cls:
        logging.error(
            f"Unknown voting system ({voting_event.voting_system}) for voting event {voting_event_id}"
        )
        return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    voting_system = voting_system_cls(**voting_event.configuration)
    votes = db_engine.get_votes(voting_event_id=voting_event_id)
    result, side_effects = voting_system.voting_result(votes=votes)
    db_engine.update_voting_event(
        voting_event_id=voting_event_id,
        voting_result=result,
        # TODO: work with side effects
        # extra_info=...
    )
    return Response(
        status_code=HTTPStatus.OK, content=json.dumps({"voting_event_result": result})
    )


@common_router.api_route("/sse/game-state", methods=["GET", "POST"])
async def stream_game_state():
    return StreamingResponse(
        connection_manager.connect(), media_type="text/event-stream"
    )


# for testing only; remove when not needed
@common_router.api_route("/broadcast")
@broadcast_game_state
async def broadcast(): ...


app.include_router(common_router)
