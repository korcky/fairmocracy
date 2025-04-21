from sqlmodel import Session

from api.models import GameStatus
from database.sql import models as sql_models
from db_config import get_db_engine, DB_ENGINE


def initialize():
    try:
        game = get_db_engine().get_game(game_id=1)
        return
    except Exception:
        pass
    test_game = sql_models.Game(
        name="Test Game", hash="1234", rounds=[
            sql_models.Round(round_number=0, parties=[sql_models.Party(name="red"), sql_models.Party(name="blue")], rules="FI")],
            status=GameStatus.STARTED,
    )
    with Session(DB_ENGINE.engine) as session:
        session.add(test_game)
        session.commit()
        session.refresh(test_game)
        test_game.current_round_id = test_game.rounds[0].id
        session.add(test_game)
        session.commit()
