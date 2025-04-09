from sqlmodel import SQLModel, Field, Relationship

class Round(SQLModel, table=True):
    """
    A round of voting in a game.
    Attributes:
    - id: A unique identifier for the round.
    - game_id: The ID of the game the round belongs to.
    - game: The game the round belongs to.
    - round_number: The number of the round.
    - rules: The rules of the round.
    - voting_events: The voting events in the round.
    - parties: The parties in the round.
    - affiliations: The affiliations in the round.
    """
    id: int = Field(primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="rounds")
    round_number: int = Field(default=0)
    rules: str = Field()
    voting_events: list["VotingEvent"] = Relationship(back_populates="round")
    parties: list["Party"] = Relationship(back_populates="round")
    affiliations: list["Affiliation"] = Relationship(back_populates="round")

