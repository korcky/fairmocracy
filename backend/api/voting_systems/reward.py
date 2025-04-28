import logging

from api.voting_systems.abstract import VotingResult
from api.voting_systems.majority import MajorityVotingSystem
from api.models import Vote, VotingEvent, Voter, Party



class MajorityWithRewardSystem(MajorityVotingSystem):
    """
    Result of the vote is based on MajorityVotingSystem

    Each voting event have a reward per party and/or per voter, thats
    based on the outcome of the event. This reward collects thorughout
    the game and represent the final "score" for a game.

    Structure for extra_info in VotingEvent:
    {
        "MAJORITY_WITH_REWARD": {
            VotingResult.ACCEPTED: {
                "voters": {voter_id_0: voter_reward_0, ...},
                "parties": {party_id_0: party_reward_0, ...}
            }
            VotingResult.REJECTED: {...},
            ...
        }
    }
    """
    name = "MAJORITY_WITH_REWARD"
    _voters_key = "voters"
    _parties_key = "parties"

    def __init__(
        self,
        reward_per_voter: bool = True,
        reward_per_party: bool = True,
        pass_threshold: float = 0.5,
        is_abstain_count_to_total: bool = False,
    ):
        self.reward_per_voter = reward_per_voter
        self.reward_per_party = reward_per_party
        super().__init__(
            pass_threshold=pass_threshold,
            is_abstain_count_to_total=is_abstain_count_to_total,
        )
    
    def _log_warning(self, voting_event_id: int, error: str):
        logging.warning(f"[VotingEvent ({voting_event_id})] Score might not be calculated: {msg}")

    def voting_result(
        self, voting_event: VotingEvent, votes: list[Vote], voters: list[Voter], parties: list[Party],
    ) -> tuple[VotingResult, list[Voter], list[Party]]:
        voting_result, _  = super().voting_result(votes)
        
        if not (self.reward_per_voter or self.reward_per_party):
            self._log_warning(voting_event.id, "both rewards flags are set to `False`")
            return voting_result, [], []
        elif self.name not in voting_event.extra_info:
            self._log_warning(voting_event.id, f"missing {self.name} key in extra_info")
            return voting_result, [], []
        elif voting_result not in voting_event.extra_info[self.name]:
            self._log_warning(voting_event.id, f"missing rewards for {voting_result}")
            return voting_result, [], []

        rewards = voting_event.extra_info[self.name][voting_result]

        if self.reward_per_voter and self._voters_key in rewards:
            for voter in voters:
                if self.name not in voter.extra_info:
                    voter.extra_info[self.name] = {"current_score": 0}
                voter.extra_info[self.name]["current_score"] += rewards[_voters_key].get(voter.id, 0)
        elif self.reward_per_voter:
            self._log_warning(voting_event.id, f"missing voters rewards for {voting_result}")
        
        changes_to_parties = {}
        if self.reward_per_party and self._parties_key in rewards:
            for party in parties:
                if self.name not in party.extra_info:
                    party.extra_info[self.name] = {"current_score": 0}
                party.extra_info[self.name]["current_score"] += rewards[_parties_key].get(party.id, 0)
        elif self.reward_per_party:
            self._log_warning(voting_event.id, f"missing parties rewards for {voting_result}")

        return voting_result, voters, parties
