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


@pytest.fixture
def access_token(client, default_user):
    data = {'username': default_user['username'], 'password': default_user['password']}
    url = '/api/token/'
    response = client.post(url, data, content_type="application/json")

    assert response.status_code == 200

    return json.loads(response.content)['access']
