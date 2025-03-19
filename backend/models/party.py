from sqlmodel import SQLModel, Field, Relationship


class Party(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
    voters: list["Voter"] = Relationship(back_populates="party")
    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="parties")