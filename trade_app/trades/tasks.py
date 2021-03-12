from celery import shared_task

from core.base_item_transfer import ItemTransfer
from core.enum_types import OrderType
from trades.models import (
    Offer,
    Trade,
    Item,
)


@shared_task
def offers_handler():
    items = Item.objects.all()
    offers = Offer.objects.filter(is_active=True)
    for item in items:
        for buy_offer in offers.filter(item=item, order_type=OrderType.BUY.value):
            buy_offer_unit_price = ItemTransfer.get_unit_price(buy_offer)
            sale_offers = offers.filter(item=item, order_type=OrderType.SALE.value, price__lte=buy_offer.price)
            valid_sale_offers = filter(lambda offer: buy_offer_unit_price >= ItemTransfer.get_unit_price(offer),
                                       sale_offers)
            for sale_offer in sorted(valid_sale_offers, key=lambda offer: ItemTransfer.get_unit_price(offer)):
                diff = min(buy_offer.quantity, sale_offer.quantity)
                Trade(item=item, seller=sale_offer.user, buyer=buy_offer.user, quantity=diff,
                      unit_price=sale_offer.price / sale_offer.quantity, buyer_offer=buy_offer,
                      seller_offer=sale_offer).save()
                [ItemTransfer.handling_offer(offer, diff) for offer in [buy_offer, sale_offer]]
                ItemTransfer.items_transfer(sale_offer, diff)
                ItemTransfer.items_transfer(buy_offer, diff, True)
                if not buy_offer.quantity:
                    break
