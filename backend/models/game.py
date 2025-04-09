import random 
import string
from sqlmodel import SQLModel, Field, Relationship


class Game(SQLModel, table=True):
    """
    A game models a voting game.
    Attributes:
    - id: A unique identifier for the game.
    - hash: A unique hash for the game. (not really a hash)
    - name: The name of the game.
    - voters: The voters (players) in the game.
    - rounds: The rounds of the game.
    - state: The state of the game: a JSON object stored as a string (perhaps a better solution exists). 
    """
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(default = ''.join(random.choices(string.ascii_lowercase, k=4)))
    name: str = Field()
    voters: list["Voter"] = Relationship(back_populates="game")
    rounds: list["Round"] = Relationship(back_populates="game")    
    state: str = Field(default="{\"current_round\": 0}")

    # TODO add game state

 