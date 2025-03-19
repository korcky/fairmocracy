from sqlmodel import SQLModel, Field, Relationship


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    rules: str = Field() # a key indicating which rule system the game uses, e.g. "FI" or something?
    parties: list["Party"] = Relationship(back_populates="game")
    voters: list["Voter"] = Relationship(back_populates="game")
    voting_events: list["VotingEvent"] = Relationship(back_populates="game")
    
    # TODO add game state