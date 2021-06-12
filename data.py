from redis import Redis
from datetime import datetime

class Database:
    def __init__(self):
        self.redis = Redis(host='localhost', port='6379', db=0, decode_responses=True)
        self.USERS_KEY = "users"

    def create_user(self, username) -> bool:
        if not self.user_exists(username):
            self.redis.sadd(self.USERS_KEY, username)
            return True
        return False

    def user_exists(self, username) -> bool:
        return self.redis.sismember(self.USERS_KEY, username)

    def add_yo(self, username, yo):
        if not self.user_exists(username):
            raise IndexError("User doesn't exist")
        inbox_key = f"inbox:{username}"
        self.redis.rpush(inbox_key, str(yo))

    def retrieve_yos(self, username):
        if not self.user_exists(username):
            raise IndexError("User doesn't exist")
        inbox_key = f"inbox:{username}"
        yos = self.redis.lrange(inbox_key, 0, -1)
        return yos