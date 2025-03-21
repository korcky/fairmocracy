from fastapi import FastAPI
from sqlalchemy import create_engine
from Game import Game
from VotingEvent import VotingEvent
from finnish_system import FinnishSystem

app = FastAPI()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#Mock events for advancing the game, replace with config file
event1 = VotingEvent("Event 1", "Description 1", FinnishSystem())
event2 = VotingEvent("Event 2", "Description 2", FinnishSystem())

game = Game("Test Game", "A test game", [event1, event2])

#TODO add config file reading

