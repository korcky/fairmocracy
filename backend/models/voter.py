from sqlmodel import SQLModel, Field, Relationship

# This class represents a voter. It contains the following attributes:
# - id: A unique identifier for the voter.
# - name: The name of the voter.
# - Party Affiliation: The party affiliation of the voter.
# - votingEvent: The voting event that the voter is participating in.

class Voter(SQLModel, table=True):
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
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="voters")
    votes: list["Vote"] = Relationship(back_populates="voter")
    affiliations: list["Affiliation"] = Relationship(back_populates="voter")
