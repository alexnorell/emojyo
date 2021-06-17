from typing import Optional

from fastapi import FastAPI
from datetime import date, datetime

from emojyo.data import Database

DB = Database()

app = FastAPI()


@app.post("/create_user/")
def create_user(username: str):
    DB.create_user(username)
    return "User Created"


@app.post("/yos/")
def send_yo(from_user: str, to_user: str):
    yo_to_send = (from_user, datetime.now())
    DB.add_yo(to_user, yo_to_send)
    return yo_to_send


@app.get("/yos/")
def get_yos(user: str):
    to_return = DB.retrieve_yos(user)
    return to_return
