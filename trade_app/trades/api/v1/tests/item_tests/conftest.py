import pytest

from trades.models import Item
from trades.models import Currency


@pytest.fixture
def default_currency():
    code = 'A' * 8
    name = 'A' * 128
    currency = Currency(code=code, name=name)
    currency.save()

    assert Currency.objects.count() == 1

    return {'id': currency.pk, 'code': code, 'name': name}


@pytest.fixture
def default_item(default_currency):
    code = 'A' * 8
    name = 'A' * 128
    price = 1
    details = 'details'
    item = Item(code=code, name=name, price=price, currency=Currency.objects.get(pk=default_currency['id']),
                details=details)
    item.save()

    assert Item.objects.count() == 1

    return {'id': item.pk, 'price': price, 'details': details}
