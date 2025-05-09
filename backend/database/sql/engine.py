from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from api import models as api_models
from api.voting_systems import VotingResult
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
                select(sql_models.Voter).where(sql_models.Voter.id == voter_id)
            ).first()
            if voter:
                return api_models.Voter(
                    id=voter.id,
                    name=voter.name,
                    game_id=voter.game_id,
                    extra_info=voter.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                )
            raise NoDataFoundError

    def get_voters(self, game_id: int) -> list[api_models.Voter]:
        with Session(self.engine) as session:
            voters = session.exec(
                select(sql_models.Voter).where(sql_models.Voter.game_id == game_id)
            ).all()
            if voters:
                return [
                    api_models.Voter(
                        id=voter.id,
                        name=voter.name,
                        game_id=voter.game_id,
                        extra_info=voter.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                    )
                    for voter in voters
                ]
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
        
    def update_voters(self, voters: list[api_models.Voter]):
        voters_extra_info = {v.id: v.extra_info for v in voters}
        with Session(self.engine) as session:
            # this should be filtered 
            sql_voters = session.exec(select(sql_models.Voter)).all()
            for voter in sql_voters:
                if voter.id in voters_extra_info:
                    voter.extra_info = voters_extra_info[voter.id]
                    session.add(voter)
            session.commit()

    def get_party(self, party_id: int) -> api_models.Party:
        with Session(self.engine) as session:
            party = session.exec(
                select(sql_models.Party).where(sql_models.Party.id == party_id)
            ).first()
            if party:
                return api_models.Party(
                    id=party.id,
                    name=party.name,
                    extra_info=party.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                    round_id=party.round_id,
                )
            raise NoDataFoundError

    def get_parties(self, game_id: int) -> list[api_models.Party]:
        with Session(self.engine) as session:
            parties = session.exec(
                select(sql_models.Party)
                .join(sql_models.Round)
                .join(sql_models.Game)
                .where(
                    sql_models.Game.id == game_id,
                    sql_models.Party.round_id == sql_models.Game.current_round_id,
                )
            ).all()
            if parties:
                return [
                    api_models.Party(
                        id=party.id,
                        name=party.name,
                        extra_info=party.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                        round_id=party.round_id,
                    )
                    for party in parties
                ]
            raise NoDataFoundError
    
    def update_parties(self, parties: list[api_models.Party]):
        parties_extra_info = {p.id: p.extra_info for p in parties}
        with Session(self.engine) as session:
            # this should be filtered 
            sql_parties = session.exec(select(sql_models.Party)).all()
            for party in sql_parties:
                if party.id in parties_extra_info:
                    party.extra_info = parties_extra_info[party.id]
                    session.add(party)
            session.commit()

    def add_affiliation(
        self, affiliation: api_models.Affiliation
    ) -> api_models.Affiliation:
        with Session(self.engine) as session:
            sql_affiliation = sql_models.Affiliation(
                voter_id=affiliation.voter_id,
                party_id=affiliation.party_id,
                round_id=affiliation.round_id,
            )
            session.add(sql_affiliation)
            session.commit()
            session.refresh(sql_affiliation)
            affiliation.id = sql_affiliation.id
            return affiliation

    def get_game(self, game_id: int) -> api_models.Game:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(sql_models.Game.id == game_id)
            ).first()
            if game:
                return api_models.Game(
                    id=game.id,
                    hash=game.hash,
                    name=game.name,
                    current_round_id=game.current_round_id,
                    current_voting_event_id=game.current_voting_event_id,
                    status=game.status,
                    n_voters=game.n_voters,
                )
            raise NoDataFoundError

    def get_game_by_hash(self, game_hash: str) -> api_models.Game:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(sql_models.Game.hash == game_hash)
            ).first()
            if not game:
                print("raising error")
                raise NoDataFoundError

            return api_models.Game(
                id=game.id,
                hash=game.hash,
                name=game.name,
                current_round_id=game.current_round_id,
                current_voting_event_id=game.current_voting_event_id,
                status=game.status,
                n_voters=game.n_voters,
            )

    def update_game_status(self, game_id: int, status: api_models.GameStatus) -> None:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(sql_models.Game.id == game_id)
            ).first()
            if not game:
                raise NoDataFoundError
            game.status = status
            session.add(game)
            session.commit()

    def start_next_round(self, game_id: int) -> None:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(sql_models.Game.id == game_id)
            ).first()
            if not game:
                raise NoDataFoundError

            rounds = self.get_rounds(game.id)
            rounds.sort(key=lambda r: r.id)

            # we haven't set current_round_id yet -> initialize to first round
            if game.current_round_id is None:
                first = rounds[0]
                game.current_round_id = first.id
                session.add(game)
                session.commit()
                return

            # already in a round -> move to the next one if there is one**
            current_index = next(
                (i for i, r in enumerate(rounds) if r.id == game.current_round_id), None
            )
            if current_index is None:
                raise Exception(f"Current round ID {game.current_round_id} not found")
            if current_index < len(rounds) - 1:
                # advance to the following round
                game.current_round_id = rounds[current_index + 1].id
                game.current_voting_event_id = None
                game.status = api_models.GameStatus.WAITING
                session.add(game)
                session.commit()
            else:
                raise Exception("No more rounds left")

    def start_next_event(self, game_id: int) -> None:
        with Session(self.engine) as session:
            game = session.exec(
                select(sql_models.Game).where(sql_models.Game.id == game_id)
            ).first()
            if not game:
                raise NoDataFoundError
            # check if there are more voting events left
            voting_events = session.exec(
                select(sql_models.VotingEvent).where(
                    sql_models.VotingEvent.round_id == game.current_round_id
                )
            ).all()
            voting_events.sort(key=lambda event: event.id)
            if not game.current_voting_event_id:
                game.current_voting_event_id = voting_events[0].id
                session.add(game)
                session.commit()
                return
            current_voting_event_index = next(
                i
                for i, v in enumerate(voting_events)
                if v.id == game.current_voting_event_id
            )
            if current_voting_event_index < len(voting_events) - 1:
                game.current_voting_event_id = voting_events[
                    current_voting_event_index + 1
                ].id
                session.add(game)
                session.commit()
            else:
                raise Exception("No more voting events left")

    def get_rounds(self, game_id: int) -> list[api_models.Round]:
        with Session(self.engine) as session:
            rounds = session.exec(
                select(sql_models.Round).where(sql_models.Round.game_id == game_id)
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

    def get_round(self, round_id: int) -> list[api_models.Round]:
        with Session(self.engine) as session:
            round = session.exec(
                select(sql_models.Round).where(sql_models.Round.id == round_id)
            ).first()
            if round:
                return api_models.Round(
                    id=round.id,
                    round_number=round.round_number,
                    game_id=round.game_id,
                )
            raise NoDataFoundError

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
                    configuration=event.configuration,
                    extra_info=event.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                    round_id=event.round_id,
                )
            raise NoDataFoundError
        
    def get_voting_events(self, round_id: int) -> list[api_models.VotingEvent]:
        with Session(self.engine) as session:
            events = session.exec(
                select(sql_models.VotingEvent).where(sql_models.VotingEvent.round_id == round_id)
            ).all()
            if events:
                return [
                    api_models.VotingEvent(
                        id=event.id,
                        title=event.title,
                        content=event.content,
                        voting_system=event.voting_system,
                        result=event.result,
                        configuration=event.configuration,
                        extra_info=event.extra_info,
                        round_id=event.round_id,
                    )
                    for event in events
                ]

            raise NoDataFoundError
    
    def update_voting_event(
        self,
        voting_event_id: int,
        voting_result: VotingResult,
        extra_info: dict | None = None,
    ) -> None:
        with Session(self.engine) as session:
            event = session.exec(
                select(sql_models.VotingEvent).where(
                    sql_models.VotingEvent.id == voting_event_id
                )
            ).first()
            event.result = voting_result
            if extra_info:
                event.extra_info = extra_info 
            session.add(event)
            session.commit()

    def cast_vote(self, vote: api_models.Vote, extra_info: dict | None = None) -> None:
        with Session(self.engine) as session:
            sql_vote = sql_models.Vote(
                value=vote.value,
                voter_id=vote.voter_id,
                voting_event_id=vote.voting_event_id,
                extra_info=extra_info,
            )
            session.add(sql_vote)
            session.commit()

    def get_votes(self, voting_event_id: int) -> list[api_models.Vote]:
        with Session(self.engine) as session:
            votes = session.exec(
                select(sql_models.Vote).where(
                    sql_models.Vote.voting_event_id == voting_event_id
                )
            ).all()
            return [
                api_models.Vote(
                    id=vote.id,
                    value=vote.value,
                    voter_id=vote.voter_id,
                    voting_event_id=vote.voting_event_id,
                    created_at=vote.created_at,
                    extra_info=vote.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                )
                for vote in votes
            ]

    def get_vote(self, voting_event_id, voter_id):
        with Session(self.engine) as session:
            vote = session.exec(
                select(sql_models.Vote).where(
                    sql_models.Vote.voting_event_id == voting_event_id,
                    sql_models.Vote.voter_id == voter_id,
                )
            ).first()
            if vote:
                return api_models.Vote(
                    id=vote.id,
                    value=vote.value,
                    voter_id=vote.voter_id,
                    voting_event_id=vote.voting_event_id,
                    created_at=vote.created_at,
                    extra_info=vote.extra_info or {}, # probably a bad fix to an error occurring with custom games, fix this in another way in the future
                )
            raise NoDataFoundError

    def get_active_game(self) -> api_models.Game:
        with Session(self.engine) as session:
            # 1) look for non-ended games, newest first
            #    (this is a fix for running custom game which seems to currently get ID 2)
            stmt = (
                select(sql_models.Game)
                .where(sql_models.Game.status != api_models.GameStatus.ENDED)
                .order_by(sql_models.Game.id.desc())
            )
            game_row = session.exec(stmt).first()

            # 2) if none found, fall back to absolutely newest game
            if not game_row:
                game_row = session.exec(
                    select(sql_models.Game).order_by(sql_models.Game.id.desc())
                ).first()

            if not game_row:
                raise NoDataFoundError()

            return api_models.Game(
                id=game_row.id,
                hash=game_row.hash,
                name=game_row.name,
                current_round_id=game_row.current_round_id,
                current_voting_event_id=game_row.current_voting_event_id,
                status=game_row.status,
                n_voters=game_row.n_voters,
            )

    def get_affiliations_for_round(self, round_id: int) -> list[api_models.Affiliation]:
        with Session(self.engine) as session:
            affiliations = session.exec(
                select(sql_models.Affiliation).where(
                    sql_models.Affiliation.round_id == round_id
                )
            )
            return [
                api_models.Affiliation(
                    id=affiliation.id,
                    voter_id=affiliation.voter_id,
                    party_id=affiliation.party_id,
                    round_id=affiliation.round_id,
                )
                for affiliation in affiliations
            ]
