import os
import random
import re

import pytest
from redis import Redis

from emojyo.main import create_user, get_yos, send_yo

user_name_list = [
    "Bear",
    "Steve",
]


@pytest.fixture
def clean_redis():
    Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]).flushall()
    yield
    Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]).flushall()



def test_register_repeat_user_with_redis_active(clean_redis):
    received_yos = {}
    for user_name in user_name_list:
        create_user(user_name)
    create_user(user_name_list[0])

    send_user = "Bear"
    receive_user = "Steve"
    received_yos[receive_user] = received_yos.get(receive_user, [])
    received_yos[receive_user].append(send_user)
    send_yo(send_user, receive_user)

    receive_user = "Steve"
    send_user = "Bear"
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
