from sqlmodel import SQLModel, Field, Relationship

class Affiliation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="affiliations")
    party_id: int = Field(foreign_key="party.id")
    party: "Party" = Relationship(back_populates="affiliations")
    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="affiliations")