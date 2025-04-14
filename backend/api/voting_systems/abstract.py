from abc import ABCMeta, abstractmethod
from enum import StrEnum

from api.models import Vote


class VotingResult(StrEnum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class AbstractVotingSystem(metaclass=ABCMeta):
    @abstractmethod
    def voting_result(self, votes: list[Vote]) -> tuple[VotingResult, dict]:
        """
        Returns voteing event result and side effects (a dict (?) with other changes, e.g. points lost/gained, etc.)

        To be defined more precise later
        """
        pass
