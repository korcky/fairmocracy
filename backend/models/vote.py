from datetime import datetime, UTC
from http import HTTPStatus
from fastapi import APIRouter, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, Field, Relationship
from voting_event import VotingEvent
from voter import Voter


class Vote(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    voter_id: int = Field(foreign_key="voter.id")
    voter: "Voter" = Relationship(back_populates="votes")
    voting_event_id: int = Field(foreign_key="voting_event.id")
    voting_event: "VotingEvent" = Relationship(back_populates="votes")
    vote_value: bool = Field()
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @game_router.post(
        "/cast_vote",
        tags=["voting"],
    )

    async def cast_vote(user_id: int, voting_event_id: int, vote_value: bool):
        with Session(engine) as session:
            voter = session.exec(select(Voter).where(Voter.id == user_id)).first()
            voting_event = session.exec(
                select(VotingEvent).where(VotingEvent.id == voting_event_id)
            ).first()
            if not voter or not voting_event:
                return Response(status_code=HTTPStatus.BAD_REQUEST)
            
            #Save vote to database
            vote = Vote(voter_id=user_id, voting_event_id=voting_event_id, vote_value=vote_value)
            session.add(vote)
            session.commit()
            session.refresh(vote)
            return vote 
