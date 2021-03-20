import pytest

from trades.models import Currency


@pytest.fixture
def default_currency():
    code = 'A' * 8
    name = 'A' * 128
    currency = Currency(code=code, name=name)
    currency.save()

    assert Currency.objects.count() == 1

    return {'id': currency.pk, 'code': code, 'name': name}
