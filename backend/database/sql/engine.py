from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from api import models as api_models
from database.abstract_engine import AbstractEngine
from database.sql import models as sql_models


class SQLEnging(AbstractEngine):
    def __init__(self, url: str) -> None:
        self.engine = create_engine(
            url,
            echo=True,
            connect_args={"check_same_thread": False},
        )

    def startup_initialization(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def get_voter(self, voter_id: int) -> api_models.Voter:
        with Session(self.engine) as session:
            voter = session.exec(
                select(sql_models.Voter).where(
                    sql_models.Voter.id == voter_id
                )
            ).first()
            if voter:
                return api_models.Voter(
                    id=voter.id,
                    name=voter.name,
                    game_id=voter.game_id,
                    party_id=voter.party_id,
                )
            raise Exception

    def get_party(self, party_id: int) -> api_models.Party:
        with Session(self.engine) as session:
            party = session.exec(
                select(sql_models.Party).where(
                    sql_models.Party.id == party_id
                )
            ).first()
            if party:
                return api_models.Party(
                    id=party.id,
                    name=party.name,
                )
            raise Exception

    def get_game(self, game_id: int) -> api_models.Game:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(
                    sql_models.Game.id == game_id
                )
            ).first()
            if game:
                return api_models.Game(
                    id=game.id,
                    name=game.name,
                    voting_event_ids=[event.id for event in game.voting_events],
                    _voting_events=game.voting_events,
                )
            raise Exception

    def get_voting_event(self, voting_event_id: int) -> api_models.VotingEvent:
        with Session(self.engine) as session:
            event = session.exec(
                select(sql_models.VotingEvent).where(
                    sql_models.VotingEvent.id == voting_event_id
                )
            ).first()
            if event:
                return api_models.VotingEvent(
                    id=event.id,
                    title=event.title,
                    content=event.content,
                    voting_system=event.voting_system,
                    result=event.result,
                )
            raise Exception

    def cast_vote(self, vote: api_models.Vote) -> None:
        with Session(self.engine) as session:
            vote = sql_models.Vote(
                value=vote.value,
                voter_id=vote.voter_id,
                voting_event_id=vote.voting_event_id,
            )
            session.add(vote)
            session.commit()
