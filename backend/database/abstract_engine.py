from abc import ABCMeta, abstractmethod

from api.voting_systems import VotingResult
from api.models import Affiliation, Voter, VotingEvent, Vote, Party, Game, Round


class NoDataFoundError(Exception):
    pass


class AbstractEngine(metaclass=ABCMeta):
    @abstractmethod
    def startup_initialization(self) -> None:
        """DB initialization that must happen on the API startup"""
        pass

    @abstractmethod
    def get_voter(self, voter_id: int) -> Voter:
        """Return Voter based on its ID"""
        pass

    @abstractmethod
    def get_voters(self, game_id: int) -> list[Voter]:
        pass

    @abstractmethod
    def add_voter(self, voter: Voter) -> Voter:
        pass

    @abstractmethod
    def update_voters(self, voters: list[Voter]):
        pass

    @abstractmethod
    def get_party(self, party_id: int) -> Party:
        """Return Party based on its ID"""
        pass

    @abstractmethod
    def get_parties(self, game_id: int) -> list[Party]:
        pass

    @abstractmethod
    def update_parties(self, parties: list[Party]):
        pass

    @abstractmethod
    def add_affiliation(self, affiliation: Affiliation) -> Affiliation:
        pass

    @abstractmethod
    def get_game(self, game_id: int) -> Game:
        """Return Game based on its ID"""
        pass

    @abstractmethod
    def get_game_by_hash(self, game_hash: str) -> Game:
        pass

    @abstractmethod
    def update_game_status(game: Game) -> None:
        pass

    @abstractmethod
    def start_next_round(game: Game) -> None:
        pass

    @abstractmethod
    def start_next_event(game: Game) -> None:
        pass

    @abstractmethod
    def get_rounds(self, game_id: int) -> list[Round]:
        pass

    @abstractmethod
    def get_voting_event(self, voting_event_id: int) -> VotingEvent:
        """Return VotingEvent based on its ID"""
        pass

    @abstractmethod
    def get_voting_events(self, round_id: int) -> list[VotingEvent]:
        """Return all VotingEvents in the given round"""
        pass


    @abstractmethod
    def update_voting_event(
        self, voting_event_id: int, voting_result: VotingResult, extra_info: dict | None = None
    ) -> None:
        pass

    @abstractmethod
    def cast_vote(self, vote: Vote) -> None:
        """Save Vote into the DB"""
        pass

    @abstractmethod
    def get_votes(self, voting_event_id: int) -> list[Vote]:
        pass

    @abstractmethod
    def get_active_game() -> Game:
        pass

    @abstractmethod
    def get_affiliations_for_round(self, round_id: int):
        pass
    