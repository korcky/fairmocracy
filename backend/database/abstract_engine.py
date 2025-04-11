from abc import ABCMeta, abstractmethod

from api_models import Voter, VotingEvent, Vote, Party, Game


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
    def get_party(self, party_id: int) -> Party:
        """Return Party based on its ID"""
        pass

    @abstractmethod
    def get_game(self, game_id: int) -> Game:
        """Return Game based on its ID"""
        pass

    @abstractmethod
    def get_voting_event(self, voting_event_id: int) -> VotingEvent:
        """Return VotingEvent based on its ID"""
        pass

    @abstractmethod
    def cast_vote(self, vote: Vote) -> None:
        """Save Vote into the DB"""
        pass
