import random 
import string
from sqlmodel import SQLModel, Field, Relationship


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(default = ''.join(random.choices(string.ascii_lowercase, k=4)))
    name: str = Field()
    voters: list["Voter"] = Relationship(back_populates="game")
    rounds: list["Round"] = Relationship(back_populates="game")    
    state: str = Field(default="{\"current_round\": 0}")
    # TODO add game state

 