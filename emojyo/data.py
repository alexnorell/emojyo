from os import environ as env

from redis import Redis


class Database:
    def __init__(self):
        redis_port = env.get("REDIS_PORT")
        redis_host = env.get("REDIS_HOST")
        if not redis_port:
            raise ValueError("REDIS_PORT needs to be set")
        if not redis_host:
            raise ValueError("REDIS_HOST needs to be set")
        self.redis: Redis = Redis(
            host=redis_host, port=redis_port, db=0, decode_responses=True
        )
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
