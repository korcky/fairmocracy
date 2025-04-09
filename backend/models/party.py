from sqlmodel import SQLModel, Field, Relationship


class Party(SQLModel, table=True):
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
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="parties")
    affiliations: list["Affiliation"] = Relationship(back_populates="party")
