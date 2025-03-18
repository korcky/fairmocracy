from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .voter import Voter

class Party(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    voters: List["Voter"] = Relationship(back_populates="party")
    game_id: int = Field(foreign_key="game.id")
    game: "Game" = Relationship(back_populates="parties")