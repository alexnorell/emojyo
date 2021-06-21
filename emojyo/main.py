from typing import Optional

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import date, datetime

from emojyo.data import Database

MIN_USERNAME_LENGTH=3

DB = Database()

app = FastAPI()

@app.post("/create_user/")
def create_user(username: str):
    if len(username) >= MIN_USERNAME_LENGTH:
        DB.create_user(username)
        return "User Created"
    else:
        return f"Username Must be at least {MIN_USERNAME_LENGTH} characters"


@app.post("/yos/")
def send_yo(from_user: str, to_user: str):
    yo_to_send = (from_user, datetime.now())
    DB.add_yo(to_user, yo_to_send)
    return yo_to_send


@app.get("/yos/")
def get_yos(user: str):
    to_return = DB.retrieve_yos(user)
    return to_return
