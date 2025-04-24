from datetime import datetime, UTC
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship


class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="votes")
    voting_event_id: int = Field(foreign_key="voting_event.id")
    voting_event: "VotingEvent" = Relationship(back_populates="votes")
    vote_value: VoteValue = Field()
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


