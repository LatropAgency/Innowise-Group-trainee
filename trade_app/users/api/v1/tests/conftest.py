import json

import pytest

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


@pytest.fixture
def default_user():
    username = 'username'
    password = 'password'
    user = User(username=username, password=make_password(password))
    user.save()

    assert User.objects.count() == 1

    return {'username': username, 'password': password}
