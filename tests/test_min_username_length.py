import os
import re

import pytest
from redis import Redis

from emojyo.main import create_user

@pytest.fixture
def clean_redis():
    Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]).flushall()
    yield
    Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]).flushall()


def test_min_username_length_with_redis_running(clean_redis):
    received_yos = {}
    assert create_user('') != "User Created"
    assert create_user('a') != "User Created"
    assert create_user('ab') != "User Created"
    assert create_user('abc') == "User Created"
