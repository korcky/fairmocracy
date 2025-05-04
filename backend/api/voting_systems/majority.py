from api.voting_systems.abstract import AbstractVotingSystem, VotingResult
from api.models import VoteValue, Vote, VotingEvent, Voter, Party


class MajorityVotingSystem(AbstractVotingSystem):
    """
    Simply Votes(yes)/Votes(No) > pass_threshold

    with is_abstain_count_to_total == True:
        Votes(yes)/Votes(No and Abstain) > pass_threshold
    """
    name = "MAJORITY"

    def __init__(
        self,
        pass_threshold: float = 0.5,
        is_abstain_count_to_total: bool = False,
    ):
        self.pass_threshold = pass_threshold
        self.is_abstain_count_to_total = is_abstain_count_to_total

    def voting_result(
        self, voting_event: VotingEvent, votes: list[Vote], voters: list[Voter], parties: list[Party],
    ) -> tuple[VotingResult, list[Voter], list[Party]]:
        votes = [
            vote.value == VoteValue.YES
            for vote in votes
            if self.is_abstain_count_to_total or vote.value != VoteValue.ABSTAIN
        ]
        result = (
            VotingResult.ACCEPTED
            if sum(votes) / len(votes) > self.pass_threshold
            else VotingResult.REJECTED
        )
        return result, [], []
