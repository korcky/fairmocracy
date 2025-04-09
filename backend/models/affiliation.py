from sqlmodel import SQLModel, Field, Relationship


class Affiliation(SQLModel, table=True):
    """
    An affiliation models the relationship between a voter and a party in a specific round.
    Attributes:
    - id: A unique identifier for the affiliation.
    - voter_id: The ID of the voter.
    - voter: The voter associated with this affiliation.
    - party_id: The ID of the party.
    - party: The party associated with this affiliation.
    - round_id: The ID of the round.
    -
    """
    id: int | None = Field(default=None, primary_key=True)
    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="affiliations")
    party_id: int = Field(foreign_key="party.id")
    party: "Party" = Relationship(back_populates="affiliations")
    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="affiliations")