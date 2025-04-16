from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from api import models as api_models
from database.abstract_engine import AbstractEngine, NoDataFoundError
from database.sql import models as sql_models


class SQLEngine(AbstractEngine):
    def __init__(self, url: str) -> None:
        self.engine = create_engine(
            url,
            # echo=True,
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
            raise NoDataFoundError
    
    def add_voter(self, voter: api_models.Voter) -> api_models.Voter:
        with Session(self.engine) as session:
            sql_voter = sql_models.Voter(
                name=voter.name,
                game_id=voter.game_id,
            )
            session.add(sql_voter)
            session.commit()
            session.refresh(sql_voter)
            voter.id = sql_voter.id
            return voter

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
            raise NoDataFoundError
    
    def get_parties(self, game_id: int) -> list[api_models.Party]:
        with Session(self.engine) as session:
            parties = session.exec(
                select(sql_models.Party).join(sql_models.Round).join(sql_models.Game).where(
                    sql_models.Game.id == game_id,
                    sql_models.Party.round_id == sql_models.Game.current_round_id,
                )
            ).all()
            if parties:
                return [
                    api_models.Party(
                        id=party.id,
                        name=party.name,
                        round_id=party.round_id,
                    )
                    for party in parties
                ]
            raise NoDataFoundError
    
    def add_affiliation(self, affiliation: api_models.Affiliation) -> api_models.Affiliation:
        with Session(self.engine) as session:
            sql_affiliation = sql_models.Affiliation(
                voter_id=affiliation.voter_id,
                party_id=affiliation.party_id,
            )
            session.add(sql_affiliation)
            session.commit()
            session.refresh(sql_affiliation)
            affiliation.id = sql_affiliation.id
            return affiliation

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
                    hash=game.hash,
                    name=game.name,
                    current_round_id=game.current_round_id,
                )
            raise NoDataFoundError
    
    def get_game_by_hash(self, game_hash: str) -> api_models.Game:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(
                    sql_models.Game.hash == game_hash
                )
            ).first()
            if game:
                return api_models.Game(
                    id=game.id,
                    hash=game.hash,
                    name=game.name,
                    current_round_id=game.current_round_id,
                )
            raise NoDataFoundError
    
    def get_rounds(self, game_id: int) -> list[api_models.Round]:
        with Session(self.engine) as session:
            rounds = session.exec(
                select(sql_models.Round).where(
                    sql_models.Round.game_id == game_id
                )
            ).all()
            if rounds:
                return [
                    api_models.Round(
                        id=_round.id,
                        round_number=_round.round_number,
                        game_id=_round.game_id,
                    )
                    for _round in rounds
                ]
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
            raise NoDataFoundError

    def cast_vote(self, vote: api_models.Vote) -> None:
        with Session(self.engine) as session:
            vote = sql_models.Vote(
                value=vote.value,
                voter_id=vote.voter_id,
                voting_event_id=vote.voting_event_id,
            )
            session.add(vote)
            session.commit()
    
    def get_votes(self, voting_event_id: int) -> list[api_models.Vote]:
        with Session(self.engine) as session:
            votes = session.exec(
                select(sql_models.Vote).where(
                    sql_models.Vote.voting_event_id == voting_event_id
                )
            ).all()
            if votes:
                return [
                    api_models.Vote(
                        id=vote.id,
                        value=vote.value,
                        voter_id=vote.voter_id,
                        voting_event_id=vote.voting_event_id,
                        created_at=vote.created_at,
                    )
                    for vote in votes
                ]
            raise NoDataFoundError

    def get_active_game(self):
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(
                    sql_models.Game.status != api_models.GameStatus.ENDED
                )
            ).first()
            if game:
                return api_models.Game(
                    id=game.id,
                    hash=game.hash,
                    name=game.name,
                    current_round_id=game.current_round_id,
                )
            raise NoDataFoundError