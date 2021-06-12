from typing import Optional

from fastapi import FastAPI
from datetime import date, datetime
app = FastAPI()

users = []
yos = {}

@app.post("/create_user/")
def create_user(username: str):
    users.append(username)
    yos[username] = []
    return "User Created"


@app.post("/yos/")
def send_yo(from_user: str, to_user: str):
    yo_to_send = (from_user, datetime.now())
    yos[to_user].append(yo_to_send)
    return yo_to_send


@app.get("/yos/")
def get_yos(user: str):
    to_return = yos[user]
    yos[user] = []
    return to_return
