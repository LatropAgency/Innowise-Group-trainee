import pytest

from rest_framework import status


@pytest.mark.django_db
class TestCurrency:
    def test_list(self, client, access_token):
        url = '/api/v1/currencies/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, client, access_token, default_currency):
        url = f'/api/v1/currencies/{default_currency["id"]}/'
        response = client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client, access_token):
        url = f'/api/v1/currencies/'
        data = {'code': 'A' * 4, 'name': 'Apple' * 4}
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, client, access_token, default_currency):
        url = f'/api/v1/currencies/{default_currency["id"]}/'
        data = {'code': 'B' * 4, 'name': 'Bpple' * 4}
        response = client.put(url, data, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client, access_token, default_currency):
        url = f'/api/v1/currencies/{default_currency["id"]}/'
        response = client.delete(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_access(self, client):
        url = '/api/v1/currencies/'
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_code_length(self, client, access_token):
        data = {'code': 'A' * 9, 'name': 'A' * 128}
        url = f'/api/v1/currencies/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_name_length(self, client, access_token):
        data = {'code': 'A' * 8, 'name': 'A' * 129}
        url = f'/api/v1/currencies/'
        response = client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
