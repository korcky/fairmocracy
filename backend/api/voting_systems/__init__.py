from api.voting_systems.abstract import AbstractVotingSystem, VotingResult
from api.voting_systems.majority import MajorityVotingSystem
from api.voting_systems.reward import MajorityWithRewardSystem


__all__ = [
    "AbstractVotingSystem",
    "VotingResult",
    "MajorityVotingSystem",
    "MajorityWithRewardSystem",
]
