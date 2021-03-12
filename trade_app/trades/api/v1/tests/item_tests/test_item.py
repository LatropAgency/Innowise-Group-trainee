import json

import pytest

from rest_framework import status


@pytest.mark.django_db
class TestItem:
    def test_list(self, client, access_token):
        url = '/api/v1/items/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, client, access_token, default_item):
        url = f'/api/v1/items/{default_item["id"]}/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client, access_token, default_currency):
        url = f'/api/v1/items/'
        data = {
            'code': 'a' * 8,
            'name': 'a' * 128,
            'price': 1,
            'currency': default_currency['id'],
            'details': 'a' * 512,
        }
        response = client.post(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, client, access_token, default_item, default_currency):
        url = f'/api/v1/items/{default_item["id"]}/'
        data = {
            'code': 'a' * 8,
            'name': 'a' * 128,
            'price': 2,
            'currency': default_currency['id'],
            'details': 'a' * 512,
        }
        response = client.put(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client, access_token, default_item):
        url = f'/api/v1/items/{default_item["id"]}/'
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_access(self, client):
        url = '/api/v1/items/'
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_code_length(self, client, access_token, default_currency):
        data = {
            'code': 'a' * 9,
            'name': 'a' * 127,
            'price': 2,
            'currency': default_currency['id'],
            'details': 'a' * 512,
        }
        url = f'/api/v1/items/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_name_length(self, client, access_token, default_currency):
        data = {
            'code': 'a' * 8,
            'name': 'a' * 129,
            'price': 2,
            'currency': default_currency['id'],
            'details': 'a' * 512,
        }
        url = f'/api/v1/items/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_details_length(self, client, access_token, default_currency):
        data = {
            'code': 'a' * 8,
            'name': 'a' * 128,
            'price': 2,
            'currency': default_currency['id'],
            'details': 'a' * 513,
        }
        url = f'/api/v1/items/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_price_max_digits(self, client, access_token, default_currency):
        data = {
            'code': 'a' * 8,
            'name': 'a' * 128,
            'price': 22222222,
            'currency': default_currency['id'],
            'details': 'a' * 512,
        }
        url = f'/api/v1/items/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_price_decimal_places(self, client, access_token, default_currency):
        data = {
            'code': 'a' * 8,
            'name': 'a' * 128,
            'price': 0.222,
            'currency': default_currency['id'],
            'details': 'a' * 512,
        }
        url = f'/api/v1/items/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
