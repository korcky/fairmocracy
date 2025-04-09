from sqlmodel import SQLModel, Field, Relationship

class VotingEvent(SQLModel, table=True):
    """
    This class is used to store the information of a voting event (a single issue).
    Attributes:
    - id: A unique identifier for the voting event.
    - subject: The subject of the voting event.
    - round_id: The ID of the round the voting event is part of.
    - round: The round the voting event is part of.
    - votes: The votes cast in the voting event. 
    """
    __tablename__ = "voting_event"
    id: int | None = Field(default=None, primary_key=True)
    subject: str = Field()
    round_id: int = Field(foreign_key="round.id")
    round: "Round" = Relationship(back_populates="voting_events")
    votes: list["Vote"] = Relationship(back_populates="voting_event")
