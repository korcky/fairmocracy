import random
import string

from datetime import datetime, UTC

from sqlmodel import SQLModel, Field, Relationship

class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(default = ''.join(random.choices(string.ascii_lowercase, k=4)))
    name: str = Field()
    current_round_id: int | None = Field(default=None)
    current_voting_event_id: int | None = Field(default=None)
    rounds: list["Round"] = Relationship(back_populates="game")
    voters: list["Voter"] = Relationship(back_populates="game")
    status: str = Field()


class Voter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()

    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="voters")
    votes: list["Vote"] = Relationship(back_populates="voter")
    affiliations: list["Affiliation"] = Relationship(back_populates="voter")


class Round(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    round_number: int = Field(default=0)

    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="rounds")
    voting_events: list["VotingEvent"] = Relationship(back_populates="round")
    parties: list["Party"] = Relationship(back_populates="round")


class Party(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()

    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="parties")

    affiliations: list["Affiliation"] = Relationship(back_populates="party")


class Affiliation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="affiliations")
    party_id: int = Field(foreign_key="party.id")
    party: "Party" = Relationship(back_populates="affiliations")


class VotingEvent(SQLModel, table=True):
    __tablename__ = "voting_event"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    content: str = Field()
    voting_system: str = Field()
    result: str | None = Field(default=None)

    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="voting_events")

    votes: list["Vote"] = Relationship(back_populates="voting_event")


class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    value: str = Field()
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="votes")
    voting_event_id: int = Field(foreign_key="voting_event.id")
    voting_event: "VotingEvent" = Relationship(back_populates="votes")
