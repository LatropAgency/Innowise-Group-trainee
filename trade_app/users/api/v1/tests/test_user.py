import json

import pytest

from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestItem:
    def test_auth(self, client, default_user):
        data = {'username': default_user['username'], 'password': default_user['password']}
        url = '/api/token/'
        response = client.post(url, data, content_type="application/json")

        assert response.status_code == 200

    def test_create(self, client):
        data = {'username': 'username', 'password': 'password'}
        url = '/api/v1/users/'
        response = client.post(url, data, content_type="application/json")

        assert User.objects.count() == 1
        assert response.status_code == status.HTTP_201_CREATED
