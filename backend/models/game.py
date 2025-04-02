import random 
import string
from sqlmodel import SQLModel, Field, Relationship


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(default = ''.join(random.choices(string.ascii_lowercase, k=4)))
    name: str = Field()
    parties: list["Party"] = Relationship(back_populates="game")
    voters: list["Voter"] = Relationship(back_populates="game")
    rounds: list["Round"] = Relationship(back_populates="game")    
    state: str = Field()
    # TODO add game state
