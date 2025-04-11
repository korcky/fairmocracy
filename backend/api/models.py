from datetime import datetime, UTC

from pydantic import BaseModel, ConfigDict, Field

# add __pydantic_extra__: dict[str, int] = Field(init=False) to validate extra fields


class Game(BaseModel):
    """
    A game models a voting game.
    Attributes:
    - id: A unique identifier for the game.
    - hash: A unique hash for the game. (not really a hash)
    - name: The name of the game.
    - voters: The voters (players) in the game.
    - rounds: The rounds of the game.
    - state: The state of the game: a JSON object stored as a string (perhaps a better solution exists). 
    """
    id: int
    hash: str
    name: str
    state: str

    model_config = ConfigDict(extra='allow')

    @property
    def voters(self) -> list[Voter]:
        pass

    @property
    def rounds(self) -> list[Round]:
        pass


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

    id: int
    name: str

    game_id: int

    model_config = ConfigDict(extra='allow')

    @property
    def game(self) -> Game:
        pass

    @property
    def affiliations(self) -> list[Affiliation]:
        pass

 
class Round(BaseModel):
    id: int
    round_number: int

    game_id: int

    @property
    def game(self) -> Game:
        pass

    @property
    def voting_events(self) -> list[VotingEvent]:
        pass

    @property
    def parties(self) -> list[Party]:
        pass


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
    id: int
    name: str

    round_id: int
    
    model_config = ConfigDict(extra='allow')

    @property
    def round(self) -> Round:
        pass

    @property
    def affiliations(self) -> list[Affiliation]:
        pass


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
    id: int

    voter_id: int
    party_id: int

    @property
    def voter(self) -> Voter:
        pass

    @property
    def party(self) -> Party:
        pass


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

    id: int
    title: str
    content: str
    voting_system: str
    result: str | None = Field(default=None)

    round_id: int
    
    model_config = ConfigDict(extra='allow')

    @property
    def round(self) -> Round:
        pass

    @property
    def votes(self) -> list[Vote]:
        pass


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
    value: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    voter_id: int
    voting_event_id: int
    
    model_config = ConfigDict(extra='allow')

    @property
    def voter(self) -> Voter:
        pass

    @property
    def voting_event(self) -> VotingEvent:
        pass
