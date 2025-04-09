from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Relationship


class Vote(SQLModel, table=True):
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
    id: int | None = Field(default=None, primary_key=True)
    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="votes")
    voting_event_id: int = Field(foreign_key="voting_event.id")
    voting_event: "VotingEvent" = Relationship(back_populates="votes")
    vote_value: bool = Field()
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
