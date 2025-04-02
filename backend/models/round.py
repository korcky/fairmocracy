from sqlmodel import SQLModel, Field, Relationship

class Round(SQLModel, table=True):
    id: int = Field(primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="rounds")
    round_number: int = Field()
    rules: str = Field()
    voting_events: list["VotingEvent"] = Relationship(back_populates="round")
