from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

@app.get("/")
async def root():
    return {"message": "Hello World"}


