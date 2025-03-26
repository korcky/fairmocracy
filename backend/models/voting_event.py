from sqlmodel import SQLModel, Field, Relationship

# This class is used to store the information of a voting event (a single issue).
# It contains the following attributes:
# - id: A unique identifier for the voting event.
# - subject: The subject of the voting event.
# - game_id: The game that the voting event is a part of. 

class VotingEvent(SQLModel, table=True):
    __tablename__ = "voting_event"
    id: int | None = Field(default=None, primary_key=True)
    subject: str = Field()
    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="voting_events")
    votes: list["Vote"] = Relationship(back_populates="voting_event")
