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
    # Add a username a second time
    create_user(user_name_list[0])

    # Send a yo from the repeated username
    send_user = user_name_list[0]
    receive_user = user_name_list[1]
    # Add transaction to receieved_yos list to for checker to know expected list of received yos
    received_yos[receive_user] = received_yos.get(receive_user, [])
    received_yos[receive_user].append(send_user)
    
    send_yo(send_user, receive_user)

    # Send a yo to the repeated username
    receive_user = user_name_list[1]
    send_user = user_name_list[0]
    # Add transaction to receieved_yos list to for checker to know expected list of received yos
    received_yos[receive_user] = received_yos.get(receive_user, [])
    received_yos[receive_user].append(send_user)
    
    send_yo(send_user, receive_user)

    for user_name in user_name_list:
        # Get list of Yo's sent to user and extract the username of the sender
        yos = get_yos(user_name)
        yo_senders = [re.search(r"(\w+)", yo_string).group(0) for yo_string in yos]
        # Check that the return list of senders matches the expected list of senders
        assert received_yos.get(user_name, []) == yo_senders
