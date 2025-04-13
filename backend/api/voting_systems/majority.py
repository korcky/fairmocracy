from api.voting_systems.abstract import AbstractVotingSystem, VotingResult
from api.models import VoteValue, Vote


class MajorityVotingSystem(AbstractVotingSystem):
    """Simply Vote(yes)/Vote(No) > pass_threshold"""
    def __init__(self, pass_threshold: float = 0.5):
        self.pass_threshold = pass_threshold

    def voting_result(self, votes: list[Vote]) -> tuple[VotingResult, dict]:
        votes = [
            vote.value == VoteValue.YES
            for vote in votes
            if vote.value != VoteValue.ABSTAIN
        ]
        result = (
            VotingResult.ACCEPTED
            if sum(votes) / len(votes) > self.pass_threshold
            else VotingResult.REJECTED
        )
        return result, {}
