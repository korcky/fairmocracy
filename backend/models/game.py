from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .party import Party

class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    rules: str = Field() # a key indicating which rule system the game uses, e.g. "FI" or something?
    parties: List["Party"] = Relationship(back_populates="game")
    voters: List["Voter"] = Relationship(back_populates="game")
    voting_events: List["VotingEvent"] = Relationship(back_populates="game")
    
    # TODO add game state