from abc import ABCMeta, abstractmethod
from enum import StrEnum

from api.models import Vote, VotingEvent, Voter, Party


class VotingResult(StrEnum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class AbstractVotingSystem(metaclass=ABCMeta):
    @abstractmethod
    def voting_result(
        self, voting_event: VotingEvent, votes: list[Vote], voters: list[Voter], parties: list[Party],
    ) -> tuple[VotingResult, list[Voter], list[Party]]:
        """
        Returns voteing event result and side effects (a dict (?) with other changes, e.g. points lost/gained, etc.)

        To be defined more precise later
        """
        pass
