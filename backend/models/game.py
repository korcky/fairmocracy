import random 
import string
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

class GameStatus(str, Enum):
    WAITING = "waiting"
    STARTED = "started"
    PAUSED = "paused"
    ENDED = "ended"

class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(default = ''.join(random.choices(string.ascii_lowercase, k=4)))
    name: str = Field()
    current_round: int = Field(default=0)
    current_voting_event: int | None = Field(default=None, foreign_key="voting_event.id")
    status : GameStatus = Field(default=GameStatus.WAITING)
    parties: list["Party"] = Relationship(back_populates="game")
    voters: list["Voter"] = Relationship(back_populates="game")
    voting_events: list["VotingEvent"] = Relationship(back_populates="game")
    #rounds: list["Round"] = Relationship(back_populates="game")    
    #state: str = Field(default="{active: true, current_round: 0, current_voting_event: 0,}")




