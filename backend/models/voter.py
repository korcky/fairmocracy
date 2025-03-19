from sqlmodel import SQLModel, Field, Relationship

# This class represents a voter. It contains the following attributes:
# - id: A unique identifier for the voter.
# - name: The name of the voter.
# - Party Affiliation: The party affiliation of the voter.
# - votingEvent: The voting event that the voter is participating in.

class Voter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    party_id: int = Field(foreign_key="party.id")
    party: "Party" = Relationship(back_populates="voters")
    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="voters")
    votes: list["Vote"] = Relationship(back_populates="voter")
