from main import create_user
from main import send_yo
from main import get_yos
import random
import pytest
import os
from redis import Redis
import re

NUMBER_OF_RANDOM_VALID_YOS = 10

user_name_list = [
                    "Bear",
                    "Steve",
                    "Kellie",
                    "Mykell",
                    "Ray",
                    "Grant",
                    "Anna",
                    "Brittany",
                    "Jennifer",
                    "Carolyn",
                    "Sheryl",
                    "Geraldine",
                    "Ana",
                    "Pam",
                    "Luther"
                ]

@pytest.fixture
def clean_redis():
    Redis(port=os.environ["REDIS_PORT"]).flushall()
    yield
    Redis(port=os.environ["REDIS_PORT"]).flushall()


def test_basic_functionality_with_redis_running(clean_redis):
    received_yos={}
    for user_name in user_name_list:
        create_user(user_name)

    for _ in range(NUMBER_OF_RANDOM_VALID_YOS):
        send_user,receive_user = random.sample(user_name_list, 2)
        received_yos[receive_user] = received_yos.get(receive_user, [])
        received_yos[receive_user].append(send_user)
        send_yo(send_user, receive_user)

    for user_name in user_name_list:
        yos = get_yos(user_name)
        yo_senders = [re.search(r"(\w+)", yo_string).group(0) for yo_string in yos]
        if received_yos.get(user_name, []) == yo_senders:
            assert True
        else:
            assert False

    

