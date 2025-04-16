import random 
import string
from datetime import datetime, UTC
from enum import StrEnum


from pydantic import BaseModel, ConfigDict, Field

# add __pydantic_extra__: dict[str, int] = Field(init=False) to validate extra fields


class VotingSystem(StrEnum):
    MAJORITY = "MAJORITY"


class VoteValue(StrEnum):
    YES = "YES"
    NO = "NO"
    ABSTAIN = "ABSTAIN"


from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

class GameStatus(StrEnum):
    WAITING = "waiting"
    STARTED = "started"
    PAUSED = "paused"
    ENDED = "ended"

class Game(BaseModel):
    """
    A game models a voting game.
    Attributes:
    - id: A unique identifier for the game.
    - hash: A unique hash for the game. (not really a hash)
    - name: The name of the game.
    - current_round_id: id for a current Round.
    - current_voting_event_id: id for a current VotingEvent.
    - status: The status of the game (waiting, started, paused, ended).
    """

    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(default = ''.join(random.choices(string.ascii_lowercase, k=4)))
    name: str = Field()
    current_round_id: int = Field(default=0)
    current_voting_event_id: int | None = Field(default=None, foreign_key="voting_event.id")
    status : GameStatus = Field(default=GameStatus.WAITING)

    def get_state(self):
        return {
            "status": self.status,
            "current_round": self.current_round_id,
            "current_voting_event": self.current_voting_event_id
        }

    model_config = ConfigDict(extra='allow')



class Voter(BaseModel):
    """
    A voter (player) in a game.
    Attributes:
    - id: A unique identifier for the voter.
    - name: The name of the voter.
    - game_id: The ID of the game the voter is participating in.
    - game: The game the voter is participating in.
    - votes: The votes cast by the voter.
    - affiliations: The affiliations of the voter with parties in the game.
    """

    id: int | None = None
    name: str
    game_id: int

    model_config = ConfigDict(extra='allow')

 
class Round(BaseModel):
    id: int | None = None
    round_number: int

    game_id: int


class Party(BaseModel):
    """
    A party represents a political party in the game.
    Different rounds might have different party setups, so it is round-specific.
    Attributes:
    - id: A unique identifier for the party.
    - name: The name of the party.
    - round_id: The ID of the round the party belongs to.
    - round: The round the party belongs to.    
    - affiliations: The affiliations of the party with voters in the game.
    """
    id: int | None = None
    name: str

    round_id: int
    
    model_config = ConfigDict(extra='allow')


class Affiliation(BaseModel):
    """
    An affiliation models the relationship between a voter and a party in a specific round.
    Attributes:
    - id: A unique identifier for the affiliation.
    - voter_id: The ID of the voter.
    - party_id: The ID of the party.
    - round_id: The ID of the round.
    -
    """
    id: int | None = None

    voter_id: int
    party_id: int


class VotingEvent(BaseModel):
    """
    This class is used to store the information of a voting event (a single issue).
    Attributes:
    - id: A unique identifier for the voting event.
    - subject: The subject of the voting event.
    - round_id: The ID of the round the voting event is part of.
    - round: The round the voting event is part of.
    - votes: The votes cast in the voting event. 
    """

    id: int | None = None
    title: str
    content: str
    voting_system: VotingSystem
    result: str | None = Field(default=None)

    round_id: int
    
    model_config = ConfigDict(extra='allow')


class Vote(BaseModel):
    """
    A single vote in a voting event.
    Attributes:
    - id: A unique identifier for the vote.
    - voter_id: The ID of the voter who cast the vote.
    - voting_event_id: The ID of the voting event the vote is for.
    - vote_value: The value of the vote (e.g., true/false). (subject to change? absent, etc.)
    - timestamp: The time the vote was cast.
    - TODO: add parameters object to hold additional information about the vote for influence voting
    """
    id: int | None = Field(default=None)
    value: VoteValue
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    voter_id: int
    voting_event_id: int
    
    model_config = ConfigDict(extra='allow')
